.section .text.main,"ax",@progbits
.balign 32
.globl main
.type main,@function
main:
  addi sp,sp,-16
  sw ra,12(sp)
  sw s0,8(sp)
  la s0,target
  jalr ra,s0,0
  li t0,1
  bne a0,t0,fail
  li t0,0x00200513
  sw t0,0(s0)
#if WITH_FENCE
  fence.i
#endif
  jalr ra,s0,0
#if WITH_FENCE
  li t0,2
#else
  li t0,1
#endif
  bne a0,t0,fail
  li a0,0
  j done
fail:
  li a0,91
done:
  lw s0,8(sp)
  lw ra,12(sp)
  addi sp,sp,16
  ret
.size main,.-main
.balign 32
target:
  addi a0,zero,1
  ret
  .rept 6
  nop
  .endr
