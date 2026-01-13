CC = gcc
CFLAGS = -Wall -O0 
TARGET = src/benchmark
SRC = src/disk_benchmark.c \
	  src/cache_benchmark.c \
	  src/main_benchmark.c

all: directories $(TARGET)

.PHONY: directories
directories:
	mkdir -p test_files
	mkdir -p results

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET) *.o
