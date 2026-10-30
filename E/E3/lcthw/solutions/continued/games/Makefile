CC=gcc
CFLAGS=-std=gnu17 -Wall -Werror -g -O0
.PHONY: all clean test
all: adventure walk
adventure: object.o actors.o map_adventure.o main_adventure.o
	$(CC) $(CFLAGS) $^ -o $@
walk: object.o actors.o map_walk.o main_walk.o
	$(CC) $(CFLAGS) $^ -o $@
%.o: %.c object.h game.h
	$(CC) $(CFLAGS) -c $< -o $@
test: all
	python3 test_games.py
clean:
	rm -f object.o actors.o map_adventure.o main_adventure.o map_walk.o main_walk.o adventure walk
