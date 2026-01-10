#define _GNU_SOURCE
#define PAGE_SIZE 4096

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

void run_disk_benchmark(const char *filename, size_t file_size, const char *csv_filename) {
    void *mem_ptr = NULL;
    struct timespec start, end;
    double time_taken;
    
    FILE *f = fopen(csv_filename, "r");
    int write_header = 0;
    if (f == NULL) {
        write_header = 1;
    } else {
        fclose(f);
    }   

    f = fopen(csv_filename, "a");
    if(f) {
        if(write_header) {
            fprintf(f, "operacion,tamano_bytes,tiempo_seg,throughput_mbs\n");
            write_header = 0;
        }
    } else {
        perror("Error abriendo CSV");
        return;
    }
    
    if(posix_memalign(&mem_ptr, PAGE_SIZE, file_size) != 0) {
        printf("Error al asignar memoria alineada\n");
        return;
    }

    int fd = open(filename, O_WRONLY | O_CREAT | O_DIRECT, 0660);
    if(fd < 0) {
        printf("Error al abrir el archivo: %s\n", strerror(errno));
        free(mem_ptr);
        return;
    }

    memset(mem_ptr, '\0', file_size);
    clock_gettime(CLOCK_MONOTONIC, &start);
    write(fd, mem_ptr, file_size);
    clock_gettime(CLOCK_MONOTONIC, &end);

    time_taken = (end.tv_sec - start.tv_sec) + ((end.tv_nsec - start.tv_nsec) / 1000000000.0);
    fprintf(f, "write,%zu,%f,%f\n", file_size, time_taken, (file_size / (1024.0 * 1024.0)) / time_taken);
    
    fclose(f);
    close(fd);
    free(mem_ptr);

    return;
}
