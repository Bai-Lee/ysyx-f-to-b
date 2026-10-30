/* C5 long memory-test loops: eight explicit accesses per group.
 * Same address/inverse patterns and width ordering as mem-sweep.c.
 * This code still executes on the RTL CPU and is checked instruction-by-instruction.
 */
.section .text.c5_sweeps,"ax",@progbits
.balign 4
.globl c5_sweep8
.type c5_sweep8,@function
c5_sweep8:
  addi sp,sp,-16
  sw s0,0(sp)
  mv s0,a0
  neg a4,a2
  li t2,1
  beqz a2,.Lstep8
  neg t2,t2
.Lstep8:
  xor t1,s0,a4
.Lwrite8:
  sb t1,0(a0)
  add t1,t1,t2
  sb t1,1(a0)
  add t1,t1,t2
  sb t1,2(a0)
  add t1,t1,t2
  sb t1,3(a0)
  add t1,t1,t2
  sb t1,4(a0)
  add t1,t1,t2
  sb t1,5(a0)
  add t1,t1,t2
  sb t1,6(a0)
  add t1,t1,t2
  sb t1,7(a0)
  add t1,t1,t2
  addi a0,a0,8
  bltu a0,a1,.Lwrite8
  beqz a3,.Lreadsetup8
  lbu t0,0(s0)
  xori t0,t0,1
  sb t0,0(s0)
.Lreadsetup8:
  mv a0,s0
  xor t1,s0,a4
  andi t1,t1,255
.Lread8:
  lbu t0,0(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,1(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,2(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,3(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,4(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,5(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,6(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  lbu t0,7(a0)
  bne t0,t1,.Lbad8
  add t1,t1,t2
  andi t1,t1,255
  addi a0,a0,8
  bltu a0,a1,.Lread8
  li a0,0
  j .Ldone8
.Lbad8:
  li a0,1
.Ldone8:
  lw s0,0(sp)
  addi sp,sp,16
  ret
.size c5_sweep8,.-c5_sweep8
.balign 4
.globl c5_sweep16
.type c5_sweep16,@function
c5_sweep16:
  addi sp,sp,-16
  sw s0,0(sp)
  mv s0,a0
  neg a4,a2
  li t2,2
  beqz a2,.Lstep16
  neg t2,t2
.Lstep16:
  xor t1,s0,a4
.Lwrite16:
  sh t1,0(a0)
  add t1,t1,t2
  sh t1,2(a0)
  add t1,t1,t2
  sh t1,4(a0)
  add t1,t1,t2
  sh t1,6(a0)
  add t1,t1,t2
  sh t1,8(a0)
  add t1,t1,t2
  sh t1,10(a0)
  add t1,t1,t2
  sh t1,12(a0)
  add t1,t1,t2
  sh t1,14(a0)
  add t1,t1,t2
  addi a0,a0,16
  bltu a0,a1,.Lwrite16
  beqz a3,.Lreadsetup16
  lbu t0,0(s0)
  xori t0,t0,1
  sb t0,0(s0)
.Lreadsetup16:
  mv a0,s0
  xor t1,s0,a4
  slli t1,t1,16
  srli t1,t1,16
.Lread16:
  lhu t0,0(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,2(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,4(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,6(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,8(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,10(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,12(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  lhu t0,14(a0)
  bne t0,t1,.Lbad16
  add t1,t1,t2
  slli t1,t1,16
  srli t1,t1,16
  addi a0,a0,16
  bltu a0,a1,.Lread16
  li a0,0
  j .Ldone16
.Lbad16:
  li a0,1
.Ldone16:
  lw s0,0(sp)
  addi sp,sp,16
  ret
.size c5_sweep16,.-c5_sweep16
.balign 4
.globl c5_sweep32
.type c5_sweep32,@function
c5_sweep32:
  addi sp,sp,-16
  sw s0,0(sp)
  mv s0,a0
  neg a4,a2
  li t2,4
  beqz a2,.Lstep32
  neg t2,t2
.Lstep32:
  xor t1,s0,a4
.Lwrite32:
  sw t1,0(a0)
  add t1,t1,t2
  sw t1,4(a0)
  add t1,t1,t2
  sw t1,8(a0)
  add t1,t1,t2
  sw t1,12(a0)
  add t1,t1,t2
  sw t1,16(a0)
  add t1,t1,t2
  sw t1,20(a0)
  add t1,t1,t2
  sw t1,24(a0)
  add t1,t1,t2
  sw t1,28(a0)
  add t1,t1,t2
  addi a0,a0,32
  bltu a0,a1,.Lwrite32
  beqz a3,.Lreadsetup32
  lbu t0,0(s0)
  xori t0,t0,1
  sb t0,0(s0)
.Lreadsetup32:
  mv a0,s0
  xor t1,s0,a4
.Lread32:
  lw t0,0(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,4(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,8(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,12(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,16(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,20(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,24(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  lw t0,28(a0)
  bne t0,t1,.Lbad32
  add t1,t1,t2
  addi a0,a0,32
  bltu a0,a1,.Lread32
  li a0,0
  j .Ldone32
.Lbad32:
  li a0,1
.Ldone32:
  lw s0,0(sp)
  addi sp,sp,16
  ret
.size c5_sweep32,.-c5_sweep32
.balign 4
.globl c5_sweep64
.type c5_sweep64,@function
c5_sweep64:
  addi sp,sp,-16
  sw s0,0(sp)
  mv s0,a0
  neg a4,a2
  li t2,8
  beqz a2,.Lstep64
  neg t2,t2
.Lstep64:
  xor t1,s0,a4
.Lwrite64:
  sw t1,0(a0)
  sw a4,4(a0)
  add t1,t1,t2
  sw t1,8(a0)
  sw a4,12(a0)
  add t1,t1,t2
  sw t1,16(a0)
  sw a4,20(a0)
  add t1,t1,t2
  sw t1,24(a0)
  sw a4,28(a0)
  add t1,t1,t2
  sw t1,32(a0)
  sw a4,36(a0)
  add t1,t1,t2
  sw t1,40(a0)
  sw a4,44(a0)
  add t1,t1,t2
  sw t1,48(a0)
  sw a4,52(a0)
  add t1,t1,t2
  sw t1,56(a0)
  sw a4,60(a0)
  add t1,t1,t2
  addi a0,a0,64
  bltu a0,a1,.Lwrite64
  beqz a3,.Lreadsetup64
  lbu t0,0(s0)
  xori t0,t0,1
  sb t0,0(s0)
.Lreadsetup64:
  mv a0,s0
  xor t1,s0,a4
.Lread64:
  lw t0,0(a0)
  bne t0,t1,.Lbad64
  lw t0,4(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,8(a0)
  bne t0,t1,.Lbad64
  lw t0,12(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,16(a0)
  bne t0,t1,.Lbad64
  lw t0,20(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,24(a0)
  bne t0,t1,.Lbad64
  lw t0,28(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,32(a0)
  bne t0,t1,.Lbad64
  lw t0,36(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,40(a0)
  bne t0,t1,.Lbad64
  lw t0,44(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,48(a0)
  bne t0,t1,.Lbad64
  lw t0,52(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  lw t0,56(a0)
  bne t0,t1,.Lbad64
  lw t0,60(a0)
  bne t0,a4,.Lbad64
  add t1,t1,t2
  addi a0,a0,64
  bltu a0,a1,.Lread64
  li a0,0
  j .Ldone64
.Lbad64:
  li a0,1
.Ldone64:
  lw s0,0(sp)
  addi sp,sp,16
  ret
.size c5_sweep64,.-c5_sweep64
