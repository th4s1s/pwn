#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/socket.h>
#include <sys/wait.h>

#include <unistd.h>
#include <signal.h>
#include <elf.h>

#include <linux/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

#include "seccomp-bpf.h"
#include "instrument.h"
#include "fork_server.h"

#define CHILD 200
#define PARENT 201

static feedback_t bbMapFb;
feedback_t* feedback = &bbMapFb;
uint32_t my_thread_no = 0;

#define SHADOW_SIZE 1024 * 1024 * 16
#define SHADOW(addr) ((uint32_t*)(((uintptr_t)addr & 0xfffffffffffffffc) - 0x200000000000 - ((uintptr_t)addr & 0x3)*0x10000000000))

int prepareSubProc(run_t *client) {
	int status = 0;
	pid_t pid = fork();
	if (!pid) {
		close(0);
		close(1);
		close(2);

		setenv("LD_PRELOAD", "./main_hook.so", 1);
		execl(client->filename, client->filename, 0);
	} else {
		client->pid = pid;
		uint64_t res = 0;
		read(PARENT, (void *)&res, 4);
		if (res != 'RDDA') {
			printf("[-] ACK fail\n");
			return 0;
		}

		write(PARENT, "DONE", 4);
		if (read(PARENT, &res, 8) != 8) {
			printf("[-] read fail\n");
			return 0;
		}

		client->binary_addr = (void *)res;
		return 1;
	}
}

void RunLoop(run_t *client) {
	if (prepareSubProc(client) != 1) {
		printf("[-] Prepare fail\n");
		exit(-1);
	}

	runSubProc(client);
}

void fetchPatchPoints(run_t *client) {
    FILE* patches = fopen("/tmp/patches.txt", "r");
    if (!patches) {
        printf("Couldn't open patchfile %s", client->filename);
        exit(-1);
    }

    // Index into the coverage bitmap for the current trap instruction.
    int bitmap_index = -1;

    char* line = NULL;
    size_t nread, len = 0;
    uint64_t index = 0;
    while ((nread = getline(&line, &len, patches)) != -1) {
    	char* end = line + len;
    	char* col = strchr(line, '@');
    	if (col) {
    		*col = 0;
    		unsigned long size = strtoul(col + 1, &end, 16);

    		if (size == 0xc0fec0fe) {
    			printf("[-] Invalid binary\n");
    			exit(-1);
    		}

    		client->numPatchPoints = (uint64_t)size;
    		client->patchPoints = (uint64_t *)malloc(sizeof(uint64_t) * client->numPatchPoints);
    		col = NULL;
    		continue;
    	}

    	unsigned long offset = strtoul(line, &end, 16);
    	if (index > _COV_BITMAP_MAX_SIZE) {
    		printf("[-] COV GUARD OVERFLOW\n");
    		exit(-1);
    	}

    	// initialize pcGuardMap
    	client->feedback.pcGuardMap[index] = 0;
    	client->patchPoints[index++] = (uint64_t)offset;
	}

	fclose(patches);
}

void trapFuzzInstall(run_t *client) {
	client->bbMap = feedback;
	fetchPatchPoints(client);

	while(1) {
		sleep(1);
		RunLoop(client);
		puts("");
	}
}





