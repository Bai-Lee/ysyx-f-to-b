.option norvc
.section .text.start,"ax"
.globl _start
.type _start,@function
_start:
  lui sp,0x80010
  addi t0,zero,5
  call outer
  ebreak
.size _start,.-_start
.section .text,"ax"
.type outer,@function
outer:
  addi sp,sp,-16
  sw ra,12(sp)
  li t0,42
  lui t1,0x80020
  sw t0,0(t1)
  lw t2,0(t1)
  call leaf
  lw ra,12(sp)
  addi sp,sp,16
  j tail
.size outer,.-outer
.type leaf,@function
leaf:
  addi t2,t2,1
  ret
.size leaf,.-leaf
.type tail,@function
tail:
  li a0,0
  ret
.size tail,.-tail
