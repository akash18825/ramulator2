#include <stdio.h>
#include <stdint.h>

#define N 16
#define BASE_A 0x10000000ULL
#define BASE_B 0x20000000ULL
#define BASE_C 0x30000000ULL

static inline uint64_t addr_A(int i, int k) {
    return BASE_A + ((uint64_t)(i * N + k) * sizeof(float));
}

static inline uint64_t addr_B(int k, int j) {
    return BASE_B + ((uint64_t)(k * N + j) * sizeof(float));
}

static inline uint64_t addr_C(int i, int j) {
    return BASE_C + ((uint64_t)(i * N + j) * sizeof(float));
}

int main() {
    FILE *f = fopen("ramulator_trace.txt", "w");
    if (!f) return 1;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                fprintf(f, "R 0x%lx\n", addr_A(i, k));
                fprintf(f, "R 0x%lx\n", addr_B(k, j));
            }
            fprintf(f, "W 0x%lx\n", addr_C(i, j));
        }
    }

    fclose(f);
    return 0;
}