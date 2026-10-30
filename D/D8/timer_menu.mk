NAME = amtest
SRCS = $(shell find src/ -name "*.[cS]")
SRCS += /workspace/projects/ysyx_f_to_b/D/D8/timer_trm_only.c
include $(AM_HOME)/Makefile
