CC=gcc
CFLAGS=-std=gnu17 -Wall -g -O0
.PHONY: all clean
all: scopes
scopes: ex22.o ex22_main.o
	$(CC) $^ -o $@
%.o: %.c ex22.h dbg.h
	$(CC) $(CFLAGS) -c $< -o $@
clean:
	rm -f ex22.o ex22_main.o scopes
