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
#include <sys/wait.h>

#include <unistd.h>
#include <signal.h>
#include <elf.h>

#include "instrument.h"
#include "fork_server.h"

#define CHILD 200
#define PARENT 201
#define SECRET 0xc0fec0de
#define SECRET_SYS 0x646e616873797377
#define SECRET_TRAP 0x6567617265766f67
#define SECRET_NORMAL 0x58454c414d524f47
#define SECRET_SEGV 0x646e616876676577

int check_arbitrary_trap_inst(run_t *client) {
	pid_t pid = fork();
	if (!pid) {
		close(0);
		close(1);
		close(2);

		setenv("LD_PRELOAD", "./child_hook.so", 1);
		execl(client->filename, client->filename, 0);
	} else {
		uint64_t res = 0;
		while (1) {
			sleep(1);
			read(PARENT, (void *)&res, 4);
			if (res == 'PART') {
				printf("[-] Invalid Binary\n");
				return 0;
			}
			if (res == 'TINI') {
				printf("[-] Pass initial check routine\n");
				return 1;
			}
			if (res == 'SYSS') {
				printf("[-] Invalid syscall\n");
				return 0;
			}
		}
	}
}

void fetch(run_t *client) {
	char buffer[0x1000] = {0, };
	for (uint64_t i = 0; i < client->limit; i++) {
		uint8_t v = 0;
		read(client->InputFd, (void *)&v, 1);

		if (v == '\n')
			break;

		*(uint8_t *)(buffer + i) = v;

	}
	write(PARENT, (void *)buffer, client->limit);
}

// Fuzz routine
void runSubProc(run_t *client) {
	write(PARENT, "\x37\x13\x37\x13", 4);
	write(PARENT, client, sizeof(run_t));

	for (uint64_t i = 0; i < client->numPatchPoints; i++) {
		write(PARENT, &client->patchPoints[i], 8);
	}

	uint64_t cmd = NULL;
	int status = 0;

	while(1) {
		int nr = read(PARENT, (void *)&cmd, 8);
		if (nr < 0) {
			printf("[-] IO ERROR");
			exit(-1);
		}

		// SIGSYS
		if (cmd == SECRET_SYS) {
			printf("[-] SIGSYS\n");
			exit(-1);
		}

		// NORMAL
		if (cmd == SECRET_NORMAL) {
			break;
		}

		// FETCH
		if (cmd == SECRET) {
			fetch(client);
			continue;
		}

		// SIGTRAP
		if (cmd == SECRET_TRAP) {
			read(PARENT, client->report, 0x1000);

			uint64_t v = 0;
			read(PARENT, &v, 8);
			uint16_t index = v >> 48;
			uint64_t pos = (v & 0x0000ffffffffffff) / 8;
			uint8_t q = (v & 0x0000ffffffffffff) % 8;

			client->feedback.bbMapPc[pos] ^= 1 << q;
			client->feedback.bbMapEdge[pos] = index & (1 << q);

			bool prev = ATOMIC_XCHG(client->feedback.pcGuardMap[index], true);
			if (prev == false) {
				client->cov++;
				printf("%s, (%#lx, %f\%)\n", client->report, pos, ((float)client->cov / (float)client->numPatchPoints) * 100);
			}

			continue;
		}

		// SIGSEGV
		if (cmd == SECRET_SEGV) {
			read(PARENT, client->report, 0x1000);
			printf("%s\n", client->report);
			break;
		}
	}

	waitpid(client->pid, &status, 0);
}
