	.file	"z3.c"
 # GNU C17 (Rev13, Built by MSYS2 project) version 15.2.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 15.2.0, GMP version 6.3.0, MPFR version 4.2.2, MPC version 1.3.1, isl version isl-0.27-GMP

 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: -mtune=generic -march=nocona -g -O0 -std=c17
	.text
.Ltext0:
	.cfi_sections	.debug_frame
	.file 0 "/workspace/projects/ysyx_f_to_b" "/workspace/projects/ysyx_f_to_b/F/programs/z3.c"
	.section .rdata,"dr"
.LC0:
	.ascii "z = %d\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
.LFB101:
	.file 1 "/workspace/projects/ysyx_f_to_b/F/programs/z3.c"
	.loc 1 2 16
	.cfi_startproc
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp	 #,
	.seh_setframe	%rbp, 0
	.cfi_def_cfa_register 6
	subq	$48, %rsp	 #,
	.seh_stackalloc	48
	.seh_endprologue
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:2: int main(void) {
	.loc 1 2 16
	call	__main	 #
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:3:   int x=1;
	.loc 1 3 7
	movl	$1, -4(%rbp)	 #, x
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:4:   int y=2;
	.loc 1 4 7
	movl	$2, -8(%rbp)	 #, y
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:5:   int z=x+y;
	.loc 1 5 7
	movl	-4(%rbp), %edx	 # x, tmp104
	movl	-8(%rbp), %eax	 # y, tmp105
	addl	%edx, %eax	 # tmp104, z_3
	movl	%eax, -12(%rbp)	 # z_3, z
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:6:   printf("z = %d\n",z);
	.loc 1 6 3
	movl	-12(%rbp), %eax	 # z, tmp106
	leaq	.LC0(%rip), %rcx	 #, tmp107
	movl	%eax, %edx	 # tmp106,
	call	printf	 #
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:7:   return 0;
	.loc 1 7 10
	movl	$0, %eax	 #, _6
 # C:\YSYX_WORKSPACE\projects\ysyx_f_to_b\F\programs\z3.c:8: }
	.loc 1 8 1
	addq	$48, %rsp	 #,
	popq	%rbp	 #
	.cfi_restore 6
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE101:
	.seh_endproc
.Letext0:
	.file 2 "D:/msys64/ucrt64/include/stdio.h"
	.section	.debug_info,"dr"
.Ldebug_info0:
	.long	0x13b
	.word	0x5
	.byte	0x1
	.byte	0x8
	.secrel32	.Ldebug_abbrev0
	.uleb128 0x3
	.ascii "GNU C17 15.2.0 -mtune=generic -march=nocona -g -O0 -std=c17\0"
	.byte	0x1d
	.byte	0x3
	.long	0x313ee
	.secrel32	.LASF0
	.secrel32	.LASF1
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.secrel32	.Ldebug_line0
	.uleb128 0x1
	.byte	0x1
	.byte	0x6
	.ascii "char\0"
	.uleb128 0x4
	.long	0x6b
	.uleb128 0x1
	.byte	0x8
	.byte	0x7
	.ascii "long long unsigned int\0"
	.uleb128 0x1
	.byte	0x8
	.byte	0x5
	.ascii "long long int\0"
	.uleb128 0x1
	.byte	0x2
	.byte	0x7
	.ascii "short unsigned int\0"
	.uleb128 0x1
	.byte	0x4
	.byte	0x5
	.ascii "int\0"
	.uleb128 0x1
	.byte	0x4
	.byte	0x5
	.ascii "long int\0"
	.uleb128 0x1
	.byte	0x4
	.byte	0x7
	.ascii "unsigned int\0"
	.uleb128 0x5
	.ascii "printf\0"
	.byte	0x2
	.word	0x1c2
	.byte	0xf
	.long	0xb9
	.long	0xf7
	.uleb128 0x6
	.long	0xf7
	.uleb128 0x7
	.byte	0
	.uleb128 0x8
	.byte	0x8
	.long	0x73
	.uleb128 0x9
	.ascii "main\0"
	.byte	0x1
	.byte	0x2
	.byte	0x5
	.long	0xb9
	.quad	.LFB101
	.quad	.LFE101-.LFB101
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x2
	.ascii "x\0"
	.byte	0x3
	.long	0xb9
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.uleb128 0x2
	.ascii "y\0"
	.byte	0x4
	.long	0xb9
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x2
	.ascii "z\0"
	.byte	0x5
	.long	0xb9
	.uleb128 0x2
	.byte	0x91
	.sleb128 -28
	.byte	0
	.byte	0
	.section	.debug_abbrev,"dr"
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0x21
	.sleb128 7
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0x8
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x90
	.uleb128 0xb
	.uleb128 0x91
	.uleb128 0x6
	.uleb128 0x3
	.uleb128 0x1f
	.uleb128 0x1b
	.uleb128 0x1f
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"dr"
	.long	0x2c
	.word	0x2
	.secrel32	.Ldebug_info0
	.byte	0x8
	.byte	0
	.word	0
	.word	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	0
	.quad	0
	.section	.debug_line,"dr"
.Ldebug_line0:
	.section	.debug_str,"dr"
	.section	.debug_line_str,"dr"
.LASF0:
	.ascii "C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\\F\\programs\\z3.c\0"
.LASF1:
	.ascii "C:\\YSYX_WORKSPACE\\projects\\ysyx_f_to_b\0"
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (Rev13, Built by MSYS2 project) 15.2.0"
	.def	printf;	.scl	2;	.type	32;	.endef
