NAME = amtest
SRCS = $(shell find src/ -name "*.[cS]")
SRCS += /workspace/projects/ysyx_f_to_b/C/C2/timer_trm_only.c
include $(AM_HOME)/Makefile
