ENTRY(_start)
MEMORY {
  mrom (rx) : ORIGIN = 0x20000000, LENGTH = 4K
  sram (rw) : ORIGIN = 0x0f000000, LENGTH = 8K
}
PHDRS { text PT_LOAD FLAGS(5); data PT_LOAD FLAGS(6); }
SECTIONS {
  .text : ALIGN(4) { KEEP(*(entry)) *(.text*) } > mrom :text
  .rodata : ALIGN(8) { *(.rodata*) *(.srodata*) } > mrom :text
  .data : ALIGN(8) {
    __data_start = .; *(.data*) *(.sdata*) . = ALIGN(8); __data_end = .;
  } > sram AT> mrom :data
  __data_load = LOADADDR(.data);
  .bss (NOLOAD) : ALIGN(8) {
    __bss_start = .; *(.bss*) *(.sbss*) *(COMMON) . = ALIGN(8); __bss_end = .;
  } > sram :data
  __global_pointer$ = __data_start + 0x800;
  _heap_start = ALIGN(__bss_end,16);
  _heap_end = ORIGIN(sram) + LENGTH(sram) - 2048;
  _stack_pointer = ORIGIN(sram) + LENGTH(sram);
  ASSERT(_heap_start <= _heap_end, "SRAM data/BSS overlaps reserved stack")
  ASSERT(__data_load + SIZEOF(.data) <= ORIGIN(mrom) + LENGTH(mrom), "MROM image exceeds4KiB")
  /DISCARD/ : { *(.eh_frame*) *(.comment*) *(.riscv.attributes) }
}
