.section entry, "ax"
.globl _start
.type _start,@function
_start:
  mv s0,zero
  la sp,_stack_pointer
  .option push
  .option norelax
  la gp,__global_pointer$
  .option pop
#if SOC_TWO_STAGE
  la t0,__ssbl_load
  la t1,__ssbl_start
  la t2,__ssbl_end
9:bgeu t1,t2,10f
  lw a0,0(t0)
  sw a0,0(t1)
  addi t0,t0,4
  addi t1,t1,4
  j 9b
10:
  la t0,__ssbl_entry
  jr t0
.size _start,.-_start
.section .ssbl,"ax",@progbits
.balign 4
.globl __ssbl_entry
.type __ssbl_entry,@function
__ssbl_entry:
#endif
#if SOC_BOOT_WARM
  # Controlled bootstrap experiment: execute temporary NOP/RET instructions
  # at the final entry before replacing the same RAM bytes from Flash.
  la t0,_trm_init
  addi t1,t0,28
  li t2,0x00000013
11:sw t2,0(t0)
  addi t0,t0,4
  bltu t0,t1,11b
  li t2,0x00008067
  sw t2,0(t1)
  la t0,_trm_init
  jalr ra,t0,0
#endif
#if SOC_RELOCATE_TEXT
  la t0,__text_load
  la t1,__text_start
  la t2,__text_end
7:bgeu t1,t2,8f
  lw a0,0(t0)
  sw a0,0(t1)
  addi t0,t0,4
  addi t1,t1,4
  j 7b
8:
  la t0,__rodata_load
  la t1,__rodata_start
  la t2,__rodata_end
7:bgeu t1,t2,8f
  lw a0,0(t0)
  sw a0,0(t1)
  addi t0,t0,4
  addi t1,t1,4
  j 7b
8:
#endif
#if SOC_POISON_SRAM
  li t0,0x0f000000
  la t1,_heap_end
  li t2,0xa5a5a5a5
1:sw t2,0(t0)
  addi t0,t0,4
  bltu t0,t1,1b
#endif
#if SOC_BOOT_DATA
#if !SOC_SKIP_DATA
  la t0,__data_load
  la t1,__data_start
  la t2,__data_end
2:bgeu t1,t2,3f
  lw a0,0(t0)
  sw a0,0(t1)
  addi t0,t0,4
  addi t1,t1,4
  j 2b
3:
#endif
#if !SOC_SKIP_BSS
  la t0,__bss_start
  la t1,__bss_end
4:bgeu t0,t1,5f
  sw zero,0(t0)
  addi t0,t0,4
  j 4b
5:
#endif
#endif
#if SOC_RELOCATE_TEXT && SOC_BOOT_FENCE
  fence.i
#endif
  call _trm_init
6:j 6b
#if SOC_TWO_STAGE
.size __ssbl_entry,.-__ssbl_entry
#else
.size _start,.-_start
#endif
