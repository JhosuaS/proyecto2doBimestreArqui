#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "disk_benchmark.h"
#include "cache_benchmark.h"

int main(int argc, char *argv[]) { 
    if(argc < 2) {
        printf("Uso: %s [disk|cache]\n", argv[0]);
        return EXIT_FAILURE;
    }
    
    if(strcmp(argv[1], "disk") == 0) {
        printf("Ejecutando benchmark de disco...\n");
        return run_disk_benchmark("test_files/test_file1.bin", 1024 * 1024 * 100, "results/disk_results.csv");
    } else if (strcmp(argv[1], "cache") == 0) {
        printf("Ejecutando benchmark de caché...\n");
        run_mem_cache_bench("results/cache_results.csv", 1024, 1024*1024*10, 2, 1000);
    } else {
        printf("Opción no válida: %s\n", argv[1]);
    }

    return EXIT_SUCCESS;
}