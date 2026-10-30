SOC_CLOCK_MHZ ?= 400
SOC_UART_MODE := 2
SOC_UART_DIV := 1
SOC_PRINT_ID ?= 0
AM_SRCS := riscv/bnpc/start.S riscv/bnpc/trm.c riscv/bnpc/ioe.c riscv/bnpc/lshrdi3.S \
           riscv/bnpc/cte.c riscv/bnpc/trap.S platform/dummy/vme.c platform/dummy/mpe.c
CFLAGS += -Os -ffunction-sections -fdata-sections -DSOC_UART_MODE=$(SOC_UART_MODE) -DSOC_UART_DIV=$(SOC_UART_DIV) -DSOC_PRINT_ID=$(SOC_PRINT_ID) -DSOC_CLOCK_MHZ=$(SOC_CLOCK_MHZ)
LDSCRIPTS += $(AM_HOME)/scripts/bnpc.ld
LDFLAGS += --gc-sections -e _start --no-relax
MAINARGS_MAX_LEN = 64
MAINARGS_PLACEHOLDER = the_insert-arg_rule_in_Makefile_will_insert_mainargs_here
CFLAGS += -DMAINARGS_MAX_LEN=$(MAINARGS_MAX_LEN) -DMAINARGS_PLACEHOLDER=$(MAINARGS_PLACEHOLDER)
image: image-dep
	@$(OBJDUMP) -d $(IMAGE).elf > $(IMAGE).txt
	@$(OBJCOPY) -S -O binary $(IMAGE).elf $(IMAGE).bin
insert-arg: image
	@python $(AM_HOME)/tools/insert-arg.py $(IMAGE).bin $(MAINARGS_MAX_LEN) $(MAINARGS_PLACEHOLDER) "$(mainargs)"
.PHONY: insert-arg
