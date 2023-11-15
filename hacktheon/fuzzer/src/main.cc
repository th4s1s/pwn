#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <pthread.h>

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/prctl.h>
#include <sys/socket.h> 
#include <sys/wait.h>


#include <unistd.h>
#include <signal.h>

#include "instrument.h"
#include "fork_server.h"

#define CHILD 200
#define PARENT 201

#define MAX_SIZE 0x1000

// limit max size
void get_source_from_user(run_t *client) {
	system("rm /tmp/*");
	char *buf = (char *)malloc(0x100);
	sprintf(buf, "/tmp/ssXXXXXX");

	int fd = mkstemp(buf);
	char *cmd = (char *)malloc(0x100);
	char *source = (char *)malloc(MAX_SIZE);
	uint64_t source_size = 0;
	memset((void *)source, 0, MAX_SIZE);
	printf("[-] input fetch buffer size > ");
	read(0, (void *)&client->limit, 8);

	if (client->limit > MAX_SIZE) {
		printf("[-] invalid fetch buffer size\n");
		exit(-1);
	}

	printf("[-] input source code size > ");
	read(0, (void *)&source_size, 8);

	if (source_size > MAX_SIZE) {
		printf("[-] invalid source size\n");
		exit(-1);
	}

	printf("[-] input source code > ");
	read(0, (void *)source, source_size);

	sprintf(cmd, "mv %s %s.c", buf, buf);
	system(cmd);

	write(fd, (void *)source, source_size);
	close(fd);

	client->filename = (char *)malloc(0x100);
	sprintf(client->filename, "/tmp/test");
	sprintf(cmd, "gcc %s.c -o /tmp/test -fno-stack-protector /fetch.c", buf);
	system(cmd);

	sprintf(cmd, "python get_patchpoints.py %s", client->filename);
	system(cmd);
}

void run() {
	run_t *client = (run_t *)malloc(sizeof(run_t));
	uint64_t limit = 0;

	if (socketpair(AF_UNIX, SOCK_STREAM, 0, client->sv) < 0) { 
		perror("socketpair error"); 
		exit(0); 
	}

	if (socketpair(AF_UNIX, SOCK_STREAM, 0, client->dsv) < 0) { 
		perror("socketpair error"); 
		exit(0); 
	}

	dup2(client->sv[0], CHILD);
	dup2(client->sv[1], PARENT);

	close(client->sv[0]);
	close(client->sv[1]);

	get_source_from_user(client);

	client->cov = 0;
	client->InputFd = open("/dev/urandom", O_RDONLY);

	client->InputBuffer = (uint8_t *)malloc(client->limit);
	client->report = (char *)malloc(0x1000);

	trapFuzzInstall(client);
}

int main(int argc, char *argv[]) {
	alarm(20);
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
	printf("[-] HACKTHEON Challenge\n");
	run();
	return 0;
}
