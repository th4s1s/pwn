#include <pthread.h>
#include <stdarg.h>
#ifdef __clang__
#include <stdatomic.h>
#endif
#include <stdbool.h>
#include <stdint.h>
#include <time.h>

/* Atomics */
#define ATOMIC_GET(x) __atomic_load_n(&(x), __ATOMIC_RELAXED)
#define ATOMIC_SET(x, y) __atomic_store_n(&(x), y, __ATOMIC_RELAXED)
#define ATOMIC_CLEAR(x) __atomic_store_n(&(x), 0, __ATOMIC_RELAXED)
#define ATOMIC_XCHG(x, y) __atomic_exchange_n(&(x), y, __ATOMIC_RELAXED)

#define ATOMIC_PRE_INC(x) __atomic_add_fetch(&(x), 1, __ATOMIC_RELAXED)
#define ATOMIC_POST_INC(x) __atomic_fetch_add(&(x), 1, __ATOMIC_RELAXED)

#define ATOMIC_PRE_DEC(x) __atomic_sub_fetch(&(x), 1, __ATOMIC_RELAXED)
#define ATOMIC_POST_DEC(x) __atomic_fetch_sub(&(x), 1, __ATOMIC_RELAXED)

#define ATOMIC_PRE_ADD(x, y) __atomic_add_fetch(&(x), y, __ATOMIC_RELAXED)
#define ATOMIC_POST_ADD(x, y) __atomic_fetch_add(&(x), y, __ATOMIC_RELAXED)

#define ATOMIC_PRE_SUB(x, y) __atomic_sub_fetch(&(x), y, __ATOMIC_RELAXED)
#define ATOMIC_POST_SUB(x, y) __atomic_fetch_sub(&(x), y, __ATOMIC_RELAXED)

#define ATOMIC_PRE_AND(x, y) __atomic_and_fetch(&(x), y, __ATOMIC_RELAXED)
#define ATOMIC_POST_AND(x, y) __atomic_fetch_and(&(x), y, __ATOMIC_RELAXED)

#define ATOMIC_PRE_OR(x, y) __atomic_or_fetch(&(x), y, __ATOMIC_RELAXED)
#define ATOMIC_POST_OR(x, y) __atomic_fetch_or(&(x), y, __ATOMIC_RELAXED)

#define ATOMIC_PRE_INC_RELAXED(x) __atomic_add_fetch(&(x), 1, __ATOMIC_RELAXED)
#define ATOMIC_POST_OR_RELAXED(x, y) __atomic_fetch_or(&(x), y, __ATOMIC_RELAXED)

__attribute__((always_inline)) static inline uint8_t ATOMIC_BTS(uint8_t* addr, size_t offset) {
    uint8_t oldbit;
    addr += (offset / 8);
    oldbit = ATOMIC_POST_OR_RELAXED(*addr, ((uint8_t)1U << (offset % 8)));
    return oldbit;
}

#define _COV_BITMAP_MAX_SIZE (4096U)

typedef struct {
    bool pcGuardMap[_COV_BITMAP_MAX_SIZE];
    uint8_t bbMapPc[_COV_BITMAP_MAX_SIZE];
    uint8_t bbMapEdge[_COV_BITMAP_MAX_SIZE];
} feedback_t;

typedef struct {
	int sv[2];
	int dsv[2];
	pid_t pid;
	uint64_t cov;
	uint64_t numPatchPoints;
	uint64_t *patchPoints;
	char *filename;
	void *binary_addr;
	char *report;
	void *shadow_addr;
	feedback_t *bbMap;
	feedback_t feedback;
	int InputFd;
	uint64_t limit;
	uint8_t *InputBuffer;
} run_t;

uint64_t find_base_address(uint64_t addr);
void trapFuzzInstall(run_t *client);





