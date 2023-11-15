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

#include "instrument.h"
#include "seccomp-bpf.h"

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

void trap_check_once(int signum, siginfo_t* si, void* context) {
	write(CHILD, "TRAP", 4);
	exit(-1);
}

void sigsys_check(int signum, siginfo_t* si, void* context) {
    write(CHILD, "SSYS", 4);
    exit(-1);
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
    main_addr = (int (*)(int, char **, char **))main;
    typeof(&__libc_start_main) orig = (typeof(&__libc_start_main))dlsym(RTLD_NEXT, "__libc_start_main");

	struct sigaction s;
    s.sa_flags = SA_SIGINFO;
    s.sa_sigaction = trap_check_once;
    sigemptyset(&s.sa_mask);
    sigaction(SIGTRAP, &s, 0);

    struct sigaction s2;
    s2.sa_flags = SA_SIGINFO;
    s2.sa_sigaction = sigsys_check;
    sigemptyset(&s2.sa_mask);
    sigaction(SIGSYS, &s2, 0);

    install_syscall_filter();
    main(argc, argv, NULL);
	write(CHILD, "INIT", 4);
	exit(0);
	return 0;
}

