SOC_BOOT_DATA ?= 1
SOC_UART_MODE ?= 2
SOC_UART_DIV ?= 1
SOC_POISON_SRAM ?= 0
SOC_SKIP_DATA ?= 0
SOC_SKIP_BSS ?= 0
SOC_FLASH_BOOT ?= 0
SOC_PRINT_ID ?= 0
SOC_PSRAM_DATA ?= 0
SOC_RELOCATE_TEXT ?= 0
SOC_CODE_SRAM ?= 0
SOC_TWO_STAGE ?= 0
SOC_CODE_SDRAM ?= 0
SOC_SDRAM_MB ?= 32
SOC_CLOCK_MHZ ?= 100
SOC_BOOT_WARM ?= 0
SOC_BOOT_FENCE ?= 1
AM_SRCS := riscv/ysyxsoc/start.S riscv/ysyxsoc/trm.c riscv/ysyxsoc/ioe.c riscv/ysyxsoc/lshrdi3.S \
           riscv/ysyxsoc/cte.c riscv/ysyxsoc/trap.S \
           platform/dummy/vme.c platform/dummy/mpe.c
CFLAGS += -Os -ffunction-sections -fdata-sections -DSOC_UART_MODE=$(SOC_UART_MODE) -DSOC_UART_DIV=$(SOC_UART_DIV) -DSOC_PRINT_ID=$(SOC_PRINT_ID) -DSOC_CLOCK_MHZ=$(SOC_CLOCK_MHZ)
ASFLAGS += -DSOC_BOOT_DATA=$(SOC_BOOT_DATA) -DSOC_POISON_SRAM=$(SOC_POISON_SRAM) -DSOC_SKIP_DATA=$(SOC_SKIP_DATA) -DSOC_SKIP_BSS=$(SOC_SKIP_BSS) -DSOC_RELOCATE_TEXT=$(SOC_RELOCATE_TEXT) -DSOC_TWO_STAGE=$(SOC_TWO_STAGE) -DSOC_BOOT_WARM=$(SOC_BOOT_WARM) -DSOC_BOOT_FENCE=$(SOC_BOOT_FENCE)
ifeq ($(SOC_CODE_SDRAM),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-code-sdram$(SOC_SDRAM_MB).ld
else ifeq ($(SOC_CODE_SRAM),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-code-sram.ld
else ifeq ($(SOC_RELOCATE_TEXT),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-code-psram.ld
else ifeq ($(SOC_PSRAM_DATA),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-psram-data.ld
else ifeq ($(SOC_FLASH_BOOT),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-flash.ld
else ifeq ($(SOC_BOOT_DATA),1)
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-mrom.ld
else
LDSCRIPTS += $(AM_HOME)/scripts/ysyxsoc-initial.ld
endif
LDFLAGS += --gc-sections -e _start --no-relax
MAINARGS_MAX_LEN = 64
MAINARGS_PLACEHOLDER = the_insert-arg_rule_in_Makefile_will_insert_mainargs_here
CFLAGS += -DMAINARGS_MAX_LEN=$(MAINARGS_MAX_LEN) -DMAINARGS_PLACEHOLDER=$(MAINARGS_PLACEHOLDER)
image: image-dep
	@$(OBJDUMP) -d $(IMAGE).elf > $(IMAGE).txt
	@$(OBJCOPY) -S -O binary $(IMAGE).elf $(IMAGE).bin
insert-arg: image
	@python $(AM_HOME)/tools/insert-arg.py $(IMAGE).bin $(MAINARGS_MAX_LEN) $(MAINARGS_PLACEHOLDER) "$(mainargs)"
run: insert-arg
	$(MAKE) -s -C $(NPC_HOME) sim IMAGE="$(IMAGE).bin" ELF="$(IMAGE).elf" NPC_ARGS="$(NPC_ARGS)"
.PHONY: insert-arg
