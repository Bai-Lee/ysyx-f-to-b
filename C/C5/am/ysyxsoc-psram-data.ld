ENTRY(_start)
MEMORY {
  flash (rx) : ORIGIN  =  0x30000000, LENGTH  =  16M
  sram (rw) : ORIGIN  =  0x0f000000, LENGTH  =  8K
  psram (rwx) : ORIGIN  =  0x80000000, LENGTH  =  4M
}
PHDRS { text PT_LOAD FLAGS(5); data PT_LOAD FLAGS(6); }
SECTIONS {
  .text : ALIGN(4) { KEEP(*(entry)) *(.text*) } > flash :text
  .rodata : ALIGN(8) { *(.rodata*) *(.srodata*) } > flash :text
  .data : ALIGN(8) { __data_start = .; *(.data*) *(.sdata*) .  =  ALIGN(8); __data_end = .; } > psram AT> flash :data
  __data_load = LOADADDR(.data);
  .bss (NOLOAD) : ALIGN(8) { __bss_start = .; *(.bss*) *(.sbss*) *(COMMON) .  =  ALIGN(8); __bss_end = .; } > psram :data
  __global_pointer$ = __data_start+0x800;
  _heap_start = ALIGN(__bss_end,16);_heap_end = ORIGIN(psram)+LENGTH(psram);
  _stack_pointer = ORIGIN(sram)+LENGTH(sram);
  ASSERT(_heap_start<_heap_end,"PSRAM data/BSS exceeds4MiB")
  ASSERT(__data_load+SIZEOF(.data)<=ORIGIN(flash)+LENGTH(flash),"Flash image exceeds16MiB")
  /DISCARD/ : { *(.eh_frame*) *(.comment*) *(.riscv.attributes) }
}
