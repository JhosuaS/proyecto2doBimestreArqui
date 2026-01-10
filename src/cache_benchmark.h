#ifndef CACHE_BENCHMARK_H
#define CACHE_BENCHMARK_H

#include <stddef.h>

void run_mem_cache_bench(const char *archivo_csv,
                         size_t min_bytes,
                         size_t max_bytes,
                         size_t factor,
                         size_t accesos);

#endif
