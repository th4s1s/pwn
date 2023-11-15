#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <dlfcn.h>
#include <string.h>
#include <stdlib.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/ptrace.h>

#include <signal.h>
#include <elf.h>
#include <execinfo.h>

#include "instrument.h"
#include "seccomp-bpf.h"

#define SHADOW_SIZE 1024 * 1024 * 16
void *shadow_addr;
run_t *client;

#define SECRET_SYS 0x646e616873797377
#define SECRET_TRAP 0x6567617265766f67
#define SECRET_NORMAL 0x58454c414d524f47
#define SECRET_SEGV 0x646e616876676577

static int install_syscall_filter(void)
{
    struct sock_filter filter[] = {
        VALIDATE_ARCHITECTURE,
        EXAMINE_SYSCALL,
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        ALLOW_SYSCALL(fstat),
        ALLOW_SYSCALL(exit),
        ALLOW_SYSCALL(brk),
        ALLOW_SYSCALL(exit),
        ALLOW_SYSCALL(exit_group),
        ALLOW_SYSCALL(rt_sigreturn),
        KILL_PROCESS
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        perror("prctl(NO_NEW_PRIVS)");
        goto failed;
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        perror("prctl(SECCOMP)");
        goto failed;
    }

    return 0;

failed:
    if (errno == EINVAL)
        fprintf(stderr, "SECCOMP_FILTER is not available. :(\n");
    return 1;
}

#define SHADOW(addr) ((uint32_t*)(((uintptr_t)addr & 0xfffffffffffffffc) - 0x200000000000 - ((uintptr_t)addr & 0x3)*0x10000000000))

#define CHILD 200
#define PARENT 201

static int (*main_addr)(int, char **, char **);

void trap_handler(int signum, siginfo_t* si, void* context) {
    ucontext_t *ctx = (ucontext_t *)context;
    uint64_t pc = (uint64_t)ctx->uc_mcontext.gregs[REG_RIP] - 1;
    uint32_t v = *(uint32_t *)((uint64_t)client->shadow_addr + (pc - (uint64_t)client->binary_addr));
    uint8_t origByte = v & 0xff;
    uint64_t index = v >> 8;

    // coverage update
    uint64_t _cmd = SECRET_TRAP;
    int nr = write(CHILD, (void *)&_cmd, 8);
    if (nr < 0) {
        printf("[-] ERROR COVERAGE UPDATE\n");
        exit(-1);
    }

    uint64_t pos = (index << 48) | (pc - (uint64_t)client->binary_addr);

    int b = 0;
    b += sprintf(client->report, "[%p] coverage update... %#llx @ %#x -> %#x", (void *)pc, pc - (uint64_t)client->binary_addr, *(uint8_t *)pc, origByte);
    write(CHILD, client->report, 0x1000);
    write(CHILD, &pos, 8);

    // restore pc
    *(uint8_t *)pc = origByte;
    ctx->uc_mcontext.gregs[REG_RIP] = pc;
}

void segv_handler(int signum, siginfo_t* si, void* context) {
    void *array[50] = {};
    ucontext_t *ctx = (ucontext_t *)context;
    void *pc = (void *)ctx->uc_mcontext.gregs[REG_RIP];

    uint64_t _cmd = SECRET_SEGV;
    int nr = write(CHILD, (void *)&_cmd, 8);
    if (nr < 0) {
        exit(-1);
    }

    int b = 0;
    b += sprintf(client->report + b, "=================SIGSEGV=================\n");
    b += sprintf(client->report + b, "RIP : %p\n", (void *)pc);
    b += sprintf(client->report + b, "RAX : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RAX]);
    b += sprintf(client->report + b, "RBX : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RBX]);
    b += sprintf(client->report + b, "RCX : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RCX]);
    b += sprintf(client->report + b, "RDX : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RDX]);
    b += sprintf(client->report + b, "RSI : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RSI]);
    b += sprintf(client->report + b, "RDI : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RDI]);
    b += sprintf(client->report + b, "RBP : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RBP]);
    b += sprintf(client->report + b, "RSP : %p\n", (void *)ctx->uc_mcontext.gregs[REG_RSP]);

    b += sprintf(client->report + b, "=================CLIENT=================\n");
    b += sprintf(client->report + b, "pid : %#lx\n", (uint64_t)client->pid);
    b += sprintf(client->report + b, "numPatchPoints : %#lx\n", (uint64_t)client->numPatchPoints);
    b += sprintf(client->report + b, "filename : %#lx\n", (uint64_t)client->filename);
    b += sprintf(client->report + b, "bbMap : %#lx\n", (uint64_t)client->bbMap);
    b += sprintf(client->report + b, "pcGuardMap : %#lx\n", (uint64_t)client->feedback.pcGuardMap);
    b += sprintf(client->report + b, "bbMapPc : %#lx\n", (uint64_t)client->feedback.bbMapPc);
    b += sprintf(client->report + b, "bbMapEdge : %#lx\n", (uint64_t)client->feedback.bbMapEdge);


    nr = write(CHILD, client->report, 0x1000);
    if (nr < 0) {
        exit(-1);
    }

    // coverage update
    exit(-1);
}

void sigsys_check(int signum, siginfo_t* si, void* context) {
    uint64_t _cmd = SECRET_SYS;
    write(CHILD, (void *)&_cmd, 8);
    exit(-1);
}

uint64_t find_base_address(uint64_t addr) {
    for (int i = 0; ; i++) {
        addr -= 0x1000 * i;
        uint32_t magic = *(uint32_t *)addr;
        if (magic == 0x464c457f) {
            return addr;
        }
    }
}

// Parse text area information
uint64_t elfParse(char *filename) {
    struct stat sb;
    stat(filename, &sb);
    int fileFd = open(filename, O_RDONLY);
    void *base = mmap(NULL, sb.st_size, PROT_READ, MAP_PRIVATE, fileFd, 0);

    Elf64_Ehdr *elf_header = (Elf64_Ehdr *)base;
    Elf64_Shdr *sec_header = base + elf_header->e_shoff;
    Elf64_Shdr *sh_strtab = &sec_header[elf_header->e_shstrndx];
    char *sh_strtab_p = (char *)base + sh_strtab->sh_offset;

    for (int i = 0; i < elf_header->e_shnum; i++) {
        if (strncmp(sh_strtab_p + sec_header[i].sh_name, ".text", 5) == 0) {
            close(fileFd);
            return (uint64_t)sec_header[i].sh_size;
        }
    }

    return (uint64_t)0;
}

// what if only __start function exist in target binary?
int __libc_start_main(
    int (*main)(int, char **, char **),
    int argc,
    char **argv,
    int (*init)(int, char **, char **),
    void (*fini)(void),
    void (*rtld_fini)(void),
    void *stack_end)
{
    client = (run_t *)malloc(sizeof(run_t));
    if (!client) {
        printf("[-] Allocate client error\n");
        exit(-1);
    }

    uint64_t receiver = 0;
    main_addr = (int (*)(int, char **, char **))main;

    typeof(&__libc_start_main) orig = (typeof(&__libc_start_main))dlsym(RTLD_NEXT, "__libc_start_main");

    uint64_t base_addr = find_base_address((uint64_t)main_addr & ~(uint64_t)0xfff);
    uint64_t textSize = elfParse(argv[0]);
    if (textSize == 0) {
        exit(-1);
    }

    mprotect((void *)base_addr, textSize + 0x1000, 7);

    write(CHILD, "ADDR", 4);
    read(CHILD, &receiver, 4);
    if (receiver != 'ENOD') {
        exit(-1);
    }

    write(CHILD, &base_addr, 8);

    // trap handler
	struct sigaction s;
    s.sa_flags = SA_SIGINFO;
    s.sa_sigaction = trap_handler;
    sigemptyset(&s.sa_mask);
    sigaction(SIGTRAP, &s, 0);

    // segv handler
    struct sigaction s2;
    s2.sa_flags = SA_SIGINFO;
    s2.sa_sigaction = segv_handler;
    sigemptyset(&s2.sa_mask);
    sigaction(SIGSEGV, &s2, 0);

    // sys handler
    struct sigaction s3;
    s3.sa_flags = SA_SIGINFO;
    s3.sa_sigaction = sigsys_check;
    sigemptyset(&s3.sa_mask);
    sigaction(SIGSYS, &s3, 0);

    read(CHILD, &receiver, 4);
    if (receiver != 0x13371337) {
        exit(-1);
    }

    void *shadow_addr = SHADOW((uint64_t)base_addr);
    void *shadow = mmap((void *)shadow_addr, SHADOW_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON | MAP_FIXED, 0, 0);
    memset(shadow, 0, SHADOW_SIZE);
    if (shadow == MAP_FAILED || shadow != shadow_addr) {
        printf("[-] Failed to allocate shadow memory\n");
        exit(-1);
    }

    read(CHILD, client, sizeof(run_t));
    client->shadow_addr = shadow;
    client->patchPoints = (uint64_t *)malloc(sizeof(uint64_t) * client->numPatchPoints);
    client->report = (char *)malloc(0x1000);
    memset(client->report, 0, 0x1000);

    uint8_t origByte = NULL;
    for (uint64_t i = 0; i < client->numPatchPoints; i++) {
        int nr = read(CHILD, &client->patchPoints[i], 8);
        if (nr != 8) {
            printf("[-] IO ERROR\n");
            exit(-1);
        }

        origByte = *(uint8_t *)(base_addr + client->patchPoints[i]);
        *(uint32_t *)(client->shadow_addr + client->patchPoints[i]) = (uint32_t)(i << 8 | (uint32_t)origByte);
        *(uint8_t *)(base_addr + client->patchPoints[i]) = 0xcc;
    }

    install_syscall_filter();
    main(argc, argv, NULL);
    printf("OUT\n");
    uint64_t _cmd = SECRET_NORMAL;
    write(CHILD, (void *)&_cmd, 8);
    exit(0);
    return 0;
}

