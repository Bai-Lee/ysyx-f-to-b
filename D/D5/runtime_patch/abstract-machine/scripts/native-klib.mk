include $(AM_HOME)/scripts/native.mk
ARCH_H := arch/native.h
CFLAGS += -D__NATIVE_USE_KLIB__
