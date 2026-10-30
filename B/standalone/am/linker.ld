ENTRY(_start)
MEMORY { ram (rwx) : ORIGIN = 0x80000000, LENGTH = 128M }
PHDRS { text PT_LOAD FLAGS(5); data PT_LOAD FLAGS(6); }
SECTIONS {
  .text : ALIGN(16) { KEEP(*(entry)) *(.text*) } > ram :text
  .rodata : ALIGN(16) { *(.rodata*) *(.srodata*) } > ram :text
  .data : ALIGN(16) {
    __data_start = .; *(.data*) *(.sdata*) . = ALIGN(8);
    __fsymtab_start = .; KEEP(*(FSymTab)) __fsymtab_end = .; . = ALIGN(8);
    __vsymtab_start = .; KEEP(*(VSymTab)) __vsymtab_end = .; . = ALIGN(8);
    __rt_init_start = .; KEEP(*(SORT(.rti_fn*))) __rt_init_end = .; . = ALIGN(8);
    __rt_utest_tc_tab_start = .; KEEP(*(UtestTcTab)) __rt_utest_tc_tab_end = .; . = ALIGN(8);
    __am_apps_data_start = .; *(__am_apps.data*) *(__am_apps.sdata*) __am_apps_data_end = .;
  } > ram :data
  .bss (NOLOAD) : ALIGN(16) {
    __bss_start = .; *(.bss*) *(.sbss*) *(COMMON)
    __am_apps_bss_start = .; *(__am_apps.bss*) *(__am_apps.sbss*) *(__am_apps.scommon*) __am_apps_bss_end = .;
    . = ALIGN(16); __bss_end = .;
  } > ram :data
  __global_pointer$ = __data_start+0x800;
  _heap_start = ALIGN(__bss_end,16); _heap_end = 0x87ff0000; _stack_pointer = 0x88000000;
  ASSERT(__bss_end<_heap_end,"Fast program exceeds RAM")
  /DISCARD/ : { *(.eh_frame*) *(.comment*) *(.riscv.attributes) }
}
