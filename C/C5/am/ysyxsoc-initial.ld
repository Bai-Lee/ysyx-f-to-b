ENTRY(_start)
MEMORY {
  mrom (rx) : ORIGIN = 0x20000000, LENGTH = 4K
  sram (rw) : ORIGIN = 0x0f000000, LENGTH = 8K
}
SECTIONS {
  .text : ALIGN(4) { KEEP(*(entry)) *(.text*) } > mrom
  .rodata : ALIGN(8) { *(.rodata*) *(.srodata*) } > mrom
  .data : ALIGN(8) { __data_start = .; *(.data*) *(.sdata*) __data_end = .; } > mrom
  .bss (NOLOAD) : ALIGN(8) { __bss_start = .; *(.bss*) *(.sbss*) *(COMMON) __bss_end = .; } > mrom
  __data_load = LOADADDR(.data);
  __global_pointer$ = __data_start + 0x800;
  _heap_start = ORIGIN(sram);
  _heap_end = ORIGIN(sram) + LENGTH(sram) - 2048;
  _stack_pointer = ORIGIN(sram) + LENGTH(sram);
  /DISCARD/ : { *(.eh_frame*) *(.comment*) *(.riscv.attributes) }
}
