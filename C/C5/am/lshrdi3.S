.section .text.__lshrdi3,"ax",@progbits
.globl __lshrdi3
.type __lshrdi3,@function
__lshrdi3:
  beqz a2,3f
  li t0,64
  bgeu a2,t0,2f
  li t0,32
  bltu a2,t0,1f
  addi a2,a2,-32
  srl a0,a1,a2
  li a1,0
  ret
1:
  sub t0,t0,a2
  sll t1,a1,t0
  srl a0,a0,a2
  or a0,a0,t1
  srl a1,a1,a2
  ret
2:
  li a0,0
  li a1,0
3:
  ret
.size __lshrdi3,.-__lshrdi3
