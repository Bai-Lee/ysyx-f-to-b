#ifndef __riscv_e
#error C5 trap entry currently supports RV32E only
#endif
#define SAVE(n) sw x##n, (n*4)(sp)
#define RESTORE(n) lw x##n, (n*4)(sp)
.section .text.__am_asm_trap,"ax",@progbits
.balign 4
.globl __am_asm_trap
.type __am_asm_trap,@function
__am_asm_trap:
  addi sp,sp,-80
  sw zero,0(sp)
  SAVE(1)
  SAVE(3)
  SAVE(4)
  SAVE(5)
  SAVE(6)
  SAVE(7)
  SAVE(8)
  SAVE(9)
  SAVE(10)
  SAVE(11)
  SAVE(12)
  SAVE(13)
  SAVE(14)
  SAVE(15)
  addi t0,sp,80
  sw t0,8(sp)
  csrr t0,mcause
  sw t0,64(sp)
  csrr t0,mstatus
  sw t0,68(sp)
  csrr t0,mepc
  sw t0,72(sp)
  sw zero,76(sp)
  mv a0,sp
  call __am_irq_handle
  mv sp,a0
  lw t0,68(sp)
  csrw mstatus,t0
  lw t0,72(sp)
  csrw mepc,t0
  RESTORE(1)
  RESTORE(3)
  RESTORE(4)
  RESTORE(5)
  RESTORE(6)
  RESTORE(7)
  RESTORE(8)
  RESTORE(9)
  RESTORE(10)
  RESTORE(11)
  RESTORE(12)
  RESTORE(13)
  RESTORE(14)
  RESTORE(15)
  lw sp,8(sp)
  mret
.size __am_asm_trap,.-__am_asm_trap
