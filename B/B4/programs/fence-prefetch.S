.text
.balign 32
.globl main
main:
  addi sp,sp,-16
  sw ra,12(sp)
  call patcher
  li t0,2
  bne a0,t0,bad
  li a0,0
  j done
bad:
  li a0,202
done:
  lw ra,12(sp)
  addi sp,sp,16
  ret
.balign 32
patcher:
  la t0,patched_word
  li t1,0x00200513
  sw t1,0(t0)
  fence.i
.globl patched_word
patched_word:
  addi a0,zero,1
  ret
