#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "fetch.h"

void FETCH_DATA(uint8_t *buffer, size_t size) {
	uint64_t v = SECRET;
    write(CHILD, &v, 8);
    read(CHILD, (void *)buffer, size);
}