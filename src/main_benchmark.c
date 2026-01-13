#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "disk_benchmark.h"
#include "cache_benchmark.h"

int main(int argc, char *argv[]) {

    if (argc < 2) {
        printf("Uso:\n");
        printf("  %s disk\n", argv[0]);
        printf("  %s cache\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (strcmp(argv[1], "disk") == 0) {
        printf("Ejecutando benchmark de disco...\n");

        int sizes_mb[] = {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000};
        int n = sizeof(sizes_mb) / sizeof(int);

        for (int i = 0; i < n; i++) {
            size_t size_bytes = sizes_mb[i] * 1024 * 1024;
            printf("  Tamaño: %d MB\n", sizes_mb[i]);
            run_disk_benchmark(
                "test_files/test_file1.bin",
                size_bytes,
                "results/disk_results.csv"
            );
        }

    } else if (strcmp(argv[1], "cache") == 0) {

        run_mem_cache_bench(
            "results/cache_results.csv",
            4 * 1024,
            64 * 1024 * 1024,
            2,
            64000000
        );

    } else {
        printf("Opción no válida\n");
    }

    return EXIT_SUCCESS;
}
