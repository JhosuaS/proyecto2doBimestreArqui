CC = gcc
CFLAGS = -Wall -O0 # O0 para que el compilador no optimice nuestros bucles de prueba
TARGET = src/benchmark
SRC = src/benchmark.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET) *.o