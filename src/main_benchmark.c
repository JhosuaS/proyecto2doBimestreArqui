#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "disk_benchmark.h"
#include "cache_benchmark.h"

int main(int argc, char *argv[]) {

    if (argc < 3) {
        printf("Uso:\n");
        printf("Uso: %s [disk size_file|\n"
               "         cache min_bytes max_bytes factor accesos]\n", argv[0]);
        return EXIT_FAILURE;
        }

    if (strcmp(argv[1], "disk") == 0) {
        printf("Ejecutando benchmark de disco...\n");

        if(argc != 3) {
            printf("Uso: %s disk size_file\n", argv[0]);
            return EXIT_FAILURE;
        } else if (atoi(argv[2]) <= 0) {
            printf("El tamaño del archivo debe ser un entero positivo.\n");
            return EXIT_FAILURE;
        }else {
            printf("Ejecutando benchmark de disco...\n");
            int size_file = atoi(argv[2]);
            run_disk_benchmark("test_files/test_file1.bin", size_file, "results/disk_results.csv");
        }

    } else if (strcmp(argv[1], "cache") == 0) {
        
        printf("Ejecutando benchmark de caché...\n");

        if(argc !=6) {
            printf("Uso: %s cache min_bytes max_bytes factor accesos\n", argv[0]);
            return EXIT_FAILURE;
        } else if (atoi(argv[2]) <= 0 || atoi(argv[3]) <= 0 || atoi(argv[4]) <= 1 || atoi(argv[5]) <= 0) {
            printf("Todos los parámetross deben ser enteros positivos, con factor mayor a 1.\n");
            return EXIT_FAILURE;
        }else {
            printf("Ejecutando benchmark de caché...\n");
            run_mem_cache_bench("results/cache_results.csv", atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]));
        }

    } else {
        printf("Opción no válida: %s\n", argv[1]);
    }

    return EXIT_SUCCESS;
}
