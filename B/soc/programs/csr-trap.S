.section .text.c5_test_trap,"ax",@progbits
.balign 4
.globl c5_test_trap
.type c5_test_trap,@function
c5_test_trap:
  csrr t0,mcause
  li t1,11
  bne t0,t1,1f
  csrr t0,mepc
  la t1,c5_ecall_site
  bne t0,t1,1f
  csrr t0,mstatus
  li t1,0x1880
  bne t0,t1,1f
  csrr t0,mepc
  addi t0,t0,4
  csrw mepc,t0
  li t2,123
  mret
1:
  li a0,62
  ebreak
  j 1b
.size c5_test_trap,.-c5_test_trap
