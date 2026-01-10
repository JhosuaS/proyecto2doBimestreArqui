#define _GNU_SOURCE
#define CACHELINE 64

#include "cache_benchmark.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>



static inline uint64_t tiempo_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + ts.tv_nsec;
}

static volatile uint64_t resultado_dummy = 0;

static void *reservar_memoria(size_t bytes) {
    void *ptr = NULL;
    if (posix_memalign(&ptr, CACHELINE, bytes) != 0) {
        return NULL;
    }
    return ptr;
}

static void llenar_arreglo(uint32_t *arr, size_t n) {
    for (size_t i = 0; i < n; i++) {
        arr[i] = (uint32_t)i;
    }
}

static double acceso_secuencial(uint32_t *arr, size_t n, size_t iteraciones) {
    uint64_t suma = 0;
    size_t indice = 0;

    uint64_t inicio = tiempo_ns();
    for (size_t i = 0; i < iteraciones; i++) {
        suma += arr[indice];
        indice++;
        if (indice == n) indice = 0;
    }
    uint64_t fin = tiempo_ns();

    resultado_dummy = suma;

    return (double)(fin - inicio) / iteraciones;
}

static double acceso_con_saltos(uint32_t *arr, size_t n,
                                size_t iteraciones, size_t salto) {
    uint64_t suma = 0;
    size_t indice = 0;

    uint64_t inicio = tiempo_ns();
    for (size_t i = 0; i < iteraciones; i++) {
        suma += arr[indice];
        indice += salto;
        if (indice >= n) indice %= n;
    }
    uint64_t fin = tiempo_ns();

    resultado_dummy = suma;
    return (double)(fin - inicio) / iteraciones;
}

void run_mem_cache_bench(const char *archivo_csv,
                         size_t min_bytes,
                         size_t max_bytes,
                         size_t factor,
                         size_t accesos) {

    FILE *f = fopen(archivo_csv, "w");
    if (!f) {
        perror("Error creando CSV");
        return;
    }

    fprintf(f, "tipo,patron,tamano_bytes,salto_bytes,ns_por_acceso\n");

    size_t salto_bytes = 4096;
    size_t salto_elementos = salto_bytes / sizeof(uint32_t);

    for (size_t bytes = min_bytes; bytes <= max_bytes; bytes *= factor) {

        size_t n = bytes / sizeof(uint32_t);
        if (n < 1024) n = 1024;

        uint32_t *arreglo = reservar_memoria(n * sizeof(uint32_t));
        if (!arreglo) break;

        llenar_arreglo(arreglo, n);

        double t_seq = acceso_secuencial(arreglo, n, accesos);

        double t_salto = acceso_con_saltos(arreglo, n, accesos, salto_elementos);

        fprintf(f, "mem,secuencial,%zu,0,%.3f\n", bytes, t_seq);
        fprintf(f, "mem,saltos,%zu,%zu,%.3f\n", bytes, salto_bytes, t_salto);

        printf("TAM %7zu KB | Secuencial: %6.2f ns | Saltos: %6.2f ns\n",
               bytes / 1024, t_seq, t_salto);

        free(arreglo);
    }

    fclose(f);
}
