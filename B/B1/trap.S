#ifdef __riscv_e
#define NR_REGS 16
#else
#define NR_REGS 32
#endif
#define CONTEXT_SIZE ((NR_REGS+4)*4)
#define SAVE(n) sw x##n, (n*4)(sp)
#define RESTORE(n) lw x##n, (n*4)(sp)
.section .text.__am_asm_trap,"ax",@progbits
.balign 4
.globl __am_asm_trap
.type __am_asm_trap,@function
__am_asm_trap:
  addi sp,sp,-CONTEXT_SIZE
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
#ifndef __riscv_e
  SAVE(16)
  SAVE(17)
  SAVE(18)
  SAVE(19)
  SAVE(20)
  SAVE(21)
  SAVE(22)
  SAVE(23)
  SAVE(24)
  SAVE(25)
  SAVE(26)
  SAVE(27)
  SAVE(28)
  SAVE(29)
  SAVE(30)
  SAVE(31)
#endif
  addi t0,sp,CONTEXT_SIZE
  sw t0,8(sp)
  csrr t0,mcause
  sw t0,(NR_REGS*4)(sp)
  csrr t0,mstatus
  sw t0,((NR_REGS+1)*4)(sp)
  csrr t0,mepc
  sw t0,((NR_REGS+2)*4)(sp)
  sw zero,((NR_REGS+3)*4)(sp)
  mv a0,sp
  call __am_irq_handle
  mv sp,a0
  lw t0,((NR_REGS+1)*4)(sp)
  csrw mstatus,t0
  lw t0,((NR_REGS+2)*4)(sp)
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
#ifndef __riscv_e
  RESTORE(16)
  RESTORE(17)
  RESTORE(18)
  RESTORE(19)
  RESTORE(20)
  RESTORE(21)
  RESTORE(22)
  RESTORE(23)
  RESTORE(24)
  RESTORE(25)
  RESTORE(26)
  RESTORE(27)
  RESTORE(28)
  RESTORE(29)
  RESTORE(30)
  RESTORE(31)
#endif
  lw sp,8(sp)
  mret
.size __am_asm_trap,.-__am_asm_trap
