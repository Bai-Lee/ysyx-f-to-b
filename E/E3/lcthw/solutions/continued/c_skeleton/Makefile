CC=gcc
CFLAGS=-std=gnu17 -g -O2 -Wall -Wextra -Isrc -fPIC
LIBNAME?=starter
SOURCES=$(wildcard src/*.c)
OBJECTS=$(SOURCES:.c=.o)
TEST_SRC=$(wildcard tests/*_tests.c)
TESTS=$(TEST_SRC:.c=)
TARGET=build/lib$(LIBNAME).a
SHARED=build/lib$(LIBNAME).so
.PHONY: all tests test clean check
all: $(TARGET) $(SHARED) tests
build:
	mkdir -p build
$(TARGET): $(OBJECTS) | build
	ar rcs $@ $(OBJECTS)
$(SHARED): $(OBJECTS) | build
	$(CC) -shared $^ -o $@
tests/%_tests: tests/%_tests.c $(TARGET) $(SHARED)
	$(CC) $(CFLAGS) $< $(TARGET) -ldl -o $@
tests test: $(TESTS)
	sh tests/runtests.sh
clean:
	rm -f $(OBJECTS) $(TESTS) $(TARGET) $(SHARED) tests/tests.log
BADFUNCS='[^_.>a-zA-Z0-9](str(n?cpy|n?cat|xfrm|n?dup|str|pbrk|tok|_)|stpn?cpy|a?sn?printf|byte_)'
check:
	@grep -En $(BADFUNCS) $(SOURCES) || true
