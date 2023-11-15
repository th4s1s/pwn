#include <stdio.h>
#include <unistd.h>

int main() {
    long maxFileDescriptors = sysconf(_SC_OPEN_MAX);
    if (maxFileDescriptors == -1) {
        perror("sysconf");
        // Handle the error...
    } else {
        printf("Maximum number of open file descriptors: %ld\n", maxFileDescriptors);
    }

    return 0;
}
