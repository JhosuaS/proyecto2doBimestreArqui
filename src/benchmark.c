#define _GNU_SOURCE
#define PAGE_SIZE 4096
#define TEST_FILE_SIZE (1024 * 1024 *100)

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    void *mem_ptr = NULL;
    struct timespec start, end;
    double time_taken;

    if(posix_memalign(&mem_ptr, PAGE_SIZE, TEST_FILE_SIZE) != 0) {
        printf("Error al asignar memoria alineada\n");
        return EXIT_FAILURE;
    }

    int fd = open("test_files/test_file1.bin", O_WRONLY | O_CREAT | O_DIRECT, 0660);
    if(fd < 0) {
        printf("Error al abrir el archivo: %s\n", strerror(errno));
        free(mem_ptr);
        return EXIT_FAILURE;
    }

    memset(mem_ptr, '\0', TEST_FILE_SIZE);
    clock_gettime(CLOCK_MONOTONIC, &start);
    write(fd, mem_ptr, TEST_FILE_SIZE);
    clock_gettime(CLOCK_MONOTONIC, &end);

    time_taken = (end.tv_sec - start.tv_sec) + ((end.tv_nsec - start.tv_nsec) / 1000000000.0);
    printf("Tiempo tomado: %f segundos\n", time_taken);

    close(fd);
    free(mem_ptr);
    return 0;
}