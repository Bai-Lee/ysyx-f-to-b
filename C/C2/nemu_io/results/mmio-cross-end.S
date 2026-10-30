.section .text
.globl _start
_start:
 lui t0,0xa1075
 addi t0,t0,0x2fe
 lw a0,0(t0)
 ebreak
