/* Preserve the C caller across assembly tests that intentionally clobber GPRs.
 * The tests' original halt relocation is redirected to batch_return only in
 * copied object files. Original test instructions and checks remain intact.
 */
.section .text.batch_call,"ax",@progbits
.global batch_call
batch_call:
  addi sp, sp, -32
  sw ra, 28(sp)
  sw s0, 24(sp)
  sw s1, 20(sp)
  sw gp, 16(sp)
  sw tp, 12(sp)
  lui t0, %hi(batch_saved_sp)
  sw sp, %lo(batch_saved_sp)(t0)
  jalr zero, a0, 0
.global batch_return
batch_return:
  lui t0, %hi(batch_saved_sp)
  lw sp, %lo(batch_saved_sp)(t0)
  lw ra, 28(sp)
  lw s0, 24(sp)
  lw s1, 20(sp)
  lw gp, 16(sp)
  lw tp, 12(sp)
  addi sp, sp, 32
  jalr zero, ra, 0
.section .bss.batch_context,"aw",@nobits
.align 2
batch_saved_sp:
  .zero 4
