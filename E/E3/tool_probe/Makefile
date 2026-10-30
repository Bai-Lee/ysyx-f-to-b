CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -Werror -O0 -g
SOURCE_ROOT = /workspace/projects/ysyx_f_to_b

all: good bad_memory

good: $(SOURCE_ROOT)/E/E2/linked_list.c
	$(CC) $(CFLAGS) $< -o $@

bad_memory: $(SOURCE_ROOT)/E/E3/tool_probe/bad_memory.c
	$(CC) $(CFLAGS) $< -o $@

.PHONY: all
