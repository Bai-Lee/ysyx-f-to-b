OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS { . = 0x80000000; .text : { KEEP(*(.text.start)) *(.text*) } .rodata : { *(.rodata*) } . = ALIGN(4); .data : { *(.data*) } .bss : { *(.bss*) *(COMMON) } /DISCARD/ : { *(.note*) *(.comment*) } }
