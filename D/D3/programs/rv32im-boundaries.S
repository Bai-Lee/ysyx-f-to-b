.option norvc
.option norelax
.section .text
.globl _start
_start:
li a0, 1
li t0, 0x00000000
li t1, 0x00000000
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 2
li t0, 0x00000000
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 3
li t0, 0x00000000
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 4
li t0, 0x00000000
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 5
li t0, 0x00000000
li t1, 0x00000020
add t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 6
li t0, 0x00000000
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 7
li t0, 0x00000000
li t1, 0x80000000
add t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 8
li t0, 0x00000000
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 9
li t0, 0x00000000
li t1, 0xffffffff
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 10
li t0, 0x00000001
li t1, 0x00000000
add t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 11
li t0, 0x00000001
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 12
li t0, 0x00000001
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 13
li t0, 0x00000001
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 14
li t0, 0x00000001
li t1, 0x00000020
add t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 15
li t0, 0x00000001
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 16
li t0, 0x00000001
li t1, 0x80000000
add t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 17
li t0, 0x00000001
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 18
li t0, 0x00000001
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 19
li t0, 0x00000002
li t1, 0x00000000
add t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 20
li t0, 0x00000002
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 21
li t0, 0x00000002
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 22
li t0, 0x00000002
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 23
li t0, 0x00000002
li t1, 0x00000020
add t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 24
li t0, 0x00000002
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 25
li t0, 0x00000002
li t1, 0x80000000
add t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 26
li t0, 0x00000002
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 27
li t0, 0x00000002
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 28
li t0, 0x0000001f
li t1, 0x00000000
add t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 29
li t0, 0x0000001f
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 30
li t0, 0x0000001f
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 31
li t0, 0x0000001f
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x0000003e
bne t6, t2, fail
li a0, 32
li t0, 0x0000001f
li t1, 0x00000020
add t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 33
li t0, 0x0000001f
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x8000001e
bne t6, t2, fail
li a0, 34
li t0, 0x0000001f
li t1, 0x80000000
add t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 35
li t0, 0x0000001f
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0x0000001d
bne t6, t2, fail
li a0, 36
li t0, 0x0000001f
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 37
li t0, 0x00000020
li t1, 0x00000000
add t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 38
li t0, 0x00000020
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 39
li t0, 0x00000020
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 40
li t0, 0x00000020
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 41
li t0, 0x00000020
li t1, 0x00000020
add t6,t0,t1
li t2, 0x00000040
bne t6, t2, fail
li a0, 42
li t0, 0x00000020
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 43
li t0, 0x00000020
li t1, 0x80000000
add t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 44
li t0, 0x00000020
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 45
li t0, 0x00000020
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 46
li t0, 0x7fffffff
li t1, 0x00000000
add t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 47
li t0, 0x7fffffff
li t1, 0x00000001
add t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 48
li t0, 0x7fffffff
li t1, 0x00000002
add t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 49
li t0, 0x7fffffff
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x8000001e
bne t6, t2, fail
li a0, 50
li t0, 0x7fffffff
li t1, 0x00000020
add t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 51
li t0, 0x7fffffff
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 52
li t0, 0x7fffffff
li t1, 0x80000000
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 53
li t0, 0x7fffffff
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0x7ffffffd
bne t6, t2, fail
li a0, 54
li t0, 0x7fffffff
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 55
li t0, 0x80000000
li t1, 0x00000000
add t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 56
li t0, 0x80000000
li t1, 0x00000001
add t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 57
li t0, 0x80000000
li t1, 0x00000002
add t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 58
li t0, 0x80000000
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 59
li t0, 0x80000000
li t1, 0x00000020
add t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 60
li t0, 0x80000000
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 61
li t0, 0x80000000
li t1, 0x80000000
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 62
li t0, 0x80000000
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 63
li t0, 0x80000000
li t1, 0xffffffff
add t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 64
li t0, 0xfffffffe
li t1, 0x00000000
add t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 65
li t0, 0xfffffffe
li t1, 0x00000001
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 66
li t0, 0xfffffffe
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 67
li t0, 0xfffffffe
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x0000001d
bne t6, t2, fail
li a0, 68
li t0, 0xfffffffe
li t1, 0x00000020
add t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 69
li t0, 0xfffffffe
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x7ffffffd
bne t6, t2, fail
li a0, 70
li t0, 0xfffffffe
li t1, 0x80000000
add t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 71
li t0, 0xfffffffe
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 72
li t0, 0xfffffffe
li t1, 0xffffffff
add t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 73
li t0, 0xffffffff
li t1, 0x00000000
add t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 74
li t0, 0xffffffff
li t1, 0x00000001
add t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 75
li t0, 0xffffffff
li t1, 0x00000002
add t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 76
li t0, 0xffffffff
li t1, 0x0000001f
add t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 77
li t0, 0xffffffff
li t1, 0x00000020
add t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 78
li t0, 0xffffffff
li t1, 0x7fffffff
add t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 79
li t0, 0xffffffff
li t1, 0x80000000
add t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 80
li t0, 0xffffffff
li t1, 0xfffffffe
add t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 81
li t0, 0xffffffff
li t1, 0xffffffff
add t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 82
li t0, 0x00000000
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 83
li t0, 0x00000000
li t1, 0x00000001
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 84
li t0, 0x00000000
li t1, 0x00000002
sub t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 85
li t0, 0x00000000
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 86
li t0, 0x00000000
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 87
li t0, 0x00000000
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 88
li t0, 0x00000000
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 89
li t0, 0x00000000
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 90
li t0, 0x00000000
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 91
li t0, 0x00000001
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 92
li t0, 0x00000001
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 93
li t0, 0x00000001
li t1, 0x00000002
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 94
li t0, 0x00000001
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0xffffffe2
bne t6, t2, fail
li a0, 95
li t0, 0x00000001
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 96
li t0, 0x00000001
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 97
li t0, 0x00000001
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 98
li t0, 0x00000001
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 99
li t0, 0x00000001
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 100
li t0, 0x00000002
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 101
li t0, 0x00000002
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 102
li t0, 0x00000002
li t1, 0x00000002
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 103
li t0, 0x00000002
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0xffffffe3
bne t6, t2, fail
li a0, 104
li t0, 0x00000002
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffe2
bne t6, t2, fail
li a0, 105
li t0, 0x00000002
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000003
bne t6, t2, fail
li a0, 106
li t0, 0x00000002
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 107
li t0, 0x00000002
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 108
li t0, 0x00000002
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 109
li t0, 0x0000001f
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 110
li t0, 0x0000001f
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 111
li t0, 0x0000001f
li t1, 0x00000002
sub t6,t0,t1
li t2, 0x0000001d
bne t6, t2, fail
li a0, 112
li t0, 0x0000001f
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 113
li t0, 0x0000001f
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 114
li t0, 0x0000001f
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 115
li t0, 0x0000001f
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 116
li t0, 0x0000001f
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 117
li t0, 0x0000001f
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 118
li t0, 0x00000020
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 119
li t0, 0x00000020
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 120
li t0, 0x00000020
li t1, 0x00000002
sub t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 121
li t0, 0x00000020
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 122
li t0, 0x00000020
li t1, 0x00000020
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 123
li t0, 0x00000020
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000021
bne t6, t2, fail
li a0, 124
li t0, 0x00000020
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 125
li t0, 0x00000020
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 126
li t0, 0x00000020
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 127
li t0, 0x7fffffff
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 128
li t0, 0x7fffffff
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 129
li t0, 0x7fffffff
li t1, 0x00000002
sub t6,t0,t1
li t2, 0x7ffffffd
bne t6, t2, fail
li a0, 130
li t0, 0x7fffffff
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0x7fffffe0
bne t6, t2, fail
li a0, 131
li t0, 0x7fffffff
li t1, 0x00000020
sub t6,t0,t1
li t2, 0x7fffffdf
bne t6, t2, fail
li a0, 132
li t0, 0x7fffffff
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 133
li t0, 0x7fffffff
li t1, 0x80000000
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 134
li t0, 0x7fffffff
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 135
li t0, 0x7fffffff
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 136
li t0, 0x80000000
li t1, 0x00000000
sub t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 137
li t0, 0x80000000
li t1, 0x00000001
sub t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 138
li t0, 0x80000000
li t1, 0x00000002
sub t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 139
li t0, 0x80000000
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0x7fffffe1
bne t6, t2, fail
li a0, 140
li t0, 0x80000000
li t1, 0x00000020
sub t6,t0,t1
li t2, 0x7fffffe0
bne t6, t2, fail
li a0, 141
li t0, 0x80000000
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 142
li t0, 0x80000000
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 143
li t0, 0x80000000
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 144
li t0, 0x80000000
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 145
li t0, 0xfffffffe
li t1, 0x00000000
sub t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 146
li t0, 0xfffffffe
li t1, 0x00000001
sub t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 147
li t0, 0xfffffffe
li t1, 0x00000002
sub t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 148
li t0, 0xfffffffe
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0xffffffdf
bne t6, t2, fail
li a0, 149
li t0, 0xfffffffe
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffde
bne t6, t2, fail
li a0, 150
li t0, 0xfffffffe
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 151
li t0, 0xfffffffe
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 152
li t0, 0xfffffffe
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 153
li t0, 0xfffffffe
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 154
li t0, 0xffffffff
li t1, 0x00000000
sub t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 155
li t0, 0xffffffff
li t1, 0x00000001
sub t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 156
li t0, 0xffffffff
li t1, 0x00000002
sub t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 157
li t0, 0xffffffff
li t1, 0x0000001f
sub t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 158
li t0, 0xffffffff
li t1, 0x00000020
sub t6,t0,t1
li t2, 0xffffffdf
bne t6, t2, fail
li a0, 159
li t0, 0xffffffff
li t1, 0x7fffffff
sub t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 160
li t0, 0xffffffff
li t1, 0x80000000
sub t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 161
li t0, 0xffffffff
li t1, 0xfffffffe
sub t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 162
li t0, 0xffffffff
li t1, 0xffffffff
sub t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 163
li t0, 0x00000000
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 164
li t0, 0x00000000
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 165
li t0, 0x00000000
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 166
li t0, 0x00000000
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 167
li t0, 0x00000000
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 168
li t0, 0x00000000
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 169
li t0, 0x00000000
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 170
li t0, 0x00000000
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 171
li t0, 0x00000000
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 172
li t0, 0x00000001
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 173
li t0, 0x00000001
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 174
li t0, 0x00000001
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 175
li t0, 0x00000001
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 176
li t0, 0x00000001
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 177
li t0, 0x00000001
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 178
li t0, 0x00000001
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 179
li t0, 0x00000001
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 180
li t0, 0x00000001
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 181
li t0, 0x00000002
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 182
li t0, 0x00000002
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 183
li t0, 0x00000002
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x00000008
bne t6, t2, fail
li a0, 184
li t0, 0x00000002
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 185
li t0, 0x00000002
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 186
li t0, 0x00000002
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 187
li t0, 0x00000002
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 188
li t0, 0x00000002
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 189
li t0, 0x00000002
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 190
li t0, 0x0000001f
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 191
li t0, 0x0000001f
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x0000003e
bne t6, t2, fail
li a0, 192
li t0, 0x0000001f
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x0000007c
bne t6, t2, fail
li a0, 193
li t0, 0x0000001f
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 194
li t0, 0x0000001f
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 195
li t0, 0x0000001f
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 196
li t0, 0x0000001f
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 197
li t0, 0x0000001f
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 198
li t0, 0x0000001f
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 199
li t0, 0x00000020
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 200
li t0, 0x00000020
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x00000040
bne t6, t2, fail
li a0, 201
li t0, 0x00000020
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x00000080
bne t6, t2, fail
li a0, 202
li t0, 0x00000020
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 203
li t0, 0x00000020
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 204
li t0, 0x00000020
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 205
li t0, 0x00000020
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 206
li t0, 0x00000020
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 207
li t0, 0x00000020
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 208
li t0, 0x7fffffff
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 209
li t0, 0x7fffffff
li t1, 0x00000001
sll t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 210
li t0, 0x7fffffff
li t1, 0x00000002
sll t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 211
li t0, 0x7fffffff
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 212
li t0, 0x7fffffff
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 213
li t0, 0x7fffffff
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 214
li t0, 0x7fffffff
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 215
li t0, 0x7fffffff
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 216
li t0, 0x7fffffff
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 217
li t0, 0x80000000
li t1, 0x00000000
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 218
li t0, 0x80000000
li t1, 0x00000001
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 219
li t0, 0x80000000
li t1, 0x00000002
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 220
li t0, 0x80000000
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 221
li t0, 0x80000000
li t1, 0x00000020
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 222
li t0, 0x80000000
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 223
li t0, 0x80000000
li t1, 0x80000000
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 224
li t0, 0x80000000
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 225
li t0, 0x80000000
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 226
li t0, 0xfffffffe
li t1, 0x00000000
sll t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 227
li t0, 0xfffffffe
li t1, 0x00000001
sll t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 228
li t0, 0xfffffffe
li t1, 0x00000002
sll t6,t0,t1
li t2, 0xfffffff8
bne t6, t2, fail
li a0, 229
li t0, 0xfffffffe
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 230
li t0, 0xfffffffe
li t1, 0x00000020
sll t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 231
li t0, 0xfffffffe
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 232
li t0, 0xfffffffe
li t1, 0x80000000
sll t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 233
li t0, 0xfffffffe
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 234
li t0, 0xfffffffe
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 235
li t0, 0xffffffff
li t1, 0x00000000
sll t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 236
li t0, 0xffffffff
li t1, 0x00000001
sll t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 237
li t0, 0xffffffff
li t1, 0x00000002
sll t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 238
li t0, 0xffffffff
li t1, 0x0000001f
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 239
li t0, 0xffffffff
li t1, 0x00000020
sll t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 240
li t0, 0xffffffff
li t1, 0x7fffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 241
li t0, 0xffffffff
li t1, 0x80000000
sll t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 242
li t0, 0xffffffff
li t1, 0xfffffffe
sll t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 243
li t0, 0xffffffff
li t1, 0xffffffff
sll t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 244
li t0, 0x00000000
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 245
li t0, 0x00000000
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 246
li t0, 0x00000000
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 247
li t0, 0x00000000
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 248
li t0, 0x00000000
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 249
li t0, 0x00000000
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 250
li t0, 0x00000000
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 251
li t0, 0x00000000
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 252
li t0, 0x00000000
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 253
li t0, 0x00000001
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 254
li t0, 0x00000001
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 255
li t0, 0x00000001
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 256
li t0, 0x00000001
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 257
li t0, 0x00000001
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 258
li t0, 0x00000001
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 259
li t0, 0x00000001
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 260
li t0, 0x00000001
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 261
li t0, 0x00000001
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 262
li t0, 0x00000002
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 263
li t0, 0x00000002
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 264
li t0, 0x00000002
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 265
li t0, 0x00000002
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 266
li t0, 0x00000002
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 267
li t0, 0x00000002
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 268
li t0, 0x00000002
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 269
li t0, 0x00000002
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 270
li t0, 0x00000002
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 271
li t0, 0x0000001f
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 272
li t0, 0x0000001f
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 273
li t0, 0x0000001f
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x00000007
bne t6, t2, fail
li a0, 274
li t0, 0x0000001f
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 275
li t0, 0x0000001f
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 276
li t0, 0x0000001f
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 277
li t0, 0x0000001f
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 278
li t0, 0x0000001f
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 279
li t0, 0x0000001f
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 280
li t0, 0x00000020
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 281
li t0, 0x00000020
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 282
li t0, 0x00000020
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x00000008
bne t6, t2, fail
li a0, 283
li t0, 0x00000020
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 284
li t0, 0x00000020
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 285
li t0, 0x00000020
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 286
li t0, 0x00000020
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 287
li t0, 0x00000020
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 288
li t0, 0x00000020
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 289
li t0, 0x7fffffff
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 290
li t0, 0x7fffffff
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 291
li t0, 0x7fffffff
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x1fffffff
bne t6, t2, fail
li a0, 292
li t0, 0x7fffffff
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 293
li t0, 0x7fffffff
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 294
li t0, 0x7fffffff
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 295
li t0, 0x7fffffff
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 296
li t0, 0x7fffffff
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 297
li t0, 0x7fffffff
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 298
li t0, 0x80000000
li t1, 0x00000000
srl t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 299
li t0, 0x80000000
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 300
li t0, 0x80000000
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x20000000
bne t6, t2, fail
li a0, 301
li t0, 0x80000000
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 302
li t0, 0x80000000
li t1, 0x00000020
srl t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 303
li t0, 0x80000000
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 304
li t0, 0x80000000
li t1, 0x80000000
srl t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 305
li t0, 0x80000000
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 306
li t0, 0x80000000
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 307
li t0, 0xfffffffe
li t1, 0x00000000
srl t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 308
li t0, 0xfffffffe
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 309
li t0, 0xfffffffe
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 310
li t0, 0xfffffffe
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 311
li t0, 0xfffffffe
li t1, 0x00000020
srl t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 312
li t0, 0xfffffffe
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 313
li t0, 0xfffffffe
li t1, 0x80000000
srl t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 314
li t0, 0xfffffffe
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 315
li t0, 0xfffffffe
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 316
li t0, 0xffffffff
li t1, 0x00000000
srl t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 317
li t0, 0xffffffff
li t1, 0x00000001
srl t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 318
li t0, 0xffffffff
li t1, 0x00000002
srl t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 319
li t0, 0xffffffff
li t1, 0x0000001f
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 320
li t0, 0xffffffff
li t1, 0x00000020
srl t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 321
li t0, 0xffffffff
li t1, 0x7fffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 322
li t0, 0xffffffff
li t1, 0x80000000
srl t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 323
li t0, 0xffffffff
li t1, 0xfffffffe
srl t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 324
li t0, 0xffffffff
li t1, 0xffffffff
srl t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 325
li t0, 0x00000000
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 326
li t0, 0x00000000
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 327
li t0, 0x00000000
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 328
li t0, 0x00000000
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 329
li t0, 0x00000000
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 330
li t0, 0x00000000
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 331
li t0, 0x00000000
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 332
li t0, 0x00000000
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 333
li t0, 0x00000000
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 334
li t0, 0x00000001
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 335
li t0, 0x00000001
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 336
li t0, 0x00000001
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 337
li t0, 0x00000001
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 338
li t0, 0x00000001
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 339
li t0, 0x00000001
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 340
li t0, 0x00000001
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 341
li t0, 0x00000001
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 342
li t0, 0x00000001
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 343
li t0, 0x00000002
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 344
li t0, 0x00000002
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 345
li t0, 0x00000002
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 346
li t0, 0x00000002
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 347
li t0, 0x00000002
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 348
li t0, 0x00000002
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 349
li t0, 0x00000002
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 350
li t0, 0x00000002
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 351
li t0, 0x00000002
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 352
li t0, 0x0000001f
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 353
li t0, 0x0000001f
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 354
li t0, 0x0000001f
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x00000007
bne t6, t2, fail
li a0, 355
li t0, 0x0000001f
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 356
li t0, 0x0000001f
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 357
li t0, 0x0000001f
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 358
li t0, 0x0000001f
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 359
li t0, 0x0000001f
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 360
li t0, 0x0000001f
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 361
li t0, 0x00000020
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 362
li t0, 0x00000020
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 363
li t0, 0x00000020
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x00000008
bne t6, t2, fail
li a0, 364
li t0, 0x00000020
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 365
li t0, 0x00000020
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 366
li t0, 0x00000020
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 367
li t0, 0x00000020
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 368
li t0, 0x00000020
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 369
li t0, 0x00000020
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 370
li t0, 0x7fffffff
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 371
li t0, 0x7fffffff
li t1, 0x00000001
sra t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 372
li t0, 0x7fffffff
li t1, 0x00000002
sra t6,t0,t1
li t2, 0x1fffffff
bne t6, t2, fail
li a0, 373
li t0, 0x7fffffff
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 374
li t0, 0x7fffffff
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 375
li t0, 0x7fffffff
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 376
li t0, 0x7fffffff
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 377
li t0, 0x7fffffff
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 378
li t0, 0x7fffffff
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 379
li t0, 0x80000000
li t1, 0x00000000
sra t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 380
li t0, 0x80000000
li t1, 0x00000001
sra t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 381
li t0, 0x80000000
li t1, 0x00000002
sra t6,t0,t1
li t2, 0xe0000000
bne t6, t2, fail
li a0, 382
li t0, 0x80000000
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 383
li t0, 0x80000000
li t1, 0x00000020
sra t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 384
li t0, 0x80000000
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 385
li t0, 0x80000000
li t1, 0x80000000
sra t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 386
li t0, 0x80000000
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 387
li t0, 0x80000000
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 388
li t0, 0xfffffffe
li t1, 0x00000000
sra t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 389
li t0, 0xfffffffe
li t1, 0x00000001
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 390
li t0, 0xfffffffe
li t1, 0x00000002
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 391
li t0, 0xfffffffe
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 392
li t0, 0xfffffffe
li t1, 0x00000020
sra t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 393
li t0, 0xfffffffe
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 394
li t0, 0xfffffffe
li t1, 0x80000000
sra t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 395
li t0, 0xfffffffe
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 396
li t0, 0xfffffffe
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 397
li t0, 0xffffffff
li t1, 0x00000000
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 398
li t0, 0xffffffff
li t1, 0x00000001
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 399
li t0, 0xffffffff
li t1, 0x00000002
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 400
li t0, 0xffffffff
li t1, 0x0000001f
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 401
li t0, 0xffffffff
li t1, 0x00000020
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 402
li t0, 0xffffffff
li t1, 0x7fffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 403
li t0, 0xffffffff
li t1, 0x80000000
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 404
li t0, 0xffffffff
li t1, 0xfffffffe
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 405
li t0, 0xffffffff
li t1, 0xffffffff
sra t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 406
li t0, 0x00000000
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 407
li t0, 0x00000000
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 408
li t0, 0x00000000
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 409
li t0, 0x00000000
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 410
li t0, 0x00000000
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 411
li t0, 0x00000000
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 412
li t0, 0x00000000
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 413
li t0, 0x00000000
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 414
li t0, 0x00000000
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 415
li t0, 0x00000001
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 416
li t0, 0x00000001
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 417
li t0, 0x00000001
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 418
li t0, 0x00000001
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 419
li t0, 0x00000001
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 420
li t0, 0x00000001
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 421
li t0, 0x00000001
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 422
li t0, 0x00000001
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 423
li t0, 0x00000001
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 424
li t0, 0x00000002
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 425
li t0, 0x00000002
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 426
li t0, 0x00000002
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 427
li t0, 0x00000002
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 428
li t0, 0x00000002
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 429
li t0, 0x00000002
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 430
li t0, 0x00000002
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 431
li t0, 0x00000002
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 432
li t0, 0x00000002
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 433
li t0, 0x0000001f
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 434
li t0, 0x0000001f
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 435
li t0, 0x0000001f
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 436
li t0, 0x0000001f
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 437
li t0, 0x0000001f
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 438
li t0, 0x0000001f
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 439
li t0, 0x0000001f
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 440
li t0, 0x0000001f
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 441
li t0, 0x0000001f
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 442
li t0, 0x00000020
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 443
li t0, 0x00000020
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 444
li t0, 0x00000020
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 445
li t0, 0x00000020
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 446
li t0, 0x00000020
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 447
li t0, 0x00000020
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 448
li t0, 0x00000020
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 449
li t0, 0x00000020
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 450
li t0, 0x00000020
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 451
li t0, 0x7fffffff
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 452
li t0, 0x7fffffff
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 453
li t0, 0x7fffffff
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 454
li t0, 0x7fffffff
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 455
li t0, 0x7fffffff
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 456
li t0, 0x7fffffff
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 457
li t0, 0x7fffffff
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 458
li t0, 0x7fffffff
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 459
li t0, 0x7fffffff
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 460
li t0, 0x80000000
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 461
li t0, 0x80000000
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 462
li t0, 0x80000000
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 463
li t0, 0x80000000
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 464
li t0, 0x80000000
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 465
li t0, 0x80000000
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 466
li t0, 0x80000000
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 467
li t0, 0x80000000
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 468
li t0, 0x80000000
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 469
li t0, 0xfffffffe
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 470
li t0, 0xfffffffe
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 471
li t0, 0xfffffffe
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 472
li t0, 0xfffffffe
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 473
li t0, 0xfffffffe
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 474
li t0, 0xfffffffe
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 475
li t0, 0xfffffffe
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 476
li t0, 0xfffffffe
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 477
li t0, 0xfffffffe
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 478
li t0, 0xffffffff
li t1, 0x00000000
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 479
li t0, 0xffffffff
li t1, 0x00000001
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 480
li t0, 0xffffffff
li t1, 0x00000002
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 481
li t0, 0xffffffff
li t1, 0x0000001f
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 482
li t0, 0xffffffff
li t1, 0x00000020
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 483
li t0, 0xffffffff
li t1, 0x7fffffff
slt t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 484
li t0, 0xffffffff
li t1, 0x80000000
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 485
li t0, 0xffffffff
li t1, 0xfffffffe
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 486
li t0, 0xffffffff
li t1, 0xffffffff
slt t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 487
li t0, 0x00000000
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 488
li t0, 0x00000000
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 489
li t0, 0x00000000
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 490
li t0, 0x00000000
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 491
li t0, 0x00000000
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 492
li t0, 0x00000000
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 493
li t0, 0x00000000
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 494
li t0, 0x00000000
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 495
li t0, 0x00000000
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 496
li t0, 0x00000001
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 497
li t0, 0x00000001
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 498
li t0, 0x00000001
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 499
li t0, 0x00000001
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 500
li t0, 0x00000001
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 501
li t0, 0x00000001
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 502
li t0, 0x00000001
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 503
li t0, 0x00000001
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 504
li t0, 0x00000001
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 505
li t0, 0x00000002
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 506
li t0, 0x00000002
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 507
li t0, 0x00000002
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 508
li t0, 0x00000002
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 509
li t0, 0x00000002
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 510
li t0, 0x00000002
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 511
li t0, 0x00000002
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 512
li t0, 0x00000002
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 513
li t0, 0x00000002
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 514
li t0, 0x0000001f
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 515
li t0, 0x0000001f
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 516
li t0, 0x0000001f
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 517
li t0, 0x0000001f
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 518
li t0, 0x0000001f
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 519
li t0, 0x0000001f
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 520
li t0, 0x0000001f
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 521
li t0, 0x0000001f
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 522
li t0, 0x0000001f
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 523
li t0, 0x00000020
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 524
li t0, 0x00000020
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 525
li t0, 0x00000020
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 526
li t0, 0x00000020
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 527
li t0, 0x00000020
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 528
li t0, 0x00000020
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 529
li t0, 0x00000020
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 530
li t0, 0x00000020
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 531
li t0, 0x00000020
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 532
li t0, 0x7fffffff
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 533
li t0, 0x7fffffff
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 534
li t0, 0x7fffffff
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 535
li t0, 0x7fffffff
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 536
li t0, 0x7fffffff
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 537
li t0, 0x7fffffff
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 538
li t0, 0x7fffffff
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 539
li t0, 0x7fffffff
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 540
li t0, 0x7fffffff
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 541
li t0, 0x80000000
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 542
li t0, 0x80000000
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 543
li t0, 0x80000000
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 544
li t0, 0x80000000
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 545
li t0, 0x80000000
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 546
li t0, 0x80000000
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 547
li t0, 0x80000000
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 548
li t0, 0x80000000
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 549
li t0, 0x80000000
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 550
li t0, 0xfffffffe
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 551
li t0, 0xfffffffe
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 552
li t0, 0xfffffffe
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 553
li t0, 0xfffffffe
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 554
li t0, 0xfffffffe
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 555
li t0, 0xfffffffe
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 556
li t0, 0xfffffffe
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 557
li t0, 0xfffffffe
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 558
li t0, 0xfffffffe
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 559
li t0, 0xffffffff
li t1, 0x00000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 560
li t0, 0xffffffff
li t1, 0x00000001
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 561
li t0, 0xffffffff
li t1, 0x00000002
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 562
li t0, 0xffffffff
li t1, 0x0000001f
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 563
li t0, 0xffffffff
li t1, 0x00000020
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 564
li t0, 0xffffffff
li t1, 0x7fffffff
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 565
li t0, 0xffffffff
li t1, 0x80000000
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 566
li t0, 0xffffffff
li t1, 0xfffffffe
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 567
li t0, 0xffffffff
li t1, 0xffffffff
sltu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 568
li t0, 0x00000000
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 569
li t0, 0x00000000
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 570
li t0, 0x00000000
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 571
li t0, 0x00000000
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 572
li t0, 0x00000000
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 573
li t0, 0x00000000
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 574
li t0, 0x00000000
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 575
li t0, 0x00000000
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 576
li t0, 0x00000000
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 577
li t0, 0x00000001
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 578
li t0, 0x00000001
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 579
li t0, 0x00000001
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 580
li t0, 0x00000001
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 581
li t0, 0x00000001
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 582
li t0, 0x00000001
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 583
li t0, 0x00000001
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 584
li t0, 0x00000001
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 585
li t0, 0x00000001
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 586
li t0, 0x00000002
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 587
li t0, 0x00000002
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 588
li t0, 0x00000002
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 589
li t0, 0x00000002
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x0000001d
bne t6, t2, fail
li a0, 590
li t0, 0x00000002
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 591
li t0, 0x00000002
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x7ffffffd
bne t6, t2, fail
li a0, 592
li t0, 0x00000002
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 593
li t0, 0x00000002
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 594
li t0, 0x00000002
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 595
li t0, 0x0000001f
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 596
li t0, 0x0000001f
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 597
li t0, 0x0000001f
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x0000001d
bne t6, t2, fail
li a0, 598
li t0, 0x0000001f
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 599
li t0, 0x0000001f
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 600
li t0, 0x0000001f
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x7fffffe0
bne t6, t2, fail
li a0, 601
li t0, 0x0000001f
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 602
li t0, 0x0000001f
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 603
li t0, 0x0000001f
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 604
li t0, 0x00000020
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 605
li t0, 0x00000020
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 606
li t0, 0x00000020
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 607
li t0, 0x00000020
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 608
li t0, 0x00000020
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 609
li t0, 0x00000020
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x7fffffdf
bne t6, t2, fail
li a0, 610
li t0, 0x00000020
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 611
li t0, 0x00000020
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0xffffffde
bne t6, t2, fail
li a0, 612
li t0, 0x00000020
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0xffffffdf
bne t6, t2, fail
li a0, 613
li t0, 0x7fffffff
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 614
li t0, 0x7fffffff
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 615
li t0, 0x7fffffff
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x7ffffffd
bne t6, t2, fail
li a0, 616
li t0, 0x7fffffff
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x7fffffe0
bne t6, t2, fail
li a0, 617
li t0, 0x7fffffff
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x7fffffdf
bne t6, t2, fail
li a0, 618
li t0, 0x7fffffff
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 619
li t0, 0x7fffffff
li t1, 0x80000000
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 620
li t0, 0x7fffffff
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 621
li t0, 0x7fffffff
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 622
li t0, 0x80000000
li t1, 0x00000000
xor t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 623
li t0, 0x80000000
li t1, 0x00000001
xor t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 624
li t0, 0x80000000
li t1, 0x00000002
xor t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 625
li t0, 0x80000000
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 626
li t0, 0x80000000
li t1, 0x00000020
xor t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 627
li t0, 0x80000000
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 628
li t0, 0x80000000
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 629
li t0, 0x80000000
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 630
li t0, 0x80000000
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 631
li t0, 0xfffffffe
li t1, 0x00000000
xor t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 632
li t0, 0xfffffffe
li t1, 0x00000001
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 633
li t0, 0xfffffffe
li t1, 0x00000002
xor t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 634
li t0, 0xfffffffe
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 635
li t0, 0xfffffffe
li t1, 0x00000020
xor t6,t0,t1
li t2, 0xffffffde
bne t6, t2, fail
li a0, 636
li t0, 0xfffffffe
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 637
li t0, 0xfffffffe
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 638
li t0, 0xfffffffe
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 639
li t0, 0xfffffffe
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 640
li t0, 0xffffffff
li t1, 0x00000000
xor t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 641
li t0, 0xffffffff
li t1, 0x00000001
xor t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 642
li t0, 0xffffffff
li t1, 0x00000002
xor t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 643
li t0, 0xffffffff
li t1, 0x0000001f
xor t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 644
li t0, 0xffffffff
li t1, 0x00000020
xor t6,t0,t1
li t2, 0xffffffdf
bne t6, t2, fail
li a0, 645
li t0, 0xffffffff
li t1, 0x7fffffff
xor t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 646
li t0, 0xffffffff
li t1, 0x80000000
xor t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 647
li t0, 0xffffffff
li t1, 0xfffffffe
xor t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 648
li t0, 0xffffffff
li t1, 0xffffffff
xor t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 649
li t0, 0x00000000
li t1, 0x00000000
or t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 650
li t0, 0x00000000
li t1, 0x00000001
or t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 651
li t0, 0x00000000
li t1, 0x00000002
or t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 652
li t0, 0x00000000
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 653
li t0, 0x00000000
li t1, 0x00000020
or t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 654
li t0, 0x00000000
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 655
li t0, 0x00000000
li t1, 0x80000000
or t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 656
li t0, 0x00000000
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 657
li t0, 0x00000000
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 658
li t0, 0x00000001
li t1, 0x00000000
or t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 659
li t0, 0x00000001
li t1, 0x00000001
or t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 660
li t0, 0x00000001
li t1, 0x00000002
or t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 661
li t0, 0x00000001
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 662
li t0, 0x00000001
li t1, 0x00000020
or t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 663
li t0, 0x00000001
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 664
li t0, 0x00000001
li t1, 0x80000000
or t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 665
li t0, 0x00000001
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 666
li t0, 0x00000001
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 667
li t0, 0x00000002
li t1, 0x00000000
or t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 668
li t0, 0x00000002
li t1, 0x00000001
or t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 669
li t0, 0x00000002
li t1, 0x00000002
or t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 670
li t0, 0x00000002
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 671
li t0, 0x00000002
li t1, 0x00000020
or t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 672
li t0, 0x00000002
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 673
li t0, 0x00000002
li t1, 0x80000000
or t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 674
li t0, 0x00000002
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 675
li t0, 0x00000002
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 676
li t0, 0x0000001f
li t1, 0x00000000
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 677
li t0, 0x0000001f
li t1, 0x00000001
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 678
li t0, 0x0000001f
li t1, 0x00000002
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 679
li t0, 0x0000001f
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 680
li t0, 0x0000001f
li t1, 0x00000020
or t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 681
li t0, 0x0000001f
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 682
li t0, 0x0000001f
li t1, 0x80000000
or t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 683
li t0, 0x0000001f
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 684
li t0, 0x0000001f
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 685
li t0, 0x00000020
li t1, 0x00000000
or t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 686
li t0, 0x00000020
li t1, 0x00000001
or t6,t0,t1
li t2, 0x00000021
bne t6, t2, fail
li a0, 687
li t0, 0x00000020
li t1, 0x00000002
or t6,t0,t1
li t2, 0x00000022
bne t6, t2, fail
li a0, 688
li t0, 0x00000020
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x0000003f
bne t6, t2, fail
li a0, 689
li t0, 0x00000020
li t1, 0x00000020
or t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 690
li t0, 0x00000020
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 691
li t0, 0x00000020
li t1, 0x80000000
or t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 692
li t0, 0x00000020
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 693
li t0, 0x00000020
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 694
li t0, 0x7fffffff
li t1, 0x00000000
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 695
li t0, 0x7fffffff
li t1, 0x00000001
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 696
li t0, 0x7fffffff
li t1, 0x00000002
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 697
li t0, 0x7fffffff
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 698
li t0, 0x7fffffff
li t1, 0x00000020
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 699
li t0, 0x7fffffff
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 700
li t0, 0x7fffffff
li t1, 0x80000000
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 701
li t0, 0x7fffffff
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 702
li t0, 0x7fffffff
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 703
li t0, 0x80000000
li t1, 0x00000000
or t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 704
li t0, 0x80000000
li t1, 0x00000001
or t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 705
li t0, 0x80000000
li t1, 0x00000002
or t6,t0,t1
li t2, 0x80000002
bne t6, t2, fail
li a0, 706
li t0, 0x80000000
li t1, 0x0000001f
or t6,t0,t1
li t2, 0x8000001f
bne t6, t2, fail
li a0, 707
li t0, 0x80000000
li t1, 0x00000020
or t6,t0,t1
li t2, 0x80000020
bne t6, t2, fail
li a0, 708
li t0, 0x80000000
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 709
li t0, 0x80000000
li t1, 0x80000000
or t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 710
li t0, 0x80000000
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 711
li t0, 0x80000000
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 712
li t0, 0xfffffffe
li t1, 0x00000000
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 713
li t0, 0xfffffffe
li t1, 0x00000001
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 714
li t0, 0xfffffffe
li t1, 0x00000002
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 715
li t0, 0xfffffffe
li t1, 0x0000001f
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 716
li t0, 0xfffffffe
li t1, 0x00000020
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 717
li t0, 0xfffffffe
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 718
li t0, 0xfffffffe
li t1, 0x80000000
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 719
li t0, 0xfffffffe
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 720
li t0, 0xfffffffe
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 721
li t0, 0xffffffff
li t1, 0x00000000
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 722
li t0, 0xffffffff
li t1, 0x00000001
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 723
li t0, 0xffffffff
li t1, 0x00000002
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 724
li t0, 0xffffffff
li t1, 0x0000001f
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 725
li t0, 0xffffffff
li t1, 0x00000020
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 726
li t0, 0xffffffff
li t1, 0x7fffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 727
li t0, 0xffffffff
li t1, 0x80000000
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 728
li t0, 0xffffffff
li t1, 0xfffffffe
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 729
li t0, 0xffffffff
li t1, 0xffffffff
or t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 730
li t0, 0x00000000
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 731
li t0, 0x00000000
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 732
li t0, 0x00000000
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 733
li t0, 0x00000000
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 734
li t0, 0x00000000
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 735
li t0, 0x00000000
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 736
li t0, 0x00000000
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 737
li t0, 0x00000000
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 738
li t0, 0x00000000
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 739
li t0, 0x00000001
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 740
li t0, 0x00000001
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 741
li t0, 0x00000001
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 742
li t0, 0x00000001
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 743
li t0, 0x00000001
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 744
li t0, 0x00000001
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 745
li t0, 0x00000001
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 746
li t0, 0x00000001
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 747
li t0, 0x00000001
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 748
li t0, 0x00000002
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 749
li t0, 0x00000002
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 750
li t0, 0x00000002
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 751
li t0, 0x00000002
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 752
li t0, 0x00000002
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 753
li t0, 0x00000002
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 754
li t0, 0x00000002
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 755
li t0, 0x00000002
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 756
li t0, 0x00000002
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 757
li t0, 0x0000001f
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 758
li t0, 0x0000001f
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 759
li t0, 0x0000001f
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 760
li t0, 0x0000001f
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 761
li t0, 0x0000001f
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 762
li t0, 0x0000001f
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 763
li t0, 0x0000001f
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 764
li t0, 0x0000001f
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 765
li t0, 0x0000001f
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 766
li t0, 0x00000020
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 767
li t0, 0x00000020
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 768
li t0, 0x00000020
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 769
li t0, 0x00000020
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 770
li t0, 0x00000020
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 771
li t0, 0x00000020
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 772
li t0, 0x00000020
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 773
li t0, 0x00000020
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 774
li t0, 0x00000020
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 775
li t0, 0x7fffffff
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 776
li t0, 0x7fffffff
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 777
li t0, 0x7fffffff
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 778
li t0, 0x7fffffff
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 779
li t0, 0x7fffffff
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 780
li t0, 0x7fffffff
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 781
li t0, 0x7fffffff
li t1, 0x80000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 782
li t0, 0x7fffffff
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 783
li t0, 0x7fffffff
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 784
li t0, 0x80000000
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 785
li t0, 0x80000000
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 786
li t0, 0x80000000
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 787
li t0, 0x80000000
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 788
li t0, 0x80000000
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 789
li t0, 0x80000000
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 790
li t0, 0x80000000
li t1, 0x80000000
and t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 791
li t0, 0x80000000
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 792
li t0, 0x80000000
li t1, 0xffffffff
and t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 793
li t0, 0xfffffffe
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 794
li t0, 0xfffffffe
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 795
li t0, 0xfffffffe
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 796
li t0, 0xfffffffe
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 797
li t0, 0xfffffffe
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 798
li t0, 0xfffffffe
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 799
li t0, 0xfffffffe
li t1, 0x80000000
and t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 800
li t0, 0xfffffffe
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 801
li t0, 0xfffffffe
li t1, 0xffffffff
and t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 802
li t0, 0xffffffff
li t1, 0x00000000
and t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 803
li t0, 0xffffffff
li t1, 0x00000001
and t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 804
li t0, 0xffffffff
li t1, 0x00000002
and t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 805
li t0, 0xffffffff
li t1, 0x0000001f
and t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 806
li t0, 0xffffffff
li t1, 0x00000020
and t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 807
li t0, 0xffffffff
li t1, 0x7fffffff
and t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 808
li t0, 0xffffffff
li t1, 0x80000000
and t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 809
li t0, 0xffffffff
li t1, 0xfffffffe
and t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 810
li t0, 0xffffffff
li t1, 0xffffffff
and t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 811
li t0, 0x00000000
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 812
li t0, 0x00000000
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 813
li t0, 0x00000000
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 814
li t0, 0x00000000
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 815
li t0, 0x00000000
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 816
li t0, 0x00000000
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 817
li t0, 0x00000000
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 818
li t0, 0x00000000
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 819
li t0, 0x00000000
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 820
li t0, 0x00000001
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 821
li t0, 0x00000001
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 822
li t0, 0x00000001
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 823
li t0, 0x00000001
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 824
li t0, 0x00000001
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 825
li t0, 0x00000001
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 826
li t0, 0x00000001
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 827
li t0, 0x00000001
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 828
li t0, 0x00000001
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 829
li t0, 0x00000002
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 830
li t0, 0x00000002
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 831
li t0, 0x00000002
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 832
li t0, 0x00000002
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x0000003e
bne t6, t2, fail
li a0, 833
li t0, 0x00000002
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x00000040
bne t6, t2, fail
li a0, 834
li t0, 0x00000002
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 835
li t0, 0x00000002
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 836
li t0, 0x00000002
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 837
li t0, 0x00000002
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 838
li t0, 0x0000001f
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 839
li t0, 0x0000001f
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 840
li t0, 0x0000001f
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x0000003e
bne t6, t2, fail
li a0, 841
li t0, 0x0000001f
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x000003c1
bne t6, t2, fail
li a0, 842
li t0, 0x0000001f
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x000003e0
bne t6, t2, fail
li a0, 843
li t0, 0x0000001f
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x7fffffe1
bne t6, t2, fail
li a0, 844
li t0, 0x0000001f
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 845
li t0, 0x0000001f
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0xffffffc2
bne t6, t2, fail
li a0, 846
li t0, 0x0000001f
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 847
li t0, 0x00000020
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 848
li t0, 0x00000020
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 849
li t0, 0x00000020
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x00000040
bne t6, t2, fail
li a0, 850
li t0, 0x00000020
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x000003e0
bne t6, t2, fail
li a0, 851
li t0, 0x00000020
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x00000400
bne t6, t2, fail
li a0, 852
li t0, 0x00000020
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 853
li t0, 0x00000020
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 854
li t0, 0x00000020
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0xffffffc0
bne t6, t2, fail
li a0, 855
li t0, 0x00000020
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 856
li t0, 0x7fffffff
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 857
li t0, 0x7fffffff
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 858
li t0, 0x7fffffff
li t1, 0x00000002
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 859
li t0, 0x7fffffff
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x7fffffe1
bne t6, t2, fail
li a0, 860
li t0, 0x7fffffff
li t1, 0x00000020
mul t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 861
li t0, 0x7fffffff
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 862
li t0, 0x7fffffff
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 863
li t0, 0x7fffffff
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 864
li t0, 0x7fffffff
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 865
li t0, 0x80000000
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 866
li t0, 0x80000000
li t1, 0x00000001
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 867
li t0, 0x80000000
li t1, 0x00000002
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 868
li t0, 0x80000000
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 869
li t0, 0x80000000
li t1, 0x00000020
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 870
li t0, 0x80000000
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 871
li t0, 0x80000000
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 872
li t0, 0x80000000
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 873
li t0, 0x80000000
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 874
li t0, 0xfffffffe
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 875
li t0, 0xfffffffe
li t1, 0x00000001
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 876
li t0, 0xfffffffe
li t1, 0x00000002
mul t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 877
li t0, 0xfffffffe
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0xffffffc2
bne t6, t2, fail
li a0, 878
li t0, 0xfffffffe
li t1, 0x00000020
mul t6,t0,t1
li t2, 0xffffffc0
bne t6, t2, fail
li a0, 879
li t0, 0xfffffffe
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 880
li t0, 0xfffffffe
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 881
li t0, 0xfffffffe
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0x00000004
bne t6, t2, fail
li a0, 882
li t0, 0xfffffffe
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 883
li t0, 0xffffffff
li t1, 0x00000000
mul t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 884
li t0, 0xffffffff
li t1, 0x00000001
mul t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 885
li t0, 0xffffffff
li t1, 0x00000002
mul t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 886
li t0, 0xffffffff
li t1, 0x0000001f
mul t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 887
li t0, 0xffffffff
li t1, 0x00000020
mul t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 888
li t0, 0xffffffff
li t1, 0x7fffffff
mul t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 889
li t0, 0xffffffff
li t1, 0x80000000
mul t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 890
li t0, 0xffffffff
li t1, 0xfffffffe
mul t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 891
li t0, 0xffffffff
li t1, 0xffffffff
mul t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 892
li t0, 0x00000000
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 893
li t0, 0x00000000
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 894
li t0, 0x00000000
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 895
li t0, 0x00000000
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 896
li t0, 0x00000000
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 897
li t0, 0x00000000
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 898
li t0, 0x00000000
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 899
li t0, 0x00000000
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 900
li t0, 0x00000000
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 901
li t0, 0x00000001
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 902
li t0, 0x00000001
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 903
li t0, 0x00000001
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 904
li t0, 0x00000001
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 905
li t0, 0x00000001
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 906
li t0, 0x00000001
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 907
li t0, 0x00000001
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 908
li t0, 0x00000001
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 909
li t0, 0x00000001
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 910
li t0, 0x00000002
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 911
li t0, 0x00000002
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 912
li t0, 0x00000002
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 913
li t0, 0x00000002
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 914
li t0, 0x00000002
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 915
li t0, 0x00000002
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 916
li t0, 0x00000002
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 917
li t0, 0x00000002
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 918
li t0, 0x00000002
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 919
li t0, 0x0000001f
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 920
li t0, 0x0000001f
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 921
li t0, 0x0000001f
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 922
li t0, 0x0000001f
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 923
li t0, 0x0000001f
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 924
li t0, 0x0000001f
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 925
li t0, 0x0000001f
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 926
li t0, 0x0000001f
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 927
li t0, 0x0000001f
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 928
li t0, 0x00000020
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 929
li t0, 0x00000020
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 930
li t0, 0x00000020
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 931
li t0, 0x00000020
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 932
li t0, 0x00000020
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 933
li t0, 0x00000020
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 934
li t0, 0x00000020
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 935
li t0, 0x00000020
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 936
li t0, 0x00000020
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 937
li t0, 0x7fffffff
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 938
li t0, 0x7fffffff
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 939
li t0, 0x7fffffff
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 940
li t0, 0x7fffffff
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 941
li t0, 0x7fffffff
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 942
li t0, 0x7fffffff
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 943
li t0, 0x7fffffff
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 944
li t0, 0x7fffffff
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 945
li t0, 0x7fffffff
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 946
li t0, 0x80000000
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 947
li t0, 0x80000000
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 948
li t0, 0x80000000
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 949
li t0, 0x80000000
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 950
li t0, 0x80000000
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 951
li t0, 0x80000000
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 952
li t0, 0x80000000
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 953
li t0, 0x80000000
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 954
li t0, 0x80000000
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 955
li t0, 0xfffffffe
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 956
li t0, 0xfffffffe
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 957
li t0, 0xfffffffe
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 958
li t0, 0xfffffffe
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 959
li t0, 0xfffffffe
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 960
li t0, 0xfffffffe
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 961
li t0, 0xfffffffe
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 962
li t0, 0xfffffffe
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 963
li t0, 0xfffffffe
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 964
li t0, 0xffffffff
li t1, 0x00000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 965
li t0, 0xffffffff
li t1, 0x00000001
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 966
li t0, 0xffffffff
li t1, 0x00000002
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 967
li t0, 0xffffffff
li t1, 0x0000001f
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 968
li t0, 0xffffffff
li t1, 0x00000020
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 969
li t0, 0xffffffff
li t1, 0x7fffffff
mulh t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 970
li t0, 0xffffffff
li t1, 0x80000000
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 971
li t0, 0xffffffff
li t1, 0xfffffffe
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 972
li t0, 0xffffffff
li t1, 0xffffffff
mulh t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 973
li t0, 0x00000000
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 974
li t0, 0x00000000
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 975
li t0, 0x00000000
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 976
li t0, 0x00000000
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 977
li t0, 0x00000000
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 978
li t0, 0x00000000
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 979
li t0, 0x00000000
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 980
li t0, 0x00000000
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 981
li t0, 0x00000000
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 982
li t0, 0x00000001
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 983
li t0, 0x00000001
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 984
li t0, 0x00000001
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 985
li t0, 0x00000001
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 986
li t0, 0x00000001
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 987
li t0, 0x00000001
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 988
li t0, 0x00000001
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 989
li t0, 0x00000001
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 990
li t0, 0x00000001
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 991
li t0, 0x00000002
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 992
li t0, 0x00000002
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 993
li t0, 0x00000002
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 994
li t0, 0x00000002
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 995
li t0, 0x00000002
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 996
li t0, 0x00000002
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 997
li t0, 0x00000002
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 998
li t0, 0x00000002
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 999
li t0, 0x00000002
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1000
li t0, 0x0000001f
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1001
li t0, 0x0000001f
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1002
li t0, 0x0000001f
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1003
li t0, 0x0000001f
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1004
li t0, 0x0000001f
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1005
li t0, 0x0000001f
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1006
li t0, 0x0000001f
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1007
li t0, 0x0000001f
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1008
li t0, 0x0000001f
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1009
li t0, 0x00000020
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1010
li t0, 0x00000020
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1011
li t0, 0x00000020
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1012
li t0, 0x00000020
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1013
li t0, 0x00000020
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1014
li t0, 0x00000020
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1015
li t0, 0x00000020
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 1016
li t0, 0x00000020
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1017
li t0, 0x00000020
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1018
li t0, 0x7fffffff
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1019
li t0, 0x7fffffff
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1020
li t0, 0x7fffffff
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1021
li t0, 0x7fffffff
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1022
li t0, 0x7fffffff
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1023
li t0, 0x7fffffff
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1024
li t0, 0x7fffffff
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1025
li t0, 0x7fffffff
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1026
li t0, 0x7fffffff
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1027
li t0, 0x80000000
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1028
li t0, 0x80000000
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1029
li t0, 0x80000000
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1030
li t0, 0x80000000
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 1031
li t0, 0x80000000
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 1032
li t0, 0x80000000
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 1033
li t0, 0x80000000
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 1034
li t0, 0x80000000
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 1035
li t0, 0x80000000
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1036
li t0, 0xfffffffe
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1037
li t0, 0xfffffffe
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1038
li t0, 0xfffffffe
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1039
li t0, 0xfffffffe
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1040
li t0, 0xfffffffe
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1041
li t0, 0xfffffffe
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1042
li t0, 0xfffffffe
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1043
li t0, 0xfffffffe
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1044
li t0, 0xfffffffe
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1045
li t0, 0xffffffff
li t1, 0x00000000
mulhsu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1046
li t0, 0xffffffff
li t1, 0x00000001
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1047
li t0, 0xffffffff
li t1, 0x00000002
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1048
li t0, 0xffffffff
li t1, 0x0000001f
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1049
li t0, 0xffffffff
li t1, 0x00000020
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1050
li t0, 0xffffffff
li t1, 0x7fffffff
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1051
li t0, 0xffffffff
li t1, 0x80000000
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1052
li t0, 0xffffffff
li t1, 0xfffffffe
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1053
li t0, 0xffffffff
li t1, 0xffffffff
mulhsu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1054
li t0, 0x00000000
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1055
li t0, 0x00000000
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1056
li t0, 0x00000000
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1057
li t0, 0x00000000
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1058
li t0, 0x00000000
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1059
li t0, 0x00000000
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1060
li t0, 0x00000000
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1061
li t0, 0x00000000
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1062
li t0, 0x00000000
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1063
li t0, 0x00000001
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1064
li t0, 0x00000001
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1065
li t0, 0x00000001
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1066
li t0, 0x00000001
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1067
li t0, 0x00000001
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1068
li t0, 0x00000001
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1069
li t0, 0x00000001
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1070
li t0, 0x00000001
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1071
li t0, 0x00000001
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1072
li t0, 0x00000002
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1073
li t0, 0x00000002
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1074
li t0, 0x00000002
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1075
li t0, 0x00000002
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1076
li t0, 0x00000002
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1077
li t0, 0x00000002
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1078
li t0, 0x00000002
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1079
li t0, 0x00000002
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1080
li t0, 0x00000002
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1081
li t0, 0x0000001f
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1082
li t0, 0x0000001f
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1083
li t0, 0x0000001f
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1084
li t0, 0x0000001f
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1085
li t0, 0x0000001f
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1086
li t0, 0x0000001f
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1087
li t0, 0x0000001f
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1088
li t0, 0x0000001f
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1089
li t0, 0x0000001f
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1090
li t0, 0x00000020
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1091
li t0, 0x00000020
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1092
li t0, 0x00000020
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1093
li t0, 0x00000020
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1094
li t0, 0x00000020
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1095
li t0, 0x00000020
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1096
li t0, 0x00000020
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 1097
li t0, 0x00000020
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1098
li t0, 0x00000020
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1099
li t0, 0x7fffffff
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1100
li t0, 0x7fffffff
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1101
li t0, 0x7fffffff
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1102
li t0, 0x7fffffff
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1103
li t0, 0x7fffffff
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1104
li t0, 0x7fffffff
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1105
li t0, 0x7fffffff
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1106
li t0, 0x7fffffff
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1107
li t0, 0x7fffffff
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1108
li t0, 0x80000000
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1109
li t0, 0x80000000
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1110
li t0, 0x80000000
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1111
li t0, 0x80000000
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1112
li t0, 0x80000000
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 1113
li t0, 0x80000000
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1114
li t0, 0x80000000
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 1115
li t0, 0x80000000
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1116
li t0, 0x80000000
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1117
li t0, 0xfffffffe
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1118
li t0, 0xfffffffe
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1119
li t0, 0xfffffffe
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1120
li t0, 0xfffffffe
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1121
li t0, 0xfffffffe
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1122
li t0, 0xfffffffe
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1123
li t0, 0xfffffffe
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1124
li t0, 0xfffffffe
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0xfffffffc
bne t6, t2, fail
li a0, 1125
li t0, 0xfffffffe
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 1126
li t0, 0xffffffff
li t1, 0x00000000
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1127
li t0, 0xffffffff
li t1, 0x00000001
mulhu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1128
li t0, 0xffffffff
li t1, 0x00000002
mulhu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1129
li t0, 0xffffffff
li t1, 0x0000001f
mulhu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1130
li t0, 0xffffffff
li t1, 0x00000020
mulhu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1131
li t0, 0xffffffff
li t1, 0x7fffffff
mulhu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1132
li t0, 0xffffffff
li t1, 0x80000000
mulhu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1133
li t0, 0xffffffff
li t1, 0xfffffffe
mulhu t6,t0,t1
li t2, 0xfffffffd
bne t6, t2, fail
li a0, 1134
li t0, 0xffffffff
li t1, 0xffffffff
mulhu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1135
li t0, 0x00000000
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1136
li t0, 0x00000000
li t1, 0x00000001
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1137
li t0, 0x00000000
li t1, 0x00000002
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1138
li t0, 0x00000000
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1139
li t0, 0x00000000
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1140
li t0, 0x00000000
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1141
li t0, 0x00000000
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1142
li t0, 0x00000000
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1143
li t0, 0x00000000
li t1, 0xffffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1144
li t0, 0x00000001
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1145
li t0, 0x00000001
li t1, 0x00000001
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1146
li t0, 0x00000001
li t1, 0x00000002
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1147
li t0, 0x00000001
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1148
li t0, 0x00000001
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1149
li t0, 0x00000001
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1150
li t0, 0x00000001
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1151
li t0, 0x00000001
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1152
li t0, 0x00000001
li t1, 0xffffffff
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1153
li t0, 0x00000002
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1154
li t0, 0x00000002
li t1, 0x00000001
div t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1155
li t0, 0x00000002
li t1, 0x00000002
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1156
li t0, 0x00000002
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1157
li t0, 0x00000002
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1158
li t0, 0x00000002
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1159
li t0, 0x00000002
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1160
li t0, 0x00000002
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1161
li t0, 0x00000002
li t1, 0xffffffff
div t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1162
li t0, 0x0000001f
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1163
li t0, 0x0000001f
li t1, 0x00000001
div t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1164
li t0, 0x0000001f
li t1, 0x00000002
div t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1165
li t0, 0x0000001f
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1166
li t0, 0x0000001f
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1167
li t0, 0x0000001f
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1168
li t0, 0x0000001f
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1169
li t0, 0x0000001f
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0xfffffff1
bne t6, t2, fail
li a0, 1170
li t0, 0x0000001f
li t1, 0xffffffff
div t6,t0,t1
li t2, 0xffffffe1
bne t6, t2, fail
li a0, 1171
li t0, 0x00000020
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1172
li t0, 0x00000020
li t1, 0x00000001
div t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1173
li t0, 0x00000020
li t1, 0x00000002
div t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 1174
li t0, 0x00000020
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1175
li t0, 0x00000020
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1176
li t0, 0x00000020
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1177
li t0, 0x00000020
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1178
li t0, 0x00000020
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0xfffffff0
bne t6, t2, fail
li a0, 1179
li t0, 0x00000020
li t1, 0xffffffff
div t6,t0,t1
li t2, 0xffffffe0
bne t6, t2, fail
li a0, 1180
li t0, 0x7fffffff
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1181
li t0, 0x7fffffff
li t1, 0x00000001
div t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1182
li t0, 0x7fffffff
li t1, 0x00000002
div t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1183
li t0, 0x7fffffff
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x04210842
bne t6, t2, fail
li a0, 1184
li t0, 0x7fffffff
li t1, 0x00000020
div t6,t0,t1
li t2, 0x03ffffff
bne t6, t2, fail
li a0, 1185
li t0, 0x7fffffff
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1186
li t0, 0x7fffffff
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1187
li t0, 0x7fffffff
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0xc0000001
bne t6, t2, fail
li a0, 1188
li t0, 0x7fffffff
li t1, 0xffffffff
div t6,t0,t1
li t2, 0x80000001
bne t6, t2, fail
li a0, 1189
li t0, 0x80000000
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1190
li t0, 0x80000000
li t1, 0x00000001
div t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1191
li t0, 0x80000000
li t1, 0x00000002
div t6,t0,t1
li t2, 0xc0000000
bne t6, t2, fail
li a0, 1192
li t0, 0x80000000
li t1, 0x0000001f
div t6,t0,t1
li t2, 0xfbdef7be
bne t6, t2, fail
li a0, 1193
li t0, 0x80000000
li t1, 0x00000020
div t6,t0,t1
li t2, 0xfc000000
bne t6, t2, fail
li a0, 1194
li t0, 0x80000000
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1195
li t0, 0x80000000
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1196
li t0, 0x80000000
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 1197
li t0, 0x80000000
li t1, 0xffffffff
div t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1198
li t0, 0xfffffffe
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1199
li t0, 0xfffffffe
li t1, 0x00000001
div t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1200
li t0, 0xfffffffe
li t1, 0x00000002
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1201
li t0, 0xfffffffe
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1202
li t0, 0xfffffffe
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1203
li t0, 0xfffffffe
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1204
li t0, 0xfffffffe
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1205
li t0, 0xfffffffe
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1206
li t0, 0xfffffffe
li t1, 0xffffffff
div t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1207
li t0, 0xffffffff
li t1, 0x00000000
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1208
li t0, 0xffffffff
li t1, 0x00000001
div t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1209
li t0, 0xffffffff
li t1, 0x00000002
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1210
li t0, 0xffffffff
li t1, 0x0000001f
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1211
li t0, 0xffffffff
li t1, 0x00000020
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1212
li t0, 0xffffffff
li t1, 0x7fffffff
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1213
li t0, 0xffffffff
li t1, 0x80000000
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1214
li t0, 0xffffffff
li t1, 0xfffffffe
div t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1215
li t0, 0xffffffff
li t1, 0xffffffff
div t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1216
li t0, 0x00000000
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1217
li t0, 0x00000000
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1218
li t0, 0x00000000
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1219
li t0, 0x00000000
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1220
li t0, 0x00000000
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1221
li t0, 0x00000000
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1222
li t0, 0x00000000
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1223
li t0, 0x00000000
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1224
li t0, 0x00000000
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1225
li t0, 0x00000001
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1226
li t0, 0x00000001
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1227
li t0, 0x00000001
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1228
li t0, 0x00000001
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1229
li t0, 0x00000001
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1230
li t0, 0x00000001
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1231
li t0, 0x00000001
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1232
li t0, 0x00000001
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1233
li t0, 0x00000001
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1234
li t0, 0x00000002
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1235
li t0, 0x00000002
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1236
li t0, 0x00000002
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1237
li t0, 0x00000002
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1238
li t0, 0x00000002
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1239
li t0, 0x00000002
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1240
li t0, 0x00000002
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1241
li t0, 0x00000002
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1242
li t0, 0x00000002
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1243
li t0, 0x0000001f
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1244
li t0, 0x0000001f
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1245
li t0, 0x0000001f
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x0000000f
bne t6, t2, fail
li a0, 1246
li t0, 0x0000001f
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1247
li t0, 0x0000001f
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1248
li t0, 0x0000001f
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1249
li t0, 0x0000001f
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1250
li t0, 0x0000001f
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1251
li t0, 0x0000001f
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1252
li t0, 0x00000020
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1253
li t0, 0x00000020
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1254
li t0, 0x00000020
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x00000010
bne t6, t2, fail
li a0, 1255
li t0, 0x00000020
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1256
li t0, 0x00000020
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1257
li t0, 0x00000020
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1258
li t0, 0x00000020
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1259
li t0, 0x00000020
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1260
li t0, 0x00000020
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1261
li t0, 0x7fffffff
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1262
li t0, 0x7fffffff
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1263
li t0, 0x7fffffff
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x3fffffff
bne t6, t2, fail
li a0, 1264
li t0, 0x7fffffff
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x04210842
bne t6, t2, fail
li a0, 1265
li t0, 0x7fffffff
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x03ffffff
bne t6, t2, fail
li a0, 1266
li t0, 0x7fffffff
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1267
li t0, 0x7fffffff
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1268
li t0, 0x7fffffff
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1269
li t0, 0x7fffffff
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1270
li t0, 0x80000000
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1271
li t0, 0x80000000
li t1, 0x00000001
divu t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1272
li t0, 0x80000000
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x40000000
bne t6, t2, fail
li a0, 1273
li t0, 0x80000000
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x04210842
bne t6, t2, fail
li a0, 1274
li t0, 0x80000000
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x04000000
bne t6, t2, fail
li a0, 1275
li t0, 0x80000000
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1276
li t0, 0x80000000
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1277
li t0, 0x80000000
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1278
li t0, 0x80000000
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1279
li t0, 0xfffffffe
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1280
li t0, 0xfffffffe
li t1, 0x00000001
divu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1281
li t0, 0xfffffffe
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1282
li t0, 0xfffffffe
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x08421084
bne t6, t2, fail
li a0, 1283
li t0, 0xfffffffe
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x07ffffff
bne t6, t2, fail
li a0, 1284
li t0, 0xfffffffe
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1285
li t0, 0xfffffffe
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1286
li t0, 0xfffffffe
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1287
li t0, 0xfffffffe
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1288
li t0, 0xffffffff
li t1, 0x00000000
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1289
li t0, 0xffffffff
li t1, 0x00000001
divu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1290
li t0, 0xffffffff
li t1, 0x00000002
divu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1291
li t0, 0xffffffff
li t1, 0x0000001f
divu t6,t0,t1
li t2, 0x08421084
bne t6, t2, fail
li a0, 1292
li t0, 0xffffffff
li t1, 0x00000020
divu t6,t0,t1
li t2, 0x07ffffff
bne t6, t2, fail
li a0, 1293
li t0, 0xffffffff
li t1, 0x7fffffff
divu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1294
li t0, 0xffffffff
li t1, 0x80000000
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1295
li t0, 0xffffffff
li t1, 0xfffffffe
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1296
li t0, 0xffffffff
li t1, 0xffffffff
divu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1297
li t0, 0x00000000
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1298
li t0, 0x00000000
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1299
li t0, 0x00000000
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1300
li t0, 0x00000000
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1301
li t0, 0x00000000
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1302
li t0, 0x00000000
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1303
li t0, 0x00000000
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1304
li t0, 0x00000000
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1305
li t0, 0x00000000
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1306
li t0, 0x00000001
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1307
li t0, 0x00000001
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1308
li t0, 0x00000001
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1309
li t0, 0x00000001
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1310
li t0, 0x00000001
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1311
li t0, 0x00000001
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1312
li t0, 0x00000001
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1313
li t0, 0x00000001
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1314
li t0, 0x00000001
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1315
li t0, 0x00000002
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1316
li t0, 0x00000002
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1317
li t0, 0x00000002
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1318
li t0, 0x00000002
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1319
li t0, 0x00000002
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1320
li t0, 0x00000002
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1321
li t0, 0x00000002
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1322
li t0, 0x00000002
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1323
li t0, 0x00000002
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1324
li t0, 0x0000001f
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1325
li t0, 0x0000001f
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1326
li t0, 0x0000001f
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1327
li t0, 0x0000001f
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1328
li t0, 0x0000001f
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1329
li t0, 0x0000001f
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1330
li t0, 0x0000001f
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1331
li t0, 0x0000001f
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1332
li t0, 0x0000001f
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1333
li t0, 0x00000020
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1334
li t0, 0x00000020
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1335
li t0, 0x00000020
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1336
li t0, 0x00000020
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1337
li t0, 0x00000020
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1338
li t0, 0x00000020
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1339
li t0, 0x00000020
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1340
li t0, 0x00000020
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1341
li t0, 0x00000020
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1342
li t0, 0x7fffffff
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1343
li t0, 0x7fffffff
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1344
li t0, 0x7fffffff
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1345
li t0, 0x7fffffff
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1346
li t0, 0x7fffffff
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1347
li t0, 0x7fffffff
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1348
li t0, 0x7fffffff
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1349
li t0, 0x7fffffff
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1350
li t0, 0x7fffffff
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1351
li t0, 0x80000000
li t1, 0x00000000
rem t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1352
li t0, 0x80000000
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1353
li t0, 0x80000000
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1354
li t0, 0x80000000
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1355
li t0, 0x80000000
li t1, 0x00000020
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1356
li t0, 0x80000000
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1357
li t0, 0x80000000
li t1, 0x80000000
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1358
li t0, 0x80000000
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1359
li t0, 0x80000000
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1360
li t0, 0xfffffffe
li t1, 0x00000000
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1361
li t0, 0xfffffffe
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1362
li t0, 0xfffffffe
li t1, 0x00000002
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1363
li t0, 0xfffffffe
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1364
li t0, 0xfffffffe
li t1, 0x00000020
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1365
li t0, 0xfffffffe
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1366
li t0, 0xfffffffe
li t1, 0x80000000
rem t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1367
li t0, 0xfffffffe
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1368
li t0, 0xfffffffe
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1369
li t0, 0xffffffff
li t1, 0x00000000
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1370
li t0, 0xffffffff
li t1, 0x00000001
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1371
li t0, 0xffffffff
li t1, 0x00000002
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1372
li t0, 0xffffffff
li t1, 0x0000001f
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1373
li t0, 0xffffffff
li t1, 0x00000020
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1374
li t0, 0xffffffff
li t1, 0x7fffffff
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1375
li t0, 0xffffffff
li t1, 0x80000000
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1376
li t0, 0xffffffff
li t1, 0xfffffffe
rem t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1377
li t0, 0xffffffff
li t1, 0xffffffff
rem t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1378
li t0, 0x00000000
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1379
li t0, 0x00000000
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1380
li t0, 0x00000000
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1381
li t0, 0x00000000
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1382
li t0, 0x00000000
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1383
li t0, 0x00000000
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1384
li t0, 0x00000000
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1385
li t0, 0x00000000
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1386
li t0, 0x00000000
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1387
li t0, 0x00000001
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1388
li t0, 0x00000001
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1389
li t0, 0x00000001
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1390
li t0, 0x00000001
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1391
li t0, 0x00000001
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1392
li t0, 0x00000001
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1393
li t0, 0x00000001
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1394
li t0, 0x00000001
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1395
li t0, 0x00000001
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1396
li t0, 0x00000002
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1397
li t0, 0x00000002
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1398
li t0, 0x00000002
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1399
li t0, 0x00000002
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1400
li t0, 0x00000002
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1401
li t0, 0x00000002
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1402
li t0, 0x00000002
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1403
li t0, 0x00000002
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1404
li t0, 0x00000002
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1405
li t0, 0x0000001f
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1406
li t0, 0x0000001f
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1407
li t0, 0x0000001f
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1408
li t0, 0x0000001f
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1409
li t0, 0x0000001f
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1410
li t0, 0x0000001f
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1411
li t0, 0x0000001f
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1412
li t0, 0x0000001f
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1413
li t0, 0x0000001f
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1414
li t0, 0x00000020
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1415
li t0, 0x00000020
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1416
li t0, 0x00000020
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1417
li t0, 0x00000020
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1418
li t0, 0x00000020
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1419
li t0, 0x00000020
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1420
li t0, 0x00000020
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1421
li t0, 0x00000020
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1422
li t0, 0x00000020
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x00000020
bne t6, t2, fail
li a0, 1423
li t0, 0x7fffffff
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1424
li t0, 0x7fffffff
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1425
li t0, 0x7fffffff
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1426
li t0, 0x7fffffff
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1427
li t0, 0x7fffffff
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1428
li t0, 0x7fffffff
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1429
li t0, 0x7fffffff
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1430
li t0, 0x7fffffff
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1431
li t0, 0x7fffffff
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1432
li t0, 0x80000000
li t1, 0x00000000
remu t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1433
li t0, 0x80000000
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1434
li t0, 0x80000000
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1435
li t0, 0x80000000
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1436
li t0, 0x80000000
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1437
li t0, 0x80000000
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1438
li t0, 0x80000000
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1439
li t0, 0x80000000
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1440
li t0, 0x80000000
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x80000000
bne t6, t2, fail
li a0, 1441
li t0, 0xfffffffe
li t1, 0x00000000
remu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1442
li t0, 0xfffffffe
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1443
li t0, 0xfffffffe
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1444
li t0, 0xfffffffe
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000002
bne t6, t2, fail
li a0, 1445
li t0, 0xfffffffe
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x0000001e
bne t6, t2, fail
li a0, 1446
li t0, 0xfffffffe
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1447
li t0, 0xfffffffe
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x7ffffffe
bne t6, t2, fail
li a0, 1448
li t0, 0xfffffffe
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1449
li t0, 0xfffffffe
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0xfffffffe
bne t6, t2, fail
li a0, 1450
li t0, 0xffffffff
li t1, 0x00000000
remu t6,t0,t1
li t2, 0xffffffff
bne t6, t2, fail
li a0, 1451
li t0, 0xffffffff
li t1, 0x00000001
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1452
li t0, 0xffffffff
li t1, 0x00000002
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1453
li t0, 0xffffffff
li t1, 0x0000001f
remu t6,t0,t1
li t2, 0x00000003
bne t6, t2, fail
li a0, 1454
li t0, 0xffffffff
li t1, 0x00000020
remu t6,t0,t1
li t2, 0x0000001f
bne t6, t2, fail
li a0, 1455
li t0, 0xffffffff
li t1, 0x7fffffff
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1456
li t0, 0xffffffff
li t1, 0x80000000
remu t6,t0,t1
li t2, 0x7fffffff
bne t6, t2, fail
li a0, 1457
li t0, 0xffffffff
li t1, 0xfffffffe
remu t6,t0,t1
li t2, 0x00000001
bne t6, t2, fail
li a0, 1458
li t0, 0xffffffff
li t1, 0xffffffff
remu t6,t0,t1
li t2, 0x00000000
bne t6, t2, fail
li a0, 1459
li t0, 0x850a11d8
li t1, 0x9b7ed888
xor t0,t0,t1
li t2, 0x1e74c950
bne t0, t2, fail
li a0, 1460
li t0, 0xd5855103
li t1, 0xae967eab
rem t0,t0,t1
li t2, 0xd5855103
bne t0, t2, fail
li a0, 1461
li t0, 0xd04c8968
li t1, 0x28286c85
divu t0,t0,t1
li t2, 0x00000005
bne t0, t2, fail
li a0, 1462
li t0, 0x44d18fcc
li t1, 0xabc63f8c
mul t0,t0,t1
li t2, 0xb0c5d790
bne t0, t2, fail
li a0, 1463
li t0, 0x92ad9633
li t1, 0xe4946e0a
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1464
li t0, 0x1c1a7db6
li t1, 0xd55bafc4
sra t0,t0,t1
li t2, 0x01c1a7db
bne t0, t2, fail
li a0, 1465
li t0, 0x2449b3fb
li t1, 0x5bf4adcc
srl t0,t0,t1
li t2, 0x0002449b
bne t0, t2, fail
li a0, 1466
li t0, 0x5f8d0531
li t1, 0x45ba3386
mulh t0,t0,t1
li t2, 0x1a068217
bne t0, t2, fail
li a0, 1467
li t0, 0x4b7fca0e
li t1, 0x0fd85fba
or t0,t0,t1
li t2, 0x4fffdfbe
bne t0, t2, fail
li a0, 1468
li t0, 0xddbc4a3b
li t1, 0xd0d8e741
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1469
li t0, 0x6450a295
li t1, 0x172aa0d2
rem t0,t0,t1
li t2, 0x07a61f4d
bne t0, t2, fail
li a0, 1470
li t0, 0x4a49e5d4
li t1, 0x0bd17ca1
and t0,t0,t1
li t2, 0x0a416480
bne t0, t2, fail
li a0, 1471
li t0, 0x38e4bce8
li t1, 0xf1ab4b7a
sll t0,t0,t1
li t2, 0xa0000000
bne t0, t2, fail
li a0, 1472
li t0, 0x1ff68cf1
li t1, 0xe404e71b
remu t0,t0,t1
li t2, 0x1ff68cf1
bne t0, t2, fail
li a0, 1473
li t0, 0xd3a644f9
li t1, 0xa1cfadf6
sll t0,t0,t1
li t2, 0x3e400000
bne t0, t2, fail
li a0, 1474
li t0, 0x4dbcea30
li t1, 0x074718fa
sll t0,t0,t1
li t2, 0xc0000000
bne t0, t2, fail
li a0, 1475
li t0, 0x02b9ae5c
li t1, 0xf47de450
xor t0,t0,t1
li t2, 0xf6c44a0c
bne t0, t2, fail
li a0, 1476
li t0, 0x8e85452e
li t1, 0x0c843013
srl t0,t0,t1
li t2, 0x000011d0
bne t0, t2, fail
li a0, 1477
li t0, 0x0079fffe
li t1, 0xa2a4b506
mulh t0,t0,t1
li t2, 0xffd3827e
bne t0, t2, fail
li a0, 1478
li t0, 0x4a84334d
li t1, 0x5a7ad923
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1479
li t0, 0x36687a54
li t1, 0x2ed12d2b
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1480
li t0, 0x9f0f5ea6
li t1, 0x51720fcd
mulh t0,t0,t1
li t2, 0xe128abce
bne t0, t2, fail
li a0, 1481
li t0, 0xd9373a28
li t1, 0x1ef6f03d
xor t0,t0,t1
li t2, 0xc7c1ca15
bne t0, t2, fail
li a0, 1482
li t0, 0xcd206c68
li t1, 0xb2b47c48
remu t0,t0,t1
li t2, 0x1a6bf020
bne t0, t2, fail
li a0, 1483
li t0, 0x20b92cc0
li t1, 0x39f67f88
remu t0,t0,t1
li t2, 0x20b92cc0
bne t0, t2, fail
li a0, 1484
li t0, 0x744313d9
li t1, 0x4bcf9e5a
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1485
li t0, 0x3001e679
li t1, 0x190e5424
xor t0,t0,t1
li t2, 0x290fb25d
bne t0, t2, fail
li a0, 1486
li t0, 0x8f267ce8
li t1, 0x270aa846
add t0,t0,t1
li t2, 0xb631252e
bne t0, t2, fail
li a0, 1487
li t0, 0x6dc74fa3
li t1, 0x3ac5ff84
or t0,t0,t1
li t2, 0x7fc7ffa7
bne t0, t2, fail
li a0, 1488
li t0, 0xd1ce6a88
li t1, 0x11c19be2
sub t0,t0,t1
li t2, 0xc00ccea6
bne t0, t2, fail
li a0, 1489
li t0, 0xe58c9da1
li t1, 0x422f7c6f
or t0,t0,t1
li t2, 0xe7affdef
bne t0, t2, fail
li a0, 1490
li t0, 0xa5d92466
li t1, 0x60af67c5
xor t0,t0,t1
li t2, 0xc57643a3
bne t0, t2, fail
li a0, 1491
li t0, 0x6434a2aa
li t1, 0xf30b1770
mulhu t0,t0,t1
li t2, 0x5f224dd6
bne t0, t2, fail
li a0, 1492
li t0, 0xf6146137
li t1, 0x0d860c4c
sll t0,t0,t1
li t2, 0x46137000
bne t0, t2, fail
li a0, 1493
li t0, 0xc97ae514
li t1, 0x04372452
divu t0,t0,t1
li t2, 0x0000002f
bne t0, t2, fail
li a0, 1494
li t0, 0x73d62504
li t1, 0xf1378012
remu t0,t0,t1
li t2, 0x73d62504
bne t0, t2, fail
li a0, 1495
li t0, 0x0806f756
li t1, 0xe024cf82
sra t0,t0,t1
li t2, 0x0201bdd5
bne t0, t2, fail
li a0, 1496
li t0, 0xe1d6457f
li t1, 0x0481e1b5
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1497
li t0, 0x688a39f2
li t1, 0x5a2676e6
remu t0,t0,t1
li t2, 0x0e63c30c
bne t0, t2, fail
li a0, 1498
li t0, 0xc3eca6e3
li t1, 0x89deafe1
mul t0,t0,t1
li t2, 0x2cedda83
bne t0, t2, fail
li a0, 1499
li t0, 0x12447568
li t1, 0x33bbe672
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1500
li t0, 0xe12ef981
li t1, 0x6c30d12e
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1501
li t0, 0x5383f688
li t1, 0x24d2458c
or t0,t0,t1
li t2, 0x77d3f78c
bne t0, t2, fail
li a0, 1502
li t0, 0x047880b2
li t1, 0xa65201bf
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1503
li t0, 0x84ce2e1e
li t1, 0x12b5214d
sra t0,t0,t1
li t2, 0xfffc2671
bne t0, t2, fail
li a0, 1504
li t0, 0x62ac519d
li t1, 0xd9850813
mul t0,t0,t1
li t2, 0x30e7f6a7
bne t0, t2, fail
li a0, 1505
li t0, 0x393c93dc
li t1, 0x6677d879
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1506
li t0, 0xb86f4611
li t1, 0x4f740a03
sll t0,t0,t1
li t2, 0xc37a3088
bne t0, t2, fail
li a0, 1507
li t0, 0x0f974ca8
li t1, 0x35440dad
mul t0,t0,t1
li t2, 0x5cc35588
bne t0, t2, fail
li a0, 1508
li t0, 0xfec508a4
li t1, 0x079526d2
sra t0,t0,t1
li t2, 0xffffffb1
bne t0, t2, fail
li a0, 1509
li t0, 0x2a8761f3
li t1, 0x364071d6
mulh t0,t0,t1
li t2, 0x0903436b
bne t0, t2, fail
li a0, 1510
li t0, 0x842de7cd
li t1, 0xc8177d51
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1511
li t0, 0x8cae54d1
li t1, 0xfc97a035
and t0,t0,t1
li t2, 0x8c860011
bne t0, t2, fail
li a0, 1512
li t0, 0xe19877cc
li t1, 0x0b2d549e
sub t0,t0,t1
li t2, 0xd66b232e
bne t0, t2, fail
li a0, 1513
li t0, 0xa29424ec
li t1, 0x4282ad11
sll t0,t0,t1
li t2, 0x49d80000
bne t0, t2, fail
li a0, 1514
li t0, 0x45e6ac4c
li t1, 0x3ee80f06
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1515
li t0, 0xb59a43c3
li t1, 0x7b7750f1
or t0,t0,t1
li t2, 0xffff53f3
bne t0, t2, fail
li a0, 1516
li t0, 0xae756669
li t1, 0xe7372606
sll t0,t0,t1
li t2, 0x9d599a40
bne t0, t2, fail
li a0, 1517
li t0, 0x7053205f
li t1, 0x607e027c
sll t0,t0,t1
li t2, 0xf0000000
bne t0, t2, fail
li a0, 1518
li t0, 0x34cd2672
li t1, 0x3a36e0af
and t0,t0,t1
li t2, 0x30042022
bne t0, t2, fail
li a0, 1519
li t0, 0xd59520e3
li t1, 0x08945a85
div t0,t0,t1
li t2, 0xfffffffc
bne t0, t2, fail
li a0, 1520
li t0, 0x44adc51d
li t1, 0xea7461aa
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1521
li t0, 0x9c4f19e7
li t1, 0x6d0ed030
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1522
li t0, 0x5b6bab54
li t1, 0x79d04fed
and t0,t0,t1
li t2, 0x59400b44
bne t0, t2, fail
li a0, 1523
li t0, 0x41b34dc8
li t1, 0xdd3f6b4b
add t0,t0,t1
li t2, 0x1ef2b913
bne t0, t2, fail
li a0, 1524
li t0, 0x2401f323
li t1, 0x60ddc753
mul t0,t0,t1
li t2, 0x35d90959
bne t0, t2, fail
li a0, 1525
li t0, 0xa860f789
li t1, 0x332fb18c
mul t0,t0,t1
li t2, 0xdd5417ec
bne t0, t2, fail
li a0, 1526
li t0, 0xa8d3377f
li t1, 0x8acb1110
sll t0,t0,t1
li t2, 0x377f0000
bne t0, t2, fail
li a0, 1527
li t0, 0x36625e5f
li t1, 0xdbf5ccd7
sra t0,t0,t1
li t2, 0x0000006c
bne t0, t2, fail
li a0, 1528
li t0, 0xea756e20
li t1, 0xc8d6e918
mulhsu t0,t0,t1
li t2, 0xef19a895
bne t0, t2, fail
li a0, 1529
li t0, 0xc3b18b71
li t1, 0x62a80a21
remu t0,t0,t1
li t2, 0x61098150
bne t0, t2, fail
li a0, 1530
li t0, 0xfe5432f3
li t1, 0xca711dfc
rem t0,t0,t1
li t2, 0xfe5432f3
bne t0, t2, fail
li a0, 1531
li t0, 0x3ba9639d
li t1, 0x83537777
xor t0,t0,t1
li t2, 0xb8fa14ea
bne t0, t2, fail
li a0, 1532
li t0, 0x9470ab84
li t1, 0x933dbea5
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1533
li t0, 0xf8399aff
li t1, 0xac324f12
mulhu t0,t0,t1
li t2, 0xa6f77c0e
bne t0, t2, fail
li a0, 1534
li t0, 0x6063117f
li t1, 0xa6b6c943
mulh t0,t0,t1
li t2, 0xde61fe0e
bne t0, t2, fail
li a0, 1535
li t0, 0x5dbe765c
li t1, 0x28d001e4
or t0,t0,t1
li t2, 0x7dfe77fc
bne t0, t2, fail
li a0, 1536
li t0, 0x7b3691b7
li t1, 0x77cb1a6b
xor t0,t0,t1
li t2, 0x0cfd8bdc
bne t0, t2, fail
li a0, 1537
li t0, 0xaaaf2bed
li t1, 0xdd30adfc
add t0,t0,t1
li t2, 0x87dfd9e9
bne t0, t2, fail
li a0, 1538
li t0, 0x1a640084
li t1, 0xb2a705c0
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1539
li t0, 0x30312c56
li t1, 0xbcf57697
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1540
li t0, 0x4ef38885
li t1, 0x1d7cf1b7
div t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1541
li t0, 0x815c5ff4
li t1, 0x76d7c6f6
mulh t0,t0,t1
li t2, 0xc535d662
bne t0, t2, fail
li a0, 1542
li t0, 0xc2519120
li t1, 0x3a59fa35
and t0,t0,t1
li t2, 0x02519020
bne t0, t2, fail
li a0, 1543
li t0, 0x3fa69f7a
li t1, 0xdb72900b
add t0,t0,t1
li t2, 0x1b192f85
bne t0, t2, fail
li a0, 1544
li t0, 0xb99ffb07
li t1, 0xa8b7a544
sra t0,t0,t1
li t2, 0xfb99ffb0
bne t0, t2, fail
li a0, 1545
li t0, 0x1134123b
li t1, 0x32df6575
mulhsu t0,t0,t1
li t2, 0x036b2ebc
bne t0, t2, fail
li a0, 1546
li t0, 0x828378ee
li t1, 0x43eee5f7
mulhu t0,t0,t1
li t2, 0x22a2341e
bne t0, t2, fail
li a0, 1547
li t0, 0x9a989d36
li t1, 0x4c7743bd
mulhu t0,t0,t1
li t2, 0x2e2d5485
bne t0, t2, fail
li a0, 1548
li t0, 0x65dbfcd0
li t1, 0x2988a14f
mul t0,t0,t1
li t2, 0x6761d430
bne t0, t2, fail
li a0, 1549
li t0, 0xbed10e33
li t1, 0xe440d895
sll t0,t0,t1
li t2, 0xc6600000
bne t0, t2, fail
li a0, 1550
li t0, 0x670b18fa
li t1, 0x47cc6b4f
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1551
li t0, 0xdb890e93
li t1, 0xebbe6116
mulhsu t0,t0,t1
li t2, 0xde6bb245
bne t0, t2, fail
li a0, 1552
li t0, 0x8fd44711
li t1, 0x9f8c3304
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1553
li t0, 0xfa305e27
li t1, 0xa72590b1
remu t0,t0,t1
li t2, 0x530acd76
bne t0, t2, fail
li a0, 1554
li t0, 0xf23f3c0e
li t1, 0x8ad5a2b4
mulhsu t0,t0,t1
li t2, 0xf88a9c3e
bne t0, t2, fail
li a0, 1555
li t0, 0x80287865
li t1, 0x49f8f442
mul t0,t0,t1
li t2, 0x0c074e0a
bne t0, t2, fail
li a0, 1556
li t0, 0x277171bd
li t1, 0x100ed71e
divu t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1557
li t0, 0xf6c84fa6
li t1, 0x57d2df5e
rem t0,t0,t1
li t2, 0xf6c84fa6
bne t0, t2, fail
li a0, 1558
li t0, 0x9ecd5351
li t1, 0xc23ea5ee
add t0,t0,t1
li t2, 0x610bf93f
bne t0, t2, fail
li a0, 1559
li t0, 0x6b8af1b9
li t1, 0xdc8a7376
srl t0,t0,t1
li t2, 0x000001ae
bne t0, t2, fail
li a0, 1560
li t0, 0x8569e071
li t1, 0xf67044be
srl t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1561
li t0, 0x6beb2be5
li t1, 0x389e1009
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1562
li t0, 0x10ee2dbf
li t1, 0x33758736
xor t0,t0,t1
li t2, 0x239baa89
bne t0, t2, fail
li a0, 1563
li t0, 0x245e0124
li t1, 0x9df801ef
srl t0,t0,t1
li t2, 0x000048bc
bne t0, t2, fail
li a0, 1564
li t0, 0x26806dd9
li t1, 0xebafc476
sub t0,t0,t1
li t2, 0x3ad0a963
bne t0, t2, fail
li a0, 1565
li t0, 0xf1daf1d6
li t1, 0x2b7784c9
mul t0,t0,t1
li t2, 0x26143906
bne t0, t2, fail
li a0, 1566
li t0, 0xf6e8db08
li t1, 0xff2f21bd
xor t0,t0,t1
li t2, 0x09c7fab5
bne t0, t2, fail
li a0, 1567
li t0, 0x2524286a
li t1, 0x0e1862ae
sll t0,t0,t1
li t2, 0x0a1a8000
bne t0, t2, fail
li a0, 1568
li t0, 0xba58172f
li t1, 0x55c1374c
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1569
li t0, 0x6381ec81
li t1, 0x288ee4e2
srl t0,t0,t1
li t2, 0x18e07b20
bne t0, t2, fail
li a0, 1570
li t0, 0xdafb1594
li t1, 0x81d93868
rem t0,t0,t1
li t2, 0xdafb1594
bne t0, t2, fail
li a0, 1571
li t0, 0xd3db2d18
li t1, 0xb646811f
and t0,t0,t1
li t2, 0x92420118
bne t0, t2, fail
li a0, 1572
li t0, 0xdb6fc11d
li t1, 0x83f34976
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1573
li t0, 0xd2e90203
li t1, 0x0df5be81
add t0,t0,t1
li t2, 0xe0dec084
bne t0, t2, fail
li a0, 1574
li t0, 0x8b8460b6
li t1, 0xf50f8876
sra t0,t0,t1
li t2, 0xfffffe2e
bne t0, t2, fail
li a0, 1575
li t0, 0x4abfaa72
li t1, 0x1735ccc7
remu t0,t0,t1
li t2, 0x051e441d
bne t0, t2, fail
li a0, 1576
li t0, 0x2802c9fb
li t1, 0x206ce379
mulh t0,t0,t1
li t2, 0x05115df9
bne t0, t2, fail
li a0, 1577
li t0, 0xc05a4bae
li t1, 0x47f62fe9
xor t0,t0,t1
li t2, 0x87ac6447
bne t0, t2, fail
li a0, 1578
li t0, 0x02dbfb45
li t1, 0x4f8be31d
remu t0,t0,t1
li t2, 0x02dbfb45
bne t0, t2, fail
li a0, 1579
li t0, 0xf49fd88e
li t1, 0x82d461e1
mulhsu t0,t0,t1
li t2, 0xfa2fbbfe
bne t0, t2, fail
li a0, 1580
li t0, 0x9b8cba8f
li t1, 0xdcb3ce76
rem t0,t0,t1
li t2, 0xe2251da3
bne t0, t2, fail
li a0, 1581
li t0, 0x462307fb
li t1, 0x83d5bd07
srl t0,t0,t1
li t2, 0x008c460f
bne t0, t2, fail
li a0, 1582
li t0, 0x958ebd6a
li t1, 0xaa31bd5f
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1583
li t0, 0x1d0e3366
li t1, 0xf9ebfdca
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1584
li t0, 0xeaf55cb7
li t1, 0x08988db1
or t0,t0,t1
li t2, 0xeafdddb7
bne t0, t2, fail
li a0, 1585
li t0, 0x84c95a6a
li t1, 0x59a964e3
div t0,t0,t1
li t2, 0xffffffff
bne t0, t2, fail
li a0, 1586
li t0, 0xf3bfa617
li t1, 0x437d93a1
add t0,t0,t1
li t2, 0x373d39b8
bne t0, t2, fail
li a0, 1587
li t0, 0x7e209e55
li t1, 0x017b3e39
mulhu t0,t0,t1
li t2, 0x00bad8f2
bne t0, t2, fail
li a0, 1588
li t0, 0x6aee4b0b
li t1, 0x1e13b9a7
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1589
li t0, 0x9a8696ef
li t1, 0xd62fd71b
sub t0,t0,t1
li t2, 0xc456bfd4
bne t0, t2, fail
li a0, 1590
li t0, 0x68c4873f
li t1, 0x245533ab
divu t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1591
li t0, 0x16857d1c
li t1, 0x8a1a75db
or t0,t0,t1
li t2, 0x9e9f7ddf
bne t0, t2, fail
li a0, 1592
li t0, 0xac84e4ab
li t1, 0xeb580d8f
sub t0,t0,t1
li t2, 0xc12cd71c
bne t0, t2, fail
li a0, 1593
li t0, 0x62a2794b
li t1, 0x016f971f
remu t0,t0,t1
li t2, 0x00fe550f
bne t0, t2, fail
li a0, 1594
li t0, 0xee822f93
li t1, 0x054d7485
sra t0,t0,t1
li t2, 0xff74117c
bne t0, t2, fail
li a0, 1595
li t0, 0xecd5b5f9
li t1, 0x1b10002d
xor t0,t0,t1
li t2, 0xf7c5b5d4
bne t0, t2, fail
li a0, 1596
li t0, 0x618f3c1f
li t1, 0xf8a44743
remu t0,t0,t1
li t2, 0x618f3c1f
bne t0, t2, fail
li a0, 1597
li t0, 0x7cc164aa
li t1, 0xb9ee8b7b
mulhu t0,t0,t1
li t2, 0x5a9c0183
bne t0, t2, fail
li a0, 1598
li t0, 0x8e9a7f98
li t1, 0x0f60195e
sra t0,t0,t1
li t2, 0xfffffffe
bne t0, t2, fail
li a0, 1599
li t0, 0x22d1ae62
li t1, 0x95ef7d60
srl t0,t0,t1
li t2, 0x22d1ae62
bne t0, t2, fail
li a0, 1600
li t0, 0x83eb4578
li t1, 0xda2d4594
remu t0,t0,t1
li t2, 0x83eb4578
bne t0, t2, fail
li a0, 1601
li t0, 0x42afdf04
li t1, 0x458f425c
remu t0,t0,t1
li t2, 0x42afdf04
bne t0, t2, fail
li a0, 1602
li t0, 0x8c41c38e
li t1, 0xf73c0d33
sra t0,t0,t1
li t2, 0xfffff188
bne t0, t2, fail
li a0, 1603
li t0, 0x4a9597f5
li t1, 0x325cb43e
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1604
li t0, 0x6616a55c
li t1, 0x611620cc
add t0,t0,t1
li t2, 0xc72cc628
bne t0, t2, fail
li a0, 1605
li t0, 0x0003b7c2
li t1, 0xe3c4bfa0
mul t0,t0,t1
li t2, 0x7ef49740
bne t0, t2, fail
li a0, 1606
li t0, 0xd17476bd
li t1, 0x540f824b
mulhsu t0,t0,t1
li t2, 0xf0b76518
bne t0, t2, fail
li a0, 1607
li t0, 0xca267357
li t1, 0x377a2fe3
sra t0,t0,t1
li t2, 0xf944ce6a
bne t0, t2, fail
li a0, 1608
li t0, 0x076bbab6
li t1, 0x53959f50
sra t0,t0,t1
li t2, 0x0000076b
bne t0, t2, fail
li a0, 1609
li t0, 0x35d16fea
li t1, 0x6cf7cd3c
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1610
li t0, 0x5666b719
li t1, 0x7a3223b5
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1611
li t0, 0x317a1cd6
li t1, 0x6955ef10
add t0,t0,t1
li t2, 0x9ad00be6
bne t0, t2, fail
li a0, 1612
li t0, 0xa1024ae0
li t1, 0x64a52e50
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1613
li t0, 0x96ad74ae
li t1, 0x0d507b3c
mulhsu t0,t0,t1
li t2, 0xfa85b26d
bne t0, t2, fail
li a0, 1614
li t0, 0x708b28e5
li t1, 0x551b84af
remu t0,t0,t1
li t2, 0x1b6fa436
bne t0, t2, fail
li a0, 1615
li t0, 0xda6c31cb
li t1, 0x17ac3b0f
sll t0,t0,t1
li t2, 0x18e58000
bne t0, t2, fail
li a0, 1616
li t0, 0x084b54c3
li t1, 0x362e1ac9
add t0,t0,t1
li t2, 0x3e796f8c
bne t0, t2, fail
li a0, 1617
li t0, 0xba319c1e
li t1, 0x14fb0738
or t0,t0,t1
li t2, 0xbefb9f3e
bne t0, t2, fail
li a0, 1618
li t0, 0x512c8044
li t1, 0xfffd431d
srl t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1619
li t0, 0x48653722
li t1, 0xe09e6f59
or t0,t0,t1
li t2, 0xe8ff7f7b
bne t0, t2, fail
li a0, 1620
li t0, 0x86d5cfd8
li t1, 0x3806a5dd
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1621
li t0, 0x463eec04
li t1, 0xf30bb15c
sll t0,t0,t1
li t2, 0x40000000
bne t0, t2, fail
li a0, 1622
li t0, 0x9930120d
li t1, 0xfd2d3822
mulhu t0,t0,t1
li t2, 0x977f90e0
bne t0, t2, fail
li a0, 1623
li t0, 0x952ebedb
li t1, 0xe6156c8d
rem t0,t0,t1
li t2, 0xfcd90ca7
bne t0, t2, fail
li a0, 1624
li t0, 0xa7a4d78f
li t1, 0xe1eadb6d
mulhsu t0,t0,t1
li t2, 0xb206d266
bne t0, t2, fail
li a0, 1625
li t0, 0x87ef5728
li t1, 0xb4fb3244
sub t0,t0,t1
li t2, 0xd2f424e4
bne t0, t2, fail
li a0, 1626
li t0, 0xae1f9d52
li t1, 0xe6dc321e
sub t0,t0,t1
li t2, 0xc7436b34
bne t0, t2, fail
li a0, 1627
li t0, 0x1a381f15
li t1, 0xd37792dc
xor t0,t0,t1
li t2, 0xc94f8dc9
bne t0, t2, fail
li a0, 1628
li t0, 0xe86d90e8
li t1, 0x24dec66f
add t0,t0,t1
li t2, 0x0d4c5757
bne t0, t2, fail
li a0, 1629
li t0, 0x71341800
li t1, 0x6f488891
remu t0,t0,t1
li t2, 0x01eb8f6f
bne t0, t2, fail
li a0, 1630
li t0, 0x02cad4fe
li t1, 0x2f729398
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1631
li t0, 0xc4d82b1f
li t1, 0x06fddfa1
divu t0,t0,t1
li t2, 0x0000001c
bne t0, t2, fail
li a0, 1632
li t0, 0x3e462ff2
li t1, 0x7235d910
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1633
li t0, 0xd4dbbbc8
li t1, 0x1b212b7e
xor t0,t0,t1
li t2, 0xcffa90b6
bne t0, t2, fail
li a0, 1634
li t0, 0xa7720de5
li t1, 0xb3f0184c
mulh t0,t0,t1
li t2, 0x1a4fa457
bne t0, t2, fail
li a0, 1635
li t0, 0xfbc83a3f
li t1, 0x26762f11
sll t0,t0,t1
li t2, 0x747e0000
bne t0, t2, fail
li a0, 1636
li t0, 0x1b9994c7
li t1, 0x08f92f8b
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1637
li t0, 0x7e7bad36
li t1, 0x169c8c89
remu t0,t0,t1
li t2, 0x0d6cee89
bne t0, t2, fail
li a0, 1638
li t0, 0x7e057bf9
li t1, 0x1298115f
mulhu t0,t0,t1
li t2, 0x09273e86
bne t0, t2, fail
li a0, 1639
li t0, 0x0fbc419b
li t1, 0x739d8f84
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1640
li t0, 0x35dc4ba6
li t1, 0xa8ec21ca
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1641
li t0, 0x44a5a455
li t1, 0x99032f32
sub t0,t0,t1
li t2, 0xaba27523
bne t0, t2, fail
li a0, 1642
li t0, 0x142bd260
li t1, 0xe5ac5454
mulh t0,t0,t1
li t2, 0xfdecf4e6
bne t0, t2, fail
li a0, 1643
li t0, 0x60a1f3b0
li t1, 0x68deb908
sra t0,t0,t1
li t2, 0x0060a1f3
bne t0, t2, fail
li a0, 1644
li t0, 0x16a519b5
li t1, 0x7a6594da
add t0,t0,t1
li t2, 0x910aae8f
bne t0, t2, fail
li a0, 1645
li t0, 0xdd5d9ad0
li t1, 0x9324ff57
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1646
li t0, 0x90aa9658
li t1, 0x13884f3f
mul t0,t0,t1
li t2, 0xa52027a8
bne t0, t2, fail
li a0, 1647
li t0, 0x286d7ef5
li t1, 0xce7cfcd4
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1648
li t0, 0x23c95167
li t1, 0xe92c13b0
add t0,t0,t1
li t2, 0x0cf56517
bne t0, t2, fail
li a0, 1649
li t0, 0xcddab552
li t1, 0x4dd621a5
divu t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1650
li t0, 0xa9f0bd24
li t1, 0x4f1d0d7f
srl t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1651
li t0, 0x36c2090b
li t1, 0x930cf719
remu t0,t0,t1
li t2, 0x36c2090b
bne t0, t2, fail
li a0, 1652
li t0, 0x2134c6bd
li t1, 0x07f6539e
add t0,t0,t1
li t2, 0x292b1a5b
bne t0, t2, fail
li a0, 1653
li t0, 0x8430d5a6
li t1, 0x5fa2ab7d
mulh t0,t0,t1
li t2, 0xd1bf733f
bne t0, t2, fail
li a0, 1654
li t0, 0x1ea3b669
li t1, 0x67cb8b15
or t0,t0,t1
li t2, 0x7febbf7d
bne t0, t2, fail
li a0, 1655
li t0, 0x1157cbde
li t1, 0x2c07d2d3
mul t0,t0,t1
li t2, 0x0bab23fa
bne t0, t2, fail
li a0, 1656
li t0, 0x31218920
li t1, 0x5f53b2bd
xor t0,t0,t1
li t2, 0x6e723b9d
bne t0, t2, fail
li a0, 1657
li t0, 0xd8c5b7d8
li t1, 0x2f4f17f0
and t0,t0,t1
li t2, 0x084517d0
bne t0, t2, fail
li a0, 1658
li t0, 0x6c52bbcf
li t1, 0xd1457251
sub t0,t0,t1
li t2, 0x9b0d497e
bne t0, t2, fail
li a0, 1659
li t0, 0xbc9e61a7
li t1, 0x5e0c700b
sub t0,t0,t1
li t2, 0x5e91f19c
bne t0, t2, fail
li a0, 1660
li t0, 0x1dd418e4
li t1, 0x84deee28
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1661
li t0, 0x488ed080
li t1, 0xe88360e2
mulh t0,t0,t1
li t2, 0xf957d8fe
bne t0, t2, fail
li a0, 1662
li t0, 0x8d986e3d
li t1, 0xdbdaf86f
mulhu t0,t0,t1
li t2, 0x799a8385
bne t0, t2, fail
li a0, 1663
li t0, 0xaf86827a
li t1, 0xf25d81c4
srl t0,t0,t1
li t2, 0x0af86827
bne t0, t2, fail
li a0, 1664
li t0, 0xd0a9a42d
li t1, 0xe8794a5a
xor t0,t0,t1
li t2, 0x38d0ee77
bne t0, t2, fail
li a0, 1665
li t0, 0xe122f4cd
li t1, 0xdc740784
sra t0,t0,t1
li t2, 0xfe122f4c
bne t0, t2, fail
li a0, 1666
li t0, 0xfc5cb8cb
li t1, 0x5ffd754c
sub t0,t0,t1
li t2, 0x9c5f437f
bne t0, t2, fail
li a0, 1667
li t0, 0x8c5661dd
li t1, 0x6d3683c9
and t0,t0,t1
li t2, 0x0c1601c9
bne t0, t2, fail
li a0, 1668
li t0, 0x9439bb50
li t1, 0xf9558529
mulh t0,t0,t1
li t2, 0x02ce6afc
bne t0, t2, fail
li a0, 1669
li t0, 0x29ddde48
li t1, 0x33065cee
or t0,t0,t1
li t2, 0x3bdfdeee
bne t0, t2, fail
li a0, 1670
li t0, 0x42bb21f3
li t1, 0x35eb966f
mul t0,t0,t1
li t2, 0x0e191a5d
bne t0, t2, fail
li a0, 1671
li t0, 0x31914a97
li t1, 0x72a67b05
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1672
li t0, 0x17bfe25a
li t1, 0x0b0bfb7e
srl t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1673
li t0, 0xd3c9ea17
li t1, 0x33c2052b
add t0,t0,t1
li t2, 0x078bef42
bne t0, t2, fail
li a0, 1674
li t0, 0x4350d10c
li t1, 0xc91dbad2
remu t0,t0,t1
li t2, 0x4350d10c
bne t0, t2, fail
li a0, 1675
li t0, 0xfbf484de
li t1, 0x8e2bfb9a
add t0,t0,t1
li t2, 0x8a208078
bne t0, t2, fail
li a0, 1676
li t0, 0x0164c3b6
li t1, 0x67198c61
rem t0,t0,t1
li t2, 0x0164c3b6
bne t0, t2, fail
li a0, 1677
li t0, 0xcd7870f4
li t1, 0x8e747a31
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1678
li t0, 0x832345f0
li t1, 0x58651830
sra t0,t0,t1
li t2, 0xffff8323
bne t0, t2, fail
li a0, 1679
li t0, 0x214d66dc
li t1, 0x097ea3f4
sra t0,t0,t1
li t2, 0x00000214
bne t0, t2, fail
li a0, 1680
li t0, 0x90495633
li t1, 0xf1fec65e
add t0,t0,t1
li t2, 0x82481c91
bne t0, t2, fail
li a0, 1681
li t0, 0x7eec602d
li t1, 0x25099c1f
sra t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1682
li t0, 0xbe01a135
li t1, 0x32bb16f3
mulhsu t0,t0,t1
li t2, 0xf2ec16c2
bne t0, t2, fail
li a0, 1683
li t0, 0xdcf49282
li t1, 0xf65bab73
rem t0,t0,t1
li t2, 0xf9e19029
bne t0, t2, fail
li a0, 1684
li t0, 0x86fd890d
li t1, 0xe1039fa8
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1685
li t0, 0x1b7deb69
li t1, 0xa3d71c11
mulhu t0,t0,t1
li t2, 0x119846a8
bne t0, t2, fail
li a0, 1686
li t0, 0x818017a3
li t1, 0xe1eed23d
sll t0,t0,t1
li t2, 0x60000000
bne t0, t2, fail
li a0, 1687
li t0, 0x1877b2ce
li t1, 0x5d7156c0
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1688
li t0, 0x768b401b
li t1, 0x71a6f5c7
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1689
li t0, 0x31d6ef25
li t1, 0x0e4154c0
divu t0,t0,t1
li t2, 0x00000003
bne t0, t2, fail
li a0, 1690
li t0, 0xcab9a820
li t1, 0x5cc70b6a
mulh t0,t0,t1
li t2, 0xecb14c5d
bne t0, t2, fail
li a0, 1691
li t0, 0xdded1714
li t1, 0x63e8723c
mulh t0,t0,t1
li t2, 0xf2b3bf95
bne t0, t2, fail
li a0, 1692
li t0, 0xa19d9a18
li t1, 0x6c1e1ec0
srl t0,t0,t1
li t2, 0xa19d9a18
bne t0, t2, fail
li a0, 1693
li t0, 0xda8e4f39
li t1, 0x6e0a95d2
mul t0,t0,t1
li t2, 0xb31329c2
bne t0, t2, fail
li a0, 1694
li t0, 0xd706c2c9
li t1, 0x612c0789
sra t0,t0,t1
li t2, 0xffeb8361
bne t0, t2, fail
li a0, 1695
li t0, 0xb2703687
li t1, 0x4f00746e
and t0,t0,t1
li t2, 0x02003406
bne t0, t2, fail
li a0, 1696
li t0, 0xf4a9ca3b
li t1, 0x94ddfb93
remu t0,t0,t1
li t2, 0x5fcbcea8
bne t0, t2, fail
li a0, 1697
li t0, 0x6d8d4fa1
li t1, 0x5a0e0c29
sub t0,t0,t1
li t2, 0x137f4378
bne t0, t2, fail
li a0, 1698
li t0, 0x4d6aa0dd
li t1, 0x7e0a1247
xor t0,t0,t1
li t2, 0x3360b29a
bne t0, t2, fail
li a0, 1699
li t0, 0xbeb033bd
li t1, 0xae6270ff
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1700
li t0, 0x56b289ff
li t1, 0x58cafd56
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1701
li t0, 0xfcb5ed09
li t1, 0xf3a98126
mul t0,t0,t1
li t2, 0x3563b856
bne t0, t2, fail
li a0, 1702
li t0, 0x7bed8bc1
li t1, 0x875935a1
mulhsu t0,t0,t1
li t2, 0x4185743e
bne t0, t2, fail
li a0, 1703
li t0, 0xf4fab360
li t1, 0xfa5d27ba
xor t0,t0,t1
li t2, 0x0ea794da
bne t0, t2, fail
li a0, 1704
li t0, 0xd0d225bc
li t1, 0xdbbe2052
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1705
li t0, 0xe4c505dd
li t1, 0x7bbe9808
sll t0,t0,t1
li t2, 0xc505dd00
bne t0, t2, fail
li a0, 1706
li t0, 0x708fcdf4
li t1, 0x52fdb4d5
sub t0,t0,t1
li t2, 0x1d92191f
bne t0, t2, fail
li a0, 1707
li t0, 0xee9c082b
li t1, 0xf6ac2e5e
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1708
li t0, 0x0e22929a
li t1, 0x2413ed94
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1709
li t0, 0x471277bb
li t1, 0x2f76a0ff
mulhsu t0,t0,t1
li t2, 0x0d2d5330
bne t0, t2, fail
li a0, 1710
li t0, 0x566363e0
li t1, 0x2ebebc60
mul t0,t0,t1
li t2, 0xc2ddf400
bne t0, t2, fail
li a0, 1711
li t0, 0xcb40dcfb
li t1, 0x06c7f7f7
mulhsu t0,t0,t1
li t2, 0xfe9a5182
bne t0, t2, fail
li a0, 1712
li t0, 0xe0c8989e
li t1, 0x6502cce9
mulhu t0,t0,t1
li t2, 0x58b199b3
bne t0, t2, fail
li a0, 1713
li t0, 0xa08a361c
li t1, 0x07e48721
mulhsu t0,t0,t1
li t2, 0xfd0e902f
bne t0, t2, fail
li a0, 1714
li t0, 0xfd1df7bd
li t1, 0x8e7e17ea
sll t0,t0,t1
li t2, 0x77def400
bne t0, t2, fail
li a0, 1715
li t0, 0xac826086
li t1, 0xb03c52db
sll t0,t0,t1
li t2, 0x30000000
bne t0, t2, fail
li a0, 1716
li t0, 0xdcd4ab46
li t1, 0x5bbc9bcf
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1717
li t0, 0xc61dd23d
li t1, 0xd0a5a824
and t0,t0,t1
li t2, 0xc0058024
bne t0, t2, fail
li a0, 1718
li t0, 0x25f454ab
li t1, 0x821bd967
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1719
li t0, 0x596a156b
li t1, 0x376a04d2
remu t0,t0,t1
li t2, 0x22001099
bne t0, t2, fail
li a0, 1720
li t0, 0x9d8afde4
li t1, 0x4bb180ce
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1721
li t0, 0x74933352
li t1, 0xedb020d6
mulh t0,t0,t1
li t2, 0xf7a94758
bne t0, t2, fail
li a0, 1722
li t0, 0x40fb6079
li t1, 0x6732075c
sll t0,t0,t1
li t2, 0x90000000
bne t0, t2, fail
li a0, 1723
li t0, 0x23647234
li t1, 0xd01543d8
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1724
li t0, 0x0fb8cc1e
li t1, 0x9becd44b
xor t0,t0,t1
li t2, 0x94541855
bne t0, t2, fail
li a0, 1725
li t0, 0x454d0977
li t1, 0x805ec837
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1726
li t0, 0x23efebd4
li t1, 0x03b29035
sub t0,t0,t1
li t2, 0x203d5b9f
bne t0, t2, fail
li a0, 1727
li t0, 0xd2995f25
li t1, 0xb1b3c0dd
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1728
li t0, 0x94d9607a
li t1, 0xa7dd0ae6
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1729
li t0, 0x1a23fb80
li t1, 0xef907cb4
mul t0,t0,t1
li t2, 0xc71ed600
bne t0, t2, fail
li a0, 1730
li t0, 0x8239668f
li t1, 0x1aa1c92e
sll t0,t0,t1
li t2, 0x59a3c000
bne t0, t2, fail
li a0, 1731
li t0, 0xaf6bfc1a
li t1, 0xd8575c25
sll t0,t0,t1
li t2, 0xed7f8340
bne t0, t2, fail
li a0, 1732
li t0, 0x6f1a1e16
li t1, 0xb31d0a5b
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1733
li t0, 0x444c12c1
li t1, 0x5d366c8b
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1734
li t0, 0xdeccd249
li t1, 0x03ec9f19
remu t0,t0,t1
li t2, 0x030a04d1
bne t0, t2, fail
li a0, 1735
li t0, 0x7c60dce8
li t1, 0xbe5ee0c3
srl t0,t0,t1
li t2, 0x0f8c1b9d
bne t0, t2, fail
li a0, 1736
li t0, 0x89e16c9f
li t1, 0x78720d2a
xor t0,t0,t1
li t2, 0xf19361b5
bne t0, t2, fail
li a0, 1737
li t0, 0x871238d4
li t1, 0xcb621a0c
mulhu t0,t0,t1
li t2, 0x6b4f35c8
bne t0, t2, fail
li a0, 1738
li t0, 0x962347af
li t1, 0xe9c0686f
div t0,t0,t1
li t2, 0x00000004
bne t0, t2, fail
li a0, 1739
li t0, 0x063ed180
li t1, 0xc71a9ca0
mulh t0,t0,t1
li t2, 0xfe9ca98d
bne t0, t2, fail
li a0, 1740
li t0, 0xa28dbcf2
li t1, 0x7c871870
sra t0,t0,t1
li t2, 0xffffa28d
bne t0, t2, fail
li a0, 1741
li t0, 0x1e00c97b
li t1, 0x330ef1a5
or t0,t0,t1
li t2, 0x3f0ef9ff
bne t0, t2, fail
li a0, 1742
li t0, 0x97e3aaa7
li t1, 0x110512d3
mulhsu t0,t0,t1
li t2, 0xf9140e1f
bne t0, t2, fail
li a0, 1743
li t0, 0xc61f8a53
li t1, 0x30fe7287
sra t0,t0,t1
li t2, 0xff8c3f14
bne t0, t2, fail
li a0, 1744
li t0, 0x24c3fff0
li t1, 0x199a9aa4
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1745
li t0, 0x11609378
li t1, 0xc79a9d48
add t0,t0,t1
li t2, 0xd8fb30c0
bne t0, t2, fail
li a0, 1746
li t0, 0x7847d7a6
li t1, 0x75049aae
mul t0,t0,t1
li t2, 0x35266ed4
bne t0, t2, fail
li a0, 1747
li t0, 0xa7a01361
li t1, 0xcd6c0ebb
mulhsu t0,t0,t1
li t2, 0xb915e1f7
bne t0, t2, fail
li a0, 1748
li t0, 0x2dad0eca
li t1, 0x9f46ae41
sra t0,t0,t1
li t2, 0x16d68765
bne t0, t2, fail
li a0, 1749
li t0, 0x9f725d4b
li t1, 0x51cf2955
div t0,t0,t1
li t2, 0xffffffff
bne t0, t2, fail
li a0, 1750
li t0, 0xfd97f6a6
li t1, 0x4604c243
mulh t0,t0,t1
li t2, 0xff5781fd
bne t0, t2, fail
li a0, 1751
li t0, 0x78167855
li t1, 0x44d9ea3f
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1752
li t0, 0xb37f26ff
li t1, 0xb9a2be6c
mul t0,t0,t1
li t2, 0x0cf3b594
bne t0, t2, fail
li a0, 1753
li t0, 0x6b55eeca
li t1, 0x92631291
and t0,t0,t1
li t2, 0x02410280
bne t0, t2, fail
li a0, 1754
li t0, 0xc14aa23f
li t1, 0x7dda4cca
and t0,t0,t1
li t2, 0x414a000a
bne t0, t2, fail
li a0, 1755
li t0, 0xbb777432
li t1, 0x97d4f456
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1756
li t0, 0x37e1e925
li t1, 0xe0e446c4
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1757
li t0, 0x8d0229c0
li t1, 0x7258a8fd
or t0,t0,t1
li t2, 0xff5aa9fd
bne t0, t2, fail
li a0, 1758
li t0, 0x131ef719
li t1, 0x53c00c04
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1759
li t0, 0xd496cac8
li t1, 0x7d5bee5d
remu t0,t0,t1
li t2, 0x573adc6b
bne t0, t2, fail
li a0, 1760
li t0, 0x41827f99
li t1, 0x91c666a9
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1761
li t0, 0xe5c43c75
li t1, 0x74b43447
xor t0,t0,t1
li t2, 0x91700832
bne t0, t2, fail
li a0, 1762
li t0, 0x0ff17765
li t1, 0x7944d347
sll t0,t0,t1
li t2, 0xf8bbb280
bne t0, t2, fail
li a0, 1763
li t0, 0x0c83f376
li t1, 0xc00028a8
or t0,t0,t1
li t2, 0xcc83fbfe
bne t0, t2, fail
li a0, 1764
li t0, 0xa8af00b2
li t1, 0x4d0926a8
and t0,t0,t1
li t2, 0x080900a0
bne t0, t2, fail
li a0, 1765
li t0, 0xca9c982e
li t1, 0xfe608ee4
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1766
li t0, 0x6798fa24
li t1, 0x3406e320
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1767
li t0, 0xf63f8d0b
li t1, 0x037a82f6
or t0,t0,t1
li t2, 0xf77f8fff
bne t0, t2, fail
li a0, 1768
li t0, 0x1f08fed8
li t1, 0x3ec86ddd
sll t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1769
li t0, 0x8baac2cf
li t1, 0x73ae6a8b
mulhsu t0,t0,t1
li t2, 0xcb6e7328
bne t0, t2, fail
li a0, 1770
li t0, 0xf11cd0a1
li t1, 0x55d6316f
mul t0,t0,t1
li t2, 0xeb0346cf
bne t0, t2, fail
li a0, 1771
li t0, 0x2656ff99
li t1, 0x610f92b2
rem t0,t0,t1
li t2, 0x2656ff99
bne t0, t2, fail
li a0, 1772
li t0, 0xdf1dc5eb
li t1, 0x856d1092
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1773
li t0, 0x46b239a6
li t1, 0x8ca6a243
rem t0,t0,t1
li t2, 0x46b239a6
bne t0, t2, fail
li a0, 1774
li t0, 0xbad4bbec
li t1, 0x2ebea607
remu t0,t0,t1
li t2, 0x2e98c9d7
bne t0, t2, fail
li a0, 1775
li t0, 0x8ff02c71
li t1, 0x609c39cf
mulhsu t0,t0,t1
li t2, 0xd5b5adb7
bne t0, t2, fail
li a0, 1776
li t0, 0xc3d187d5
li t1, 0x046ffdef
srl t0,t0,t1
li t2, 0x000187a3
bne t0, t2, fail
li a0, 1777
li t0, 0x5382c3b0
li t1, 0x1ca73a5e
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1778
li t0, 0xbf1c24e5
li t1, 0xd1504501
rem t0,t0,t1
li t2, 0xedcbdfe4
bne t0, t2, fail
li a0, 1779
li t0, 0x7a21d746
li t1, 0x51ca0c2c
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1780
li t0, 0xdecaf78e
li t1, 0xd77302fd
sra t0,t0,t1
li t2, 0xfffffffe
bne t0, t2, fail
li a0, 1781
li t0, 0x932638b4
li t1, 0xe3dc021c
mulh t0,t0,t1
li t2, 0x0bf71f86
bne t0, t2, fail
li a0, 1782
li t0, 0x04165f8c
li t1, 0xaff32665
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1783
li t0, 0x0688bf73
li t1, 0x7c57defd
mul t0,t0,t1
li t2, 0xcf3feea7
bne t0, t2, fail
li a0, 1784
li t0, 0xc6e42fc4
li t1, 0x40648e60
and t0,t0,t1
li t2, 0x40640e40
bne t0, t2, fail
li a0, 1785
li t0, 0x31730561
li t1, 0x9b27b098
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1786
li t0, 0x469d197f
li t1, 0x1acb0da2
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1787
li t0, 0x3dc8952d
li t1, 0x8bf1ae59
or t0,t0,t1
li t2, 0xbff9bf7d
bne t0, t2, fail
li a0, 1788
li t0, 0xfde84ad7
li t1, 0x8a1deaa8
sra t0,t0,t1
li t2, 0xfffde84a
bne t0, t2, fail
li a0, 1789
li t0, 0xada58487
li t1, 0x891bf560
sra t0,t0,t1
li t2, 0xada58487
bne t0, t2, fail
li a0, 1790
li t0, 0xba5c5850
li t1, 0xdfaad8ad
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1791
li t0, 0xa52f3798
li t1, 0x4b17a5d6
mulh t0,t0,t1
li t2, 0xe55c71b3
bne t0, t2, fail
li a0, 1792
li t0, 0x842c0ea8
li t1, 0xa007d8a5
and t0,t0,t1
li t2, 0x800408a0
bne t0, t2, fail
li a0, 1793
li t0, 0x2546af67
li t1, 0xb65700ff
remu t0,t0,t1
li t2, 0x2546af67
bne t0, t2, fail
li a0, 1794
li t0, 0x2ee27458
li t1, 0xcb48edad
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1795
li t0, 0xb3a2236a
li t1, 0x1a37fe04
mul t0,t0,t1
li t2, 0x0d71b9a8
bne t0, t2, fail
li a0, 1796
li t0, 0x9199d99e
li t1, 0xb3b770df
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1797
li t0, 0x1391ad89
li t1, 0xd63d9f6d
sra t0,t0,t1
li t2, 0x00009c8d
bne t0, t2, fail
li a0, 1798
li t0, 0x5b8cbfe9
li t1, 0x7629b749
mulhsu t0,t0,t1
li t2, 0x2a41cb8b
bne t0, t2, fail
li a0, 1799
li t0, 0x5cef103e
li t1, 0xadb3fd8b
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1800
li t0, 0xf3fa341f
li t1, 0x7d673abe
remu t0,t0,t1
li t2, 0x7692f961
bne t0, t2, fail
li a0, 1801
li t0, 0x28427c8f
li t1, 0xe4314a4c
remu t0,t0,t1
li t2, 0x28427c8f
bne t0, t2, fail
li a0, 1802
li t0, 0x7e72dd10
li t1, 0x6950d8d1
div t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1803
li t0, 0x0404150d
li t1, 0x39b59102
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1804
li t0, 0x60d3c0f6
li t1, 0x556bedff
rem t0,t0,t1
li t2, 0x0b67d2f7
bne t0, t2, fail
li a0, 1805
li t0, 0x2ede90df
li t1, 0x40885443
rem t0,t0,t1
li t2, 0x2ede90df
bne t0, t2, fail
li a0, 1806
li t0, 0x4b76fef6
li t1, 0x26211d6c
mul t0,t0,t1
li t2, 0xb2cb6dc8
bne t0, t2, fail
li a0, 1807
li t0, 0x1ff49e8c
li t1, 0xd8dc20f1
mulhu t0,t0,t1
li t2, 0x1b11e01b
bne t0, t2, fail
li a0, 1808
li t0, 0x1ac0e21b
li t1, 0xfa8a0371
sll t0,t0,t1
li t2, 0xc4360000
bne t0, t2, fail
li a0, 1809
li t0, 0x4aaed7a7
li t1, 0x191b8b81
sra t0,t0,t1
li t2, 0x25576bd3
bne t0, t2, fail
li a0, 1810
li t0, 0xc13f9602
li t1, 0x936df52f
mul t0,t0,t1
li t2, 0x5a16745e
bne t0, t2, fail
li a0, 1811
li t0, 0xb2d96e8a
li t1, 0x5cd3aa15
or t0,t0,t1
li t2, 0xfedbee9f
bne t0, t2, fail
li a0, 1812
li t0, 0xde764a76
li t1, 0x0f4ca841
mulhsu t0,t0,t1
li t2, 0xfdfee370
bne t0, t2, fail
li a0, 1813
li t0, 0xad35777b
li t1, 0xcff30c4d
rem t0,t0,t1
li t2, 0xdd426b2e
bne t0, t2, fail
li a0, 1814
li t0, 0x9d3dd112
li t1, 0xf8405753
xor t0,t0,t1
li t2, 0x657d8641
bne t0, t2, fail
li a0, 1815
li t0, 0xf47b909b
li t1, 0x8c9d0f25
sub t0,t0,t1
li t2, 0x67de8176
bne t0, t2, fail
li a0, 1816
li t0, 0x4a73bb7e
li t1, 0xe8c47791
div t0,t0,t1
li t2, 0xfffffffd
bne t0, t2, fail
li a0, 1817
li t0, 0xab3d7fc6
li t1, 0xb42c2c83
or t0,t0,t1
li t2, 0xbf3d7fc7
bne t0, t2, fail
li a0, 1818
li t0, 0x59b8c1eb
li t1, 0x3e67387e
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1819
li t0, 0xe856af2c
li t1, 0x5dce4c39
sll t0,t0,t1
li t2, 0x58000000
bne t0, t2, fail
li a0, 1820
li t0, 0x5e7d9416
li t1, 0x9ed22258
sra t0,t0,t1
li t2, 0x0000005e
bne t0, t2, fail
li a0, 1821
li t0, 0x2bda46db
li t1, 0xad14b282
sra t0,t0,t1
li t2, 0x0af691b6
bne t0, t2, fail
li a0, 1822
li t0, 0x72932ec7
li t1, 0x522d6c7f
xor t0,t0,t1
li t2, 0x20be42b8
bne t0, t2, fail
li a0, 1823
li t0, 0x9a2c0378
li t1, 0x580679cc
remu t0,t0,t1
li t2, 0x422589ac
bne t0, t2, fail
li a0, 1824
li t0, 0xdae5ad47
li t1, 0x614bc29b
sub t0,t0,t1
li t2, 0x7999eaac
bne t0, t2, fail
li a0, 1825
li t0, 0x157726ce
li t1, 0xec766564
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1826
li t0, 0x059e7814
li t1, 0xa168d0ec
mulhsu t0,t0,t1
li t2, 0x038af67b
bne t0, t2, fail
li a0, 1827
li t0, 0x70dd1688
li t1, 0xd2480c5f
and t0,t0,t1
li t2, 0x50480408
bne t0, t2, fail
li a0, 1828
li t0, 0xba582635
li t1, 0x12c2cd5d
xor t0,t0,t1
li t2, 0xa89aeb68
bne t0, t2, fail
li a0, 1829
li t0, 0xad73c562
li t1, 0x669cf575
mulhu t0,t0,t1
li t2, 0x45867980
bne t0, t2, fail
li a0, 1830
li t0, 0x02cdcb6e
li t1, 0xc2c908ca
mulhsu t0,t0,t1
li t2, 0x022227d6
bne t0, t2, fail
li a0, 1831
li t0, 0xfe078f5c
li t1, 0xf183b7ef
mulhu t0,t0,t1
li t2, 0xefa7d258
bne t0, t2, fail
li a0, 1832
li t0, 0x5d667736
li t1, 0x31fadcb9
xor t0,t0,t1
li t2, 0x6c9cab8f
bne t0, t2, fail
li a0, 1833
li t0, 0x05b8cbc4
li t1, 0x6653c937
sll t0,t0,t1
li t2, 0xe2000000
bne t0, t2, fail
li a0, 1834
li t0, 0xa8e415c9
li t1, 0x1e90061f
mulh t0,t0,t1
li t2, 0xf599b8c4
bne t0, t2, fail
li a0, 1835
li t0, 0x8beadfdb
li t1, 0x69e59aa3
xor t0,t0,t1
li t2, 0xe20f4578
bne t0, t2, fail
li a0, 1836
li t0, 0x919fad61
li t1, 0x2413b60b
srl t0,t0,t1
li t2, 0x001233f5
bne t0, t2, fail
li a0, 1837
li t0, 0x11541f34
li t1, 0x2e8a3e09
remu t0,t0,t1
li t2, 0x11541f34
bne t0, t2, fail
li a0, 1838
li t0, 0x467e50cb
li t1, 0x29e58019
rem t0,t0,t1
li t2, 0x1c98d0b2
bne t0, t2, fail
li a0, 1839
li t0, 0x67a1a32f
li t1, 0x8fec9081
mulhsu t0,t0,t1
li t2, 0x3a430da8
bne t0, t2, fail
li a0, 1840
li t0, 0xe9039d5b
li t1, 0x07a307bb
mulhu t0,t0,t1
li t2, 0x06f37da3
bne t0, t2, fail
li a0, 1841
li t0, 0xadc7cdb3
li t1, 0x213fecfe
sub t0,t0,t1
li t2, 0x8c87e0b5
bne t0, t2, fail
li a0, 1842
li t0, 0xd8a6b78f
li t1, 0x0b04ca32
sra t0,t0,t1
li t2, 0xfffff629
bne t0, t2, fail
li a0, 1843
li t0, 0xf4b9ad00
li t1, 0xac8537a9
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1844
li t0, 0xc4a7a16d
li t1, 0xd47db784
srl t0,t0,t1
li t2, 0x0c4a7a16
bne t0, t2, fail
li a0, 1845
li t0, 0x48c7cc8a
li t1, 0x9d3aaff0
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1846
li t0, 0x117e1a15
li t1, 0x00b7aeb1
sra t0,t0,t1
li t2, 0x000008bf
bne t0, t2, fail
li a0, 1847
li t0, 0xe744e243
li t1, 0xc695ffd4
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1848
li t0, 0xa7736f64
li t1, 0xe08e7cab
sll t0,t0,t1
li t2, 0x9b7b2000
bne t0, t2, fail
li a0, 1849
li t0, 0x89f35bf3
li t1, 0xacd948d3
rem t0,t0,t1
li t2, 0xdd1a1320
bne t0, t2, fail
li a0, 1850
li t0, 0xfb178d40
li t1, 0x4db5d5dc
mulh t0,t0,t1
li t2, 0xfe829909
bne t0, t2, fail
li a0, 1851
li t0, 0xe9c03ba8
li t1, 0xca1c19c2
add t0,t0,t1
li t2, 0xb3dc556a
bne t0, t2, fail
li a0, 1852
li t0, 0xe4e7d70b
li t1, 0x9ebcba5d
mulhu t0,t0,t1
li t2, 0x8defd79e
bne t0, t2, fail
li a0, 1853
li t0, 0xefb1e34a
li t1, 0x2b58f11d
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1854
li t0, 0x672e6b94
li t1, 0x5d6ad458
mulhu t0,t0,t1
li t2, 0x25a6ebe3
bne t0, t2, fail
li a0, 1855
li t0, 0x48cae53b
li t1, 0x79785be0
and t0,t0,t1
li t2, 0x48484120
bne t0, t2, fail
li a0, 1856
li t0, 0xe564d790
li t1, 0x59065ff0
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1857
li t0, 0xb50b7a8d
li t1, 0x5a036868
add t0,t0,t1
li t2, 0x0f0ee2f5
bne t0, t2, fail
li a0, 1858
li t0, 0x9642fe50
li t1, 0x01e80174
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1859
li t0, 0x3b532d87
li t1, 0x5ec3ddcf
add t0,t0,t1
li t2, 0x9a170b56
bne t0, t2, fail
li a0, 1860
li t0, 0x64684cf3
li t1, 0xa44b0cee
div t0,t0,t1
li t2, 0xffffffff
bne t0, t2, fail
li a0, 1861
li t0, 0x90db9dee
li t1, 0x09a86fc7
sra t0,t0,t1
li t2, 0xff21b73b
bne t0, t2, fail
li a0, 1862
li t0, 0xac82b26f
li t1, 0x9d9e3a2d
add t0,t0,t1
li t2, 0x4a20ec9c
bne t0, t2, fail
li a0, 1863
li t0, 0x0bc6150a
li t1, 0x03f23329
div t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1864
li t0, 0xbd8324ca
li t1, 0x8ee52fcf
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1865
li t0, 0x2b4b3cba
li t1, 0x823b0219
mulhu t0,t0,t1
li t2, 0x16062f88
bne t0, t2, fail
li a0, 1866
li t0, 0xfcbcba65
li t1, 0x932a842c
mulhu t0,t0,t1
li t2, 0x914a587b
bne t0, t2, fail
li a0, 1867
li t0, 0x454f5e22
li t1, 0x4420fd21
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1868
li t0, 0x277b8168
li t1, 0xd071dc41
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1869
li t0, 0x3cb66074
li t1, 0x539a8f24
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1870
li t0, 0x781e0aad
li t1, 0x09558bd2
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1871
li t0, 0xeb6fed2b
li t1, 0x4b6a8286
mul t0,t0,t1
li t2, 0xdfd3fa82
bne t0, t2, fail
li a0, 1872
li t0, 0x3458a6c8
li t1, 0x6f562848
mulhsu t0,t0,t1
li t2, 0x16c40e55
bne t0, t2, fail
li a0, 1873
li t0, 0x2325ad85
li t1, 0xe6bd4f35
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1874
li t0, 0x6f0baf99
li t1, 0x193fad98
div t0,t0,t1
li t2, 0x00000004
bne t0, t2, fail
li a0, 1875
li t0, 0x003cd8c6
li t1, 0xf8229fee
and t0,t0,t1
li t2, 0x002098c6
bne t0, t2, fail
li a0, 1876
li t0, 0x490b13af
li t1, 0x7b5af548
xor t0,t0,t1
li t2, 0x3251e6e7
bne t0, t2, fail
li a0, 1877
li t0, 0x45a1cad0
li t1, 0x2fce1a76
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1878
li t0, 0xb49a7572
li t1, 0xf95dcaa8
add t0,t0,t1
li t2, 0xadf8401a
bne t0, t2, fail
li a0, 1879
li t0, 0x282ab4ab
li t1, 0x9d6e26a8
sra t0,t0,t1
li t2, 0x00282ab4
bne t0, t2, fail
li a0, 1880
li t0, 0xb4c08c69
li t1, 0xfeaf9993
mulh t0,t0,t1
li t2, 0x0062e163
bne t0, t2, fail
li a0, 1881
li t0, 0xb22856a8
li t1, 0x6e658408
sra t0,t0,t1
li t2, 0xffb22856
bne t0, t2, fail
li a0, 1882
li t0, 0x470e0eba
li t1, 0x3c5c140c
sll t0,t0,t1
li t2, 0xe0eba000
bne t0, t2, fail
li a0, 1883
li t0, 0xc054de44
li t1, 0xf3ed7d93
mulhsu t0,t0,t1
li t2, 0xc3557e51
bne t0, t2, fail
li a0, 1884
li t0, 0xaa33595e
li t1, 0x85e3faf9
divu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1885
li t0, 0xe2ea529f
li t1, 0x190e0ecd
mulh t0,t0,t1
li t2, 0xfd274933
bne t0, t2, fail
li a0, 1886
li t0, 0xf163354c
li t1, 0x8cdf2a46
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1887
li t0, 0x87347cfe
li t1, 0x5af32191
srl t0,t0,t1
li t2, 0x0000439a
bne t0, t2, fail
li a0, 1888
li t0, 0xcf058720
li t1, 0xaa5fc6c4
or t0,t0,t1
li t2, 0xef5fc7e4
bne t0, t2, fail
li a0, 1889
li t0, 0xdc44ddd8
li t1, 0x6eb6babc
or t0,t0,t1
li t2, 0xfef6fffc
bne t0, t2, fail
li a0, 1890
li t0, 0x89b2c122
li t1, 0xddc1addc
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1891
li t0, 0x0c619732
li t1, 0xb0398ca7
mulhsu t0,t0,t1
li t2, 0x0885e07a
bne t0, t2, fail
li a0, 1892
li t0, 0x4e978664
li t1, 0x40fe165c
or t0,t0,t1
li t2, 0x4eff967c
bne t0, t2, fail
li a0, 1893
li t0, 0x8b19d2fa
li t1, 0x9a39ee03
mulh t0,t0,t1
li t2, 0x2e794201
bne t0, t2, fail
li a0, 1894
li t0, 0x5f796999
li t1, 0x5d2b12dc
sra t0,t0,t1
li t2, 0x00000005
bne t0, t2, fail
li a0, 1895
li t0, 0x1805ffd9
li t1, 0x93ab6413
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1896
li t0, 0x013cab1d
li t1, 0xd279ec8e
add t0,t0,t1
li t2, 0xd3b697ab
bne t0, t2, fail
li a0, 1897
li t0, 0x0cdc1a40
li t1, 0x2b9d8e7b
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1898
li t0, 0xaca87b44
li t1, 0x5a067889
remu t0,t0,t1
li t2, 0x52a202bb
bne t0, t2, fail
li a0, 1899
li t0, 0x1d9852a1
li t1, 0x5b5c59fe
mulhsu t0,t0,t1
li t2, 0x0a8fd284
bne t0, t2, fail
li a0, 1900
li t0, 0x6d8e3f5e
li t1, 0x9a93b315
mulhu t0,t0,t1
li t2, 0x4226c770
bne t0, t2, fail
li a0, 1901
li t0, 0x83d1925c
li t1, 0x72efb5e9
sub t0,t0,t1
li t2, 0x10e1dc73
bne t0, t2, fail
li a0, 1902
li t0, 0xd65035b0
li t1, 0xa42c5ba6
remu t0,t0,t1
li t2, 0x3223da0a
bne t0, t2, fail
li a0, 1903
li t0, 0xcf43b786
li t1, 0xdee1f470
xor t0,t0,t1
li t2, 0x11a243f6
bne t0, t2, fail
li a0, 1904
li t0, 0x05149da4
li t1, 0xbca1437e
srl t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1905
li t0, 0x3c56452b
li t1, 0xe3a99dcb
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1906
li t0, 0x838e2546
li t1, 0xd8960331
div t0,t0,t1
li t2, 0x00000003
bne t0, t2, fail
li a0, 1907
li t0, 0xacbf9b91
li t1, 0x915c78b1
and t0,t0,t1
li t2, 0x801c1891
bne t0, t2, fail
li a0, 1908
li t0, 0xe5fc8d8e
li t1, 0xd12cd3ed
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1909
li t0, 0xaf8772f2
li t1, 0xbff301b3
srl t0,t0,t1
li t2, 0x000015f0
bne t0, t2, fail
li a0, 1910
li t0, 0x6a429e52
li t1, 0x81c3b7fb
or t0,t0,t1
li t2, 0xebc3bffb
bne t0, t2, fail
li a0, 1911
li t0, 0xd73ca215
li t1, 0x49c93643
rem t0,t0,t1
li t2, 0xd73ca215
bne t0, t2, fail
li a0, 1912
li t0, 0xe0a830a0
li t1, 0x59d4d5d7
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1913
li t0, 0xc401fd52
li t1, 0x84c0053d
mulh t0,t0,t1
li t2, 0x1ce20990
bne t0, t2, fail
li a0, 1914
li t0, 0xad0330af
li t1, 0x8b51494b
and t0,t0,t1
li t2, 0x8901000b
bne t0, t2, fail
li a0, 1915
li t0, 0x408ea9d2
li t1, 0x141c4089
and t0,t0,t1
li t2, 0x000c0080
bne t0, t2, fail
li a0, 1916
li t0, 0x75b68a6c
li t1, 0xe1a68fe7
xor t0,t0,t1
li t2, 0x9410058b
bne t0, t2, fail
li a0, 1917
li t0, 0x6476fce8
li t1, 0x3a1735a4
rem t0,t0,t1
li t2, 0x2a5fc744
bne t0, t2, fail
li a0, 1918
li t0, 0x51b5b229
li t1, 0xbec5e36a
add t0,t0,t1
li t2, 0x107b9593
bne t0, t2, fail
li a0, 1919
li t0, 0xded71f91
li t1, 0xd7d12913
add t0,t0,t1
li t2, 0xb6a848a4
bne t0, t2, fail
li a0, 1920
li t0, 0x0c3d627e
li t1, 0x2b281bfd
mulh t0,t0,t1
li t2, 0x02103a79
bne t0, t2, fail
li a0, 1921
li t0, 0x14bc6178
li t1, 0xa1237f74
add t0,t0,t1
li t2, 0xb5dfe0ec
bne t0, t2, fail
li a0, 1922
li t0, 0xbf971b58
li t1, 0x9ef08c94
xor t0,t0,t1
li t2, 0x216797cc
bne t0, t2, fail
li a0, 1923
li t0, 0xd4a301fc
li t1, 0xd8fd0484
sub t0,t0,t1
li t2, 0xfba5fd78
bne t0, t2, fail
li a0, 1924
li t0, 0x7b494c7e
li t1, 0x89bd9fd0
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1925
li t0, 0x9f38f29e
li t1, 0x75afa6aa
xor t0,t0,t1
li t2, 0xea975434
bne t0, t2, fail
li a0, 1926
li t0, 0x5176ae8f
li t1, 0x3076b16f
mulh t0,t0,t1
li t2, 0x0f6c05e5
bne t0, t2, fail
li a0, 1927
li t0, 0xe2db2267
li t1, 0xb8e0f8c2
slt t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1928
li t0, 0xce44b92c
li t1, 0x80f431f7
xor t0,t0,t1
li t2, 0x4eb088db
bne t0, t2, fail
li a0, 1929
li t0, 0xae5d3d27
li t1, 0x3cb5ef41
and t0,t0,t1
li t2, 0x2c152d01
bne t0, t2, fail
li a0, 1930
li t0, 0x4884592c
li t1, 0x7c951bf3
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1931
li t0, 0x5775364b
li t1, 0xd79833e0
mulh t0,t0,t1
li t2, 0xf232399f
bne t0, t2, fail
li a0, 1932
li t0, 0xa495b6e4
li t1, 0x7a11f4ab
remu t0,t0,t1
li t2, 0x2a83c239
bne t0, t2, fail
li a0, 1933
li t0, 0x4b131824
li t1, 0x30f1f8b2
sll t0,t0,t1
li t2, 0x60900000
bne t0, t2, fail
li a0, 1934
li t0, 0x083fe8c8
li t1, 0x6869a337
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1935
li t0, 0x312eb0e7
li t1, 0x188f81b4
divu t0,t0,t1
li t2, 0x00000002
bne t0, t2, fail
li a0, 1936
li t0, 0x0e17e67f
li t1, 0x1bad18f4
sub t0,t0,t1
li t2, 0xf26acd8b
bne t0, t2, fail
li a0, 1937
li t0, 0x4d929e51
li t1, 0x68f7c8b1
sll t0,t0,t1
li t2, 0x3ca20000
bne t0, t2, fail
li a0, 1938
li t0, 0xd11dfce9
li t1, 0x35f18fac
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1939
li t0, 0xcf192bba
li t1, 0xb688649a
and t0,t0,t1
li t2, 0x8608209a
bne t0, t2, fail
li a0, 1940
li t0, 0xc6cb8356
li t1, 0xdf892571
mulhsu t0,t0,t1
li t2, 0xce0ca1f3
bne t0, t2, fail
li a0, 1941
li t0, 0x164ef383
li t1, 0x7d8eefa6
sra t0,t0,t1
li t2, 0x00593bce
bne t0, t2, fail
li a0, 1942
li t0, 0xb0a2a059
li t1, 0xdf2f32a9
sub t0,t0,t1
li t2, 0xd1736db0
bne t0, t2, fail
li a0, 1943
li t0, 0x58ed52cd
li t1, 0xbe6eb94d
or t0,t0,t1
li t2, 0xfeeffbcd
bne t0, t2, fail
li a0, 1944
li t0, 0x661d75b2
li t1, 0x9daae001
rem t0,t0,t1
li t2, 0x03c855b3
bne t0, t2, fail
li a0, 1945
li t0, 0x4c54d39b
li t1, 0x628387c5
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1946
li t0, 0x4dc88f91
li t1, 0x895b630b
rem t0,t0,t1
li t2, 0x4dc88f91
bne t0, t2, fail
li a0, 1947
li t0, 0xd9a977df
li t1, 0xfc5f6c7d
and t0,t0,t1
li t2, 0xd809645d
bne t0, t2, fail
li a0, 1948
li t0, 0x39c64a8f
li t1, 0xb789ee40
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1949
li t0, 0xb11e68db
li t1, 0x1aac57d0
and t0,t0,t1
li t2, 0x100c40d0
bne t0, t2, fail
li a0, 1950
li t0, 0xac5bf43b
li t1, 0xf3a0204d
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1951
li t0, 0x74c64425
li t1, 0x769c04a4
divu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1952
li t0, 0x846d64f3
li t1, 0x8c3800b0
slt t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1953
li t0, 0x177d891e
li t1, 0x05b476ae
remu t0,t0,t1
li t2, 0x00abae66
bne t0, t2, fail
li a0, 1954
li t0, 0x5bced0de
li t1, 0x92b4253f
and t0,t0,t1
li t2, 0x1284001e
bne t0, t2, fail
li a0, 1955
li t0, 0xabf8c7f3
li t1, 0xc11e4ebf
mulh t0,t0,t1
li t2, 0x14a3d419
bne t0, t2, fail
li a0, 1956
li t0, 0x01982d14
li t1, 0xd3d3fd3b
mulhsu t0,t0,t1
li t2, 0x0151bf28
bne t0, t2, fail
li a0, 1957
li t0, 0x15588abd
li t1, 0xc979ca61
sra t0,t0,t1
li t2, 0x0aac455e
bne t0, t2, fail
li a0, 1958
li t0, 0x149a7142
li t1, 0x7f6c91fe
sub t0,t0,t1
li t2, 0x952ddf44
bne t0, t2, fail
li a0, 1959
li t0, 0x0edee9f9
li t1, 0xbaa895ce
sltu t0,t0,t1
li t2, 0x00000001
bne t0, t2, fail
li a0, 1960
li t0, 0x2a4e68d2
li t1, 0xda60991c
mul t0,t0,t1
li t2, 0x9ff8f8f8
bne t0, t2, fail
li a0, 1961
li t0, 0xbdf87252
li t1, 0x56cc0871
add t0,t0,t1
li t2, 0x14c47ac3
bne t0, t2, fail
li a0, 1962
li t0, 0x3e6252d8
li t1, 0x46a54bde
div t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1963
li t0, 0xd72d8d8d
li t1, 0xbc68cf0e
sltu t0,t0,t1
li t2, 0x00000000
bne t0, t2, fail
li a0, 1964
li t0, 0xcac66f79
li t1, 0xdc10e425
remu t0,t0,t1
li t2, 0xcac66f79
bne t0, t2, fail
li a0, 1965
li t0, 0x4a3977f0
li t1, 0xf65452a1
div t0,t0,t1
li t2, 0xfffffff9
bne t0, t2, fail
li a0, 1966
li t0, 0x9ff7659c
li t1, 0x49c42f9f
div t0,t0,t1
li t2, 0xffffffff
bne t0, t2, fail
li a0, 1967
li t0, 0xcbd95e51
li t1, 0xe875924e
xor t0,t0,t1
li t2, 0x23accc1f
bne t0, t2, fail
li a0, 1968
li t0, 0x2deeeb73
li t1, 0x710c20a0
mulhsu t0,t0,t1
li t2, 0x1448a2fb
bne t0, t2, fail
li a0, 1969
li t0, 0x62255e4e
li t1, 0xf6d573b2
mulhu t0,t0,t1
li t2, 0x5ea1be11
bne t0, t2, fail
li a0, 1970
li t0, 0x6b75218c
li t1, 0xa0df08f3
xor t0,t0,t1
li t2, 0xcbaa297f
bne t0, t2, fail
li a0, 1971
li t0, 0x00000000
addi t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 1972
li t0, 0x00000000
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 1973
li t0, 0x00000000
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 1974
li t0, 0x00000000
xori t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 1975
li t0, 0x00000000
ori t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 1976
li t0, 0x00000000
andi t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 1977
li t0, 0x00000000
addi t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 1978
li t0, 0x00000000
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 1979
li t0, 0x00000000
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1980
li t0, 0x00000000
xori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 1981
li t0, 0x00000000
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 1982
li t0, 0x00000000
andi t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 1983
li t0, 0x00000000
addi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1984
li t0, 0x00000000
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1985
li t0, 0x00000000
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1986
li t0, 0x00000000
xori t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1987
li t0, 0x00000000
ori t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1988
li t0, 0x00000000
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 1989
li t0, 0x00000000
addi t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1990
li t0, 0x00000000
slti t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1991
li t0, 0x00000000
sltiu t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1992
li t0, 0x00000000
xori t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1993
li t0, 0x00000000
ori t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 1994
li t0, 0x00000000
andi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 1995
li t0, 0x00000000
addi t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 1996
li t0, 0x00000000
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 1997
li t0, 0x00000000
sltiu t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 1998
li t0, 0x00000000
xori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 1999
li t0, 0x00000000
ori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2000
li t0, 0x00000000
andi t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2001
li t0, 0x00000000
slli t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2002
li t0, 0x00000000
srli t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2003
li t0, 0x00000000
srai t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2004
li t0, 0x00000000
slli t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2005
li t0, 0x00000000
srli t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2006
li t0, 0x00000000
srai t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2007
li t0, 0x00000000
slli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2008
li t0, 0x00000000
srli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2009
li t0, 0x00000000
srai t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2010
li t0, 0x00000000
slli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2011
li t0, 0x00000000
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2012
li t0, 0x00000000
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2013
li t0, 0x00000001
addi t1,t0,-2048
li t2, 0xfffff801
bne t1, t2, fail
li a0, 2014
li t0, 0x00000001
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2015
li t0, 0x00000001
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2016
li t0, 0x00000001
xori t1,t0,-2048
li t2, 0xfffff801
bne t1, t2, fail
li a0, 2017
li t0, 0x00000001
ori t1,t0,-2048
li t2, 0xfffff801
bne t1, t2, fail
li a0, 2018
li t0, 0x00000001
andi t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2019
li t0, 0x00000001
addi t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2020
li t0, 0x00000001
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2021
li t0, 0x00000001
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2022
li t0, 0x00000001
xori t1,t0,-1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2023
li t0, 0x00000001
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2024
li t0, 0x00000001
andi t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2025
li t0, 0x00000001
addi t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2026
li t0, 0x00000001
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2027
li t0, 0x00000001
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2028
li t0, 0x00000001
xori t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2029
li t0, 0x00000001
ori t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2030
li t0, 0x00000001
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2031
li t0, 0x00000001
addi t1,t0,1
li t2, 0x00000002
bne t1, t2, fail
li a0, 2032
li t0, 0x00000001
slti t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2033
li t0, 0x00000001
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2034
li t0, 0x00000001
xori t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2035
li t0, 0x00000001
ori t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2036
li t0, 0x00000001
andi t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2037
li t0, 0x00000001
addi t1,t0,2047
li t2, 0x00000800
bne t1, t2, fail
li a0, 2038
li t0, 0x00000001
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2039
li t0, 0x00000001
sltiu t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2040
li t0, 0x00000001
xori t1,t0,2047
li t2, 0x000007fe
bne t1, t2, fail
li a0, 2041
li t0, 0x00000001
ori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2042
li t0, 0x00000001
andi t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2043
li t0, 0x00000001
slli t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2044
li t0, 0x00000001
srli t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2045
li t0, 0x00000001
srai t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2046
li t0, 0x00000001
slli t1,t0,1
li t2, 0x00000002
bne t1, t2, fail
li a0, 2047
li t0, 0x00000001
srli t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2048
li t0, 0x00000001
srai t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2049
li t0, 0x00000001
slli t1,t0,15
li t2, 0x00008000
bne t1, t2, fail
li a0, 2050
li t0, 0x00000001
srli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2051
li t0, 0x00000001
srai t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2052
li t0, 0x00000001
slli t1,t0,31
li t2, 0x80000000
bne t1, t2, fail
li a0, 2053
li t0, 0x00000001
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2054
li t0, 0x00000001
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2055
li t0, 0x00000002
addi t1,t0,-2048
li t2, 0xfffff802
bne t1, t2, fail
li a0, 2056
li t0, 0x00000002
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2057
li t0, 0x00000002
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2058
li t0, 0x00000002
xori t1,t0,-2048
li t2, 0xfffff802
bne t1, t2, fail
li a0, 2059
li t0, 0x00000002
ori t1,t0,-2048
li t2, 0xfffff802
bne t1, t2, fail
li a0, 2060
li t0, 0x00000002
andi t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2061
li t0, 0x00000002
addi t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2062
li t0, 0x00000002
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2063
li t0, 0x00000002
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2064
li t0, 0x00000002
xori t1,t0,-1
li t2, 0xfffffffd
bne t1, t2, fail
li a0, 2065
li t0, 0x00000002
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2066
li t0, 0x00000002
andi t1,t0,-1
li t2, 0x00000002
bne t1, t2, fail
li a0, 2067
li t0, 0x00000002
addi t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2068
li t0, 0x00000002
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2069
li t0, 0x00000002
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2070
li t0, 0x00000002
xori t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2071
li t0, 0x00000002
ori t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2072
li t0, 0x00000002
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2073
li t0, 0x00000002
addi t1,t0,1
li t2, 0x00000003
bne t1, t2, fail
li a0, 2074
li t0, 0x00000002
slti t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2075
li t0, 0x00000002
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2076
li t0, 0x00000002
xori t1,t0,1
li t2, 0x00000003
bne t1, t2, fail
li a0, 2077
li t0, 0x00000002
ori t1,t0,1
li t2, 0x00000003
bne t1, t2, fail
li a0, 2078
li t0, 0x00000002
andi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2079
li t0, 0x00000002
addi t1,t0,2047
li t2, 0x00000801
bne t1, t2, fail
li a0, 2080
li t0, 0x00000002
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2081
li t0, 0x00000002
sltiu t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2082
li t0, 0x00000002
xori t1,t0,2047
li t2, 0x000007fd
bne t1, t2, fail
li a0, 2083
li t0, 0x00000002
ori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2084
li t0, 0x00000002
andi t1,t0,2047
li t2, 0x00000002
bne t1, t2, fail
li a0, 2085
li t0, 0x00000002
slli t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2086
li t0, 0x00000002
srli t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2087
li t0, 0x00000002
srai t1,t0,0
li t2, 0x00000002
bne t1, t2, fail
li a0, 2088
li t0, 0x00000002
slli t1,t0,1
li t2, 0x00000004
bne t1, t2, fail
li a0, 2089
li t0, 0x00000002
srli t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2090
li t0, 0x00000002
srai t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2091
li t0, 0x00000002
slli t1,t0,15
li t2, 0x00010000
bne t1, t2, fail
li a0, 2092
li t0, 0x00000002
srli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2093
li t0, 0x00000002
srai t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2094
li t0, 0x00000002
slli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2095
li t0, 0x00000002
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2096
li t0, 0x00000002
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2097
li t0, 0x0000001f
addi t1,t0,-2048
li t2, 0xfffff81f
bne t1, t2, fail
li a0, 2098
li t0, 0x0000001f
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2099
li t0, 0x0000001f
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2100
li t0, 0x0000001f
xori t1,t0,-2048
li t2, 0xfffff81f
bne t1, t2, fail
li a0, 2101
li t0, 0x0000001f
ori t1,t0,-2048
li t2, 0xfffff81f
bne t1, t2, fail
li a0, 2102
li t0, 0x0000001f
andi t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2103
li t0, 0x0000001f
addi t1,t0,-1
li t2, 0x0000001e
bne t1, t2, fail
li a0, 2104
li t0, 0x0000001f
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2105
li t0, 0x0000001f
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2106
li t0, 0x0000001f
xori t1,t0,-1
li t2, 0xffffffe0
bne t1, t2, fail
li a0, 2107
li t0, 0x0000001f
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2108
li t0, 0x0000001f
andi t1,t0,-1
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2109
li t0, 0x0000001f
addi t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2110
li t0, 0x0000001f
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2111
li t0, 0x0000001f
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2112
li t0, 0x0000001f
xori t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2113
li t0, 0x0000001f
ori t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2114
li t0, 0x0000001f
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2115
li t0, 0x0000001f
addi t1,t0,1
li t2, 0x00000020
bne t1, t2, fail
li a0, 2116
li t0, 0x0000001f
slti t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2117
li t0, 0x0000001f
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2118
li t0, 0x0000001f
xori t1,t0,1
li t2, 0x0000001e
bne t1, t2, fail
li a0, 2119
li t0, 0x0000001f
ori t1,t0,1
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2120
li t0, 0x0000001f
andi t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2121
li t0, 0x0000001f
addi t1,t0,2047
li t2, 0x0000081e
bne t1, t2, fail
li a0, 2122
li t0, 0x0000001f
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2123
li t0, 0x0000001f
sltiu t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2124
li t0, 0x0000001f
xori t1,t0,2047
li t2, 0x000007e0
bne t1, t2, fail
li a0, 2125
li t0, 0x0000001f
ori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2126
li t0, 0x0000001f
andi t1,t0,2047
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2127
li t0, 0x0000001f
slli t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2128
li t0, 0x0000001f
srli t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2129
li t0, 0x0000001f
srai t1,t0,0
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2130
li t0, 0x0000001f
slli t1,t0,1
li t2, 0x0000003e
bne t1, t2, fail
li a0, 2131
li t0, 0x0000001f
srli t1,t0,1
li t2, 0x0000000f
bne t1, t2, fail
li a0, 2132
li t0, 0x0000001f
srai t1,t0,1
li t2, 0x0000000f
bne t1, t2, fail
li a0, 2133
li t0, 0x0000001f
slli t1,t0,15
li t2, 0x000f8000
bne t1, t2, fail
li a0, 2134
li t0, 0x0000001f
srli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2135
li t0, 0x0000001f
srai t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2136
li t0, 0x0000001f
slli t1,t0,31
li t2, 0x80000000
bne t1, t2, fail
li a0, 2137
li t0, 0x0000001f
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2138
li t0, 0x0000001f
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2139
li t0, 0x00000020
addi t1,t0,-2048
li t2, 0xfffff820
bne t1, t2, fail
li a0, 2140
li t0, 0x00000020
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2141
li t0, 0x00000020
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2142
li t0, 0x00000020
xori t1,t0,-2048
li t2, 0xfffff820
bne t1, t2, fail
li a0, 2143
li t0, 0x00000020
ori t1,t0,-2048
li t2, 0xfffff820
bne t1, t2, fail
li a0, 2144
li t0, 0x00000020
andi t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2145
li t0, 0x00000020
addi t1,t0,-1
li t2, 0x0000001f
bne t1, t2, fail
li a0, 2146
li t0, 0x00000020
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2147
li t0, 0x00000020
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2148
li t0, 0x00000020
xori t1,t0,-1
li t2, 0xffffffdf
bne t1, t2, fail
li a0, 2149
li t0, 0x00000020
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2150
li t0, 0x00000020
andi t1,t0,-1
li t2, 0x00000020
bne t1, t2, fail
li a0, 2151
li t0, 0x00000020
addi t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2152
li t0, 0x00000020
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2153
li t0, 0x00000020
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2154
li t0, 0x00000020
xori t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2155
li t0, 0x00000020
ori t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2156
li t0, 0x00000020
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2157
li t0, 0x00000020
addi t1,t0,1
li t2, 0x00000021
bne t1, t2, fail
li a0, 2158
li t0, 0x00000020
slti t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2159
li t0, 0x00000020
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2160
li t0, 0x00000020
xori t1,t0,1
li t2, 0x00000021
bne t1, t2, fail
li a0, 2161
li t0, 0x00000020
ori t1,t0,1
li t2, 0x00000021
bne t1, t2, fail
li a0, 2162
li t0, 0x00000020
andi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2163
li t0, 0x00000020
addi t1,t0,2047
li t2, 0x0000081f
bne t1, t2, fail
li a0, 2164
li t0, 0x00000020
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2165
li t0, 0x00000020
sltiu t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2166
li t0, 0x00000020
xori t1,t0,2047
li t2, 0x000007df
bne t1, t2, fail
li a0, 2167
li t0, 0x00000020
ori t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2168
li t0, 0x00000020
andi t1,t0,2047
li t2, 0x00000020
bne t1, t2, fail
li a0, 2169
li t0, 0x00000020
slli t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2170
li t0, 0x00000020
srli t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2171
li t0, 0x00000020
srai t1,t0,0
li t2, 0x00000020
bne t1, t2, fail
li a0, 2172
li t0, 0x00000020
slli t1,t0,1
li t2, 0x00000040
bne t1, t2, fail
li a0, 2173
li t0, 0x00000020
srli t1,t0,1
li t2, 0x00000010
bne t1, t2, fail
li a0, 2174
li t0, 0x00000020
srai t1,t0,1
li t2, 0x00000010
bne t1, t2, fail
li a0, 2175
li t0, 0x00000020
slli t1,t0,15
li t2, 0x00100000
bne t1, t2, fail
li a0, 2176
li t0, 0x00000020
srli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2177
li t0, 0x00000020
srai t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2178
li t0, 0x00000020
slli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2179
li t0, 0x00000020
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2180
li t0, 0x00000020
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2181
li t0, 0x7fffffff
addi t1,t0,-2048
li t2, 0x7ffff7ff
bne t1, t2, fail
li a0, 2182
li t0, 0x7fffffff
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2183
li t0, 0x7fffffff
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2184
li t0, 0x7fffffff
xori t1,t0,-2048
li t2, 0x800007ff
bne t1, t2, fail
li a0, 2185
li t0, 0x7fffffff
ori t1,t0,-2048
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2186
li t0, 0x7fffffff
andi t1,t0,-2048
li t2, 0x7ffff800
bne t1, t2, fail
li a0, 2187
li t0, 0x7fffffff
addi t1,t0,-1
li t2, 0x7ffffffe
bne t1, t2, fail
li a0, 2188
li t0, 0x7fffffff
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2189
li t0, 0x7fffffff
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2190
li t0, 0x7fffffff
xori t1,t0,-1
li t2, 0x80000000
bne t1, t2, fail
li a0, 2191
li t0, 0x7fffffff
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2192
li t0, 0x7fffffff
andi t1,t0,-1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2193
li t0, 0x7fffffff
addi t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2194
li t0, 0x7fffffff
slti t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2195
li t0, 0x7fffffff
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2196
li t0, 0x7fffffff
xori t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2197
li t0, 0x7fffffff
ori t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2198
li t0, 0x7fffffff
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2199
li t0, 0x7fffffff
addi t1,t0,1
li t2, 0x80000000
bne t1, t2, fail
li a0, 2200
li t0, 0x7fffffff
slti t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2201
li t0, 0x7fffffff
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2202
li t0, 0x7fffffff
xori t1,t0,1
li t2, 0x7ffffffe
bne t1, t2, fail
li a0, 2203
li t0, 0x7fffffff
ori t1,t0,1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2204
li t0, 0x7fffffff
andi t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2205
li t0, 0x7fffffff
addi t1,t0,2047
li t2, 0x800007fe
bne t1, t2, fail
li a0, 2206
li t0, 0x7fffffff
slti t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2207
li t0, 0x7fffffff
sltiu t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2208
li t0, 0x7fffffff
xori t1,t0,2047
li t2, 0x7ffff800
bne t1, t2, fail
li a0, 2209
li t0, 0x7fffffff
ori t1,t0,2047
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2210
li t0, 0x7fffffff
andi t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2211
li t0, 0x7fffffff
slli t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2212
li t0, 0x7fffffff
srli t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2213
li t0, 0x7fffffff
srai t1,t0,0
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2214
li t0, 0x7fffffff
slli t1,t0,1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2215
li t0, 0x7fffffff
srli t1,t0,1
li t2, 0x3fffffff
bne t1, t2, fail
li a0, 2216
li t0, 0x7fffffff
srai t1,t0,1
li t2, 0x3fffffff
bne t1, t2, fail
li a0, 2217
li t0, 0x7fffffff
slli t1,t0,15
li t2, 0xffff8000
bne t1, t2, fail
li a0, 2218
li t0, 0x7fffffff
srli t1,t0,15
li t2, 0x0000ffff
bne t1, t2, fail
li a0, 2219
li t0, 0x7fffffff
srai t1,t0,15
li t2, 0x0000ffff
bne t1, t2, fail
li a0, 2220
li t0, 0x7fffffff
slli t1,t0,31
li t2, 0x80000000
bne t1, t2, fail
li a0, 2221
li t0, 0x7fffffff
srli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2222
li t0, 0x7fffffff
srai t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2223
li t0, 0x80000000
addi t1,t0,-2048
li t2, 0x7ffff800
bne t1, t2, fail
li a0, 2224
li t0, 0x80000000
slti t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2225
li t0, 0x80000000
sltiu t1,t0,-2048
li t2, 0x00000001
bne t1, t2, fail
li a0, 2226
li t0, 0x80000000
xori t1,t0,-2048
li t2, 0x7ffff800
bne t1, t2, fail
li a0, 2227
li t0, 0x80000000
ori t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 2228
li t0, 0x80000000
andi t1,t0,-2048
li t2, 0x80000000
bne t1, t2, fail
li a0, 2229
li t0, 0x80000000
addi t1,t0,-1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2230
li t0, 0x80000000
slti t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2231
li t0, 0x80000000
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2232
li t0, 0x80000000
xori t1,t0,-1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2233
li t0, 0x80000000
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2234
li t0, 0x80000000
andi t1,t0,-1
li t2, 0x80000000
bne t1, t2, fail
li a0, 2235
li t0, 0x80000000
addi t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2236
li t0, 0x80000000
slti t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2237
li t0, 0x80000000
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2238
li t0, 0x80000000
xori t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2239
li t0, 0x80000000
ori t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2240
li t0, 0x80000000
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2241
li t0, 0x80000000
addi t1,t0,1
li t2, 0x80000001
bne t1, t2, fail
li a0, 2242
li t0, 0x80000000
slti t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2243
li t0, 0x80000000
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2244
li t0, 0x80000000
xori t1,t0,1
li t2, 0x80000001
bne t1, t2, fail
li a0, 2245
li t0, 0x80000000
ori t1,t0,1
li t2, 0x80000001
bne t1, t2, fail
li a0, 2246
li t0, 0x80000000
andi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2247
li t0, 0x80000000
addi t1,t0,2047
li t2, 0x800007ff
bne t1, t2, fail
li a0, 2248
li t0, 0x80000000
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2249
li t0, 0x80000000
sltiu t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2250
li t0, 0x80000000
xori t1,t0,2047
li t2, 0x800007ff
bne t1, t2, fail
li a0, 2251
li t0, 0x80000000
ori t1,t0,2047
li t2, 0x800007ff
bne t1, t2, fail
li a0, 2252
li t0, 0x80000000
andi t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2253
li t0, 0x80000000
slli t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2254
li t0, 0x80000000
srli t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2255
li t0, 0x80000000
srai t1,t0,0
li t2, 0x80000000
bne t1, t2, fail
li a0, 2256
li t0, 0x80000000
slli t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2257
li t0, 0x80000000
srli t1,t0,1
li t2, 0x40000000
bne t1, t2, fail
li a0, 2258
li t0, 0x80000000
srai t1,t0,1
li t2, 0xc0000000
bne t1, t2, fail
li a0, 2259
li t0, 0x80000000
slli t1,t0,15
li t2, 0x00000000
bne t1, t2, fail
li a0, 2260
li t0, 0x80000000
srli t1,t0,15
li t2, 0x00010000
bne t1, t2, fail
li a0, 2261
li t0, 0x80000000
srai t1,t0,15
li t2, 0xffff0000
bne t1, t2, fail
li a0, 2262
li t0, 0x80000000
slli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2263
li t0, 0x80000000
srli t1,t0,31
li t2, 0x00000001
bne t1, t2, fail
li a0, 2264
li t0, 0x80000000
srai t1,t0,31
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2265
li t0, 0xfffffffe
addi t1,t0,-2048
li t2, 0xfffff7fe
bne t1, t2, fail
li a0, 2266
li t0, 0xfffffffe
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2267
li t0, 0xfffffffe
sltiu t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2268
li t0, 0xfffffffe
xori t1,t0,-2048
li t2, 0x000007fe
bne t1, t2, fail
li a0, 2269
li t0, 0xfffffffe
ori t1,t0,-2048
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2270
li t0, 0xfffffffe
andi t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 2271
li t0, 0xfffffffe
addi t1,t0,-1
li t2, 0xfffffffd
bne t1, t2, fail
li a0, 2272
li t0, 0xfffffffe
slti t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2273
li t0, 0xfffffffe
sltiu t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2274
li t0, 0xfffffffe
xori t1,t0,-1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2275
li t0, 0xfffffffe
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2276
li t0, 0xfffffffe
andi t1,t0,-1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2277
li t0, 0xfffffffe
addi t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2278
li t0, 0xfffffffe
slti t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2279
li t0, 0xfffffffe
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2280
li t0, 0xfffffffe
xori t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2281
li t0, 0xfffffffe
ori t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2282
li t0, 0xfffffffe
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2283
li t0, 0xfffffffe
addi t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2284
li t0, 0xfffffffe
slti t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2285
li t0, 0xfffffffe
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2286
li t0, 0xfffffffe
xori t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2287
li t0, 0xfffffffe
ori t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2288
li t0, 0xfffffffe
andi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2289
li t0, 0xfffffffe
addi t1,t0,2047
li t2, 0x000007fd
bne t1, t2, fail
li a0, 2290
li t0, 0xfffffffe
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2291
li t0, 0xfffffffe
sltiu t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2292
li t0, 0xfffffffe
xori t1,t0,2047
li t2, 0xfffff801
bne t1, t2, fail
li a0, 2293
li t0, 0xfffffffe
ori t1,t0,2047
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2294
li t0, 0xfffffffe
andi t1,t0,2047
li t2, 0x000007fe
bne t1, t2, fail
li a0, 2295
li t0, 0xfffffffe
slli t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2296
li t0, 0xfffffffe
srli t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2297
li t0, 0xfffffffe
srai t1,t0,0
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2298
li t0, 0xfffffffe
slli t1,t0,1
li t2, 0xfffffffc
bne t1, t2, fail
li a0, 2299
li t0, 0xfffffffe
srli t1,t0,1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2300
li t0, 0xfffffffe
srai t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2301
li t0, 0xfffffffe
slli t1,t0,15
li t2, 0xffff0000
bne t1, t2, fail
li a0, 2302
li t0, 0xfffffffe
srli t1,t0,15
li t2, 0x0001ffff
bne t1, t2, fail
li a0, 2303
li t0, 0xfffffffe
srai t1,t0,15
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2304
li t0, 0xfffffffe
slli t1,t0,31
li t2, 0x00000000
bne t1, t2, fail
li a0, 2305
li t0, 0xfffffffe
srli t1,t0,31
li t2, 0x00000001
bne t1, t2, fail
li a0, 2306
li t0, 0xfffffffe
srai t1,t0,31
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2307
li t0, 0xffffffff
addi t1,t0,-2048
li t2, 0xfffff7ff
bne t1, t2, fail
li a0, 2308
li t0, 0xffffffff
slti t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2309
li t0, 0xffffffff
sltiu t1,t0,-2048
li t2, 0x00000000
bne t1, t2, fail
li a0, 2310
li t0, 0xffffffff
xori t1,t0,-2048
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2311
li t0, 0xffffffff
ori t1,t0,-2048
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2312
li t0, 0xffffffff
andi t1,t0,-2048
li t2, 0xfffff800
bne t1, t2, fail
li a0, 2313
li t0, 0xffffffff
addi t1,t0,-1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2314
li t0, 0xffffffff
slti t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2315
li t0, 0xffffffff
sltiu t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2316
li t0, 0xffffffff
xori t1,t0,-1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2317
li t0, 0xffffffff
ori t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2318
li t0, 0xffffffff
andi t1,t0,-1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2319
li t0, 0xffffffff
addi t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2320
li t0, 0xffffffff
slti t1,t0,0
li t2, 0x00000001
bne t1, t2, fail
li a0, 2321
li t0, 0xffffffff
sltiu t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2322
li t0, 0xffffffff
xori t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2323
li t0, 0xffffffff
ori t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2324
li t0, 0xffffffff
andi t1,t0,0
li t2, 0x00000000
bne t1, t2, fail
li a0, 2325
li t0, 0xffffffff
addi t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2326
li t0, 0xffffffff
slti t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2327
li t0, 0xffffffff
sltiu t1,t0,1
li t2, 0x00000000
bne t1, t2, fail
li a0, 2328
li t0, 0xffffffff
xori t1,t0,1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2329
li t0, 0xffffffff
ori t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2330
li t0, 0xffffffff
andi t1,t0,1
li t2, 0x00000001
bne t1, t2, fail
li a0, 2331
li t0, 0xffffffff
addi t1,t0,2047
li t2, 0x000007fe
bne t1, t2, fail
li a0, 2332
li t0, 0xffffffff
slti t1,t0,2047
li t2, 0x00000001
bne t1, t2, fail
li a0, 2333
li t0, 0xffffffff
sltiu t1,t0,2047
li t2, 0x00000000
bne t1, t2, fail
li a0, 2334
li t0, 0xffffffff
xori t1,t0,2047
li t2, 0xfffff800
bne t1, t2, fail
li a0, 2335
li t0, 0xffffffff
ori t1,t0,2047
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2336
li t0, 0xffffffff
andi t1,t0,2047
li t2, 0x000007ff
bne t1, t2, fail
li a0, 2337
li t0, 0xffffffff
slli t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2338
li t0, 0xffffffff
srli t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2339
li t0, 0xffffffff
srai t1,t0,0
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2340
li t0, 0xffffffff
slli t1,t0,1
li t2, 0xfffffffe
bne t1, t2, fail
li a0, 2341
li t0, 0xffffffff
srli t1,t0,1
li t2, 0x7fffffff
bne t1, t2, fail
li a0, 2342
li t0, 0xffffffff
srai t1,t0,1
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2343
li t0, 0xffffffff
slli t1,t0,15
li t2, 0xffff8000
bne t1, t2, fail
li a0, 2344
li t0, 0xffffffff
srli t1,t0,15
li t2, 0x0001ffff
bne t1, t2, fail
li a0, 2345
li t0, 0xffffffff
srai t1,t0,15
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2346
li t0, 0xffffffff
slli t1,t0,31
li t2, 0x80000000
bne t1, t2, fail
li a0, 2347
li t0, 0xffffffff
srli t1,t0,31
li t2, 0x00000001
bne t1, t2, fail
li a0, 2348
li t0, 0xffffffff
srai t1,t0,31
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2349
addi zero,zero,37
addi t0,zero,5
li t2, 0x00000005
bne t0, t2, fail
li a0, 2350
lui t0,0xabcde
li t2, 0xabcde000
bne t0, t2, fail
auipc t0,0
la t1,pc_label
pc_label:
addi t0,t0,12
bne t0,t1,fail
li a0, 2351
li t0,0x00000000
li t1,0x00000000
li t3,0
beq t0,t1,branch_2350
j branch_2350_done
branch_2350:
li t3,1
branch_2350_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2352
li t0,0x00000000
li t1,0x00000001
li t3,0
beq t0,t1,branch_2351
j branch_2351_done
branch_2351:
li t3,1
branch_2351_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2353
li t0,0x00000001
li t1,0x00000000
li t3,0
beq t0,t1,branch_2352
j branch_2352_done
branch_2352:
li t3,1
branch_2352_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2354
li t0,0x80000000
li t1,0x00000001
li t3,0
beq t0,t1,branch_2353
j branch_2353_done
branch_2353:
li t3,1
branch_2353_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2355
li t0,0xffffffff
li t1,0x80000000
li t3,0
beq t0,t1,branch_2354
j branch_2354_done
branch_2354:
li t3,1
branch_2354_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2356
li t0,0x00000000
li t1,0x00000000
li t3,0
bne t0,t1,branch_2355
j branch_2355_done
branch_2355:
li t3,1
branch_2355_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2357
li t0,0x00000000
li t1,0x00000001
li t3,0
bne t0,t1,branch_2356
j branch_2356_done
branch_2356:
li t3,1
branch_2356_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2358
li t0,0x00000001
li t1,0x00000000
li t3,0
bne t0,t1,branch_2357
j branch_2357_done
branch_2357:
li t3,1
branch_2357_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2359
li t0,0x80000000
li t1,0x00000001
li t3,0
bne t0,t1,branch_2358
j branch_2358_done
branch_2358:
li t3,1
branch_2358_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2360
li t0,0xffffffff
li t1,0x80000000
li t3,0
bne t0,t1,branch_2359
j branch_2359_done
branch_2359:
li t3,1
branch_2359_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2361
li t0,0x00000000
li t1,0x00000000
li t3,0
blt t0,t1,branch_2360
j branch_2360_done
branch_2360:
li t3,1
branch_2360_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2362
li t0,0x00000000
li t1,0x00000001
li t3,0
blt t0,t1,branch_2361
j branch_2361_done
branch_2361:
li t3,1
branch_2361_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2363
li t0,0x00000001
li t1,0x00000000
li t3,0
blt t0,t1,branch_2362
j branch_2362_done
branch_2362:
li t3,1
branch_2362_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2364
li t0,0x80000000
li t1,0x00000001
li t3,0
blt t0,t1,branch_2363
j branch_2363_done
branch_2363:
li t3,1
branch_2363_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2365
li t0,0xffffffff
li t1,0x80000000
li t3,0
blt t0,t1,branch_2364
j branch_2364_done
branch_2364:
li t3,1
branch_2364_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2366
li t0,0x00000000
li t1,0x00000000
li t3,0
bge t0,t1,branch_2365
j branch_2365_done
branch_2365:
li t3,1
branch_2365_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2367
li t0,0x00000000
li t1,0x00000001
li t3,0
bge t0,t1,branch_2366
j branch_2366_done
branch_2366:
li t3,1
branch_2366_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2368
li t0,0x00000001
li t1,0x00000000
li t3,0
bge t0,t1,branch_2367
j branch_2367_done
branch_2367:
li t3,1
branch_2367_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2369
li t0,0x80000000
li t1,0x00000001
li t3,0
bge t0,t1,branch_2368
j branch_2368_done
branch_2368:
li t3,1
branch_2368_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2370
li t0,0xffffffff
li t1,0x80000000
li t3,0
bge t0,t1,branch_2369
j branch_2369_done
branch_2369:
li t3,1
branch_2369_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2371
li t0,0x00000000
li t1,0x00000000
li t3,0
bltu t0,t1,branch_2370
j branch_2370_done
branch_2370:
li t3,1
branch_2370_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2372
li t0,0x00000000
li t1,0x00000001
li t3,0
bltu t0,t1,branch_2371
j branch_2371_done
branch_2371:
li t3,1
branch_2371_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2373
li t0,0x00000001
li t1,0x00000000
li t3,0
bltu t0,t1,branch_2372
j branch_2372_done
branch_2372:
li t3,1
branch_2372_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2374
li t0,0x80000000
li t1,0x00000001
li t3,0
bltu t0,t1,branch_2373
j branch_2373_done
branch_2373:
li t3,1
branch_2373_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2375
li t0,0xffffffff
li t1,0x80000000
li t3,0
bltu t0,t1,branch_2374
j branch_2374_done
branch_2374:
li t3,1
branch_2374_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2376
li t0,0x00000000
li t1,0x00000000
li t3,0
bgeu t0,t1,branch_2375
j branch_2375_done
branch_2375:
li t3,1
branch_2375_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2377
li t0,0x00000000
li t1,0x00000001
li t3,0
bgeu t0,t1,branch_2376
j branch_2376_done
branch_2376:
li t3,1
branch_2376_done:
li t2, 0x00000000
bne t3, t2, fail
li a0, 2378
li t0,0x00000001
li t1,0x00000000
li t3,0
bgeu t0,t1,branch_2377
j branch_2377_done
branch_2377:
li t3,1
branch_2377_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2379
li t0,0x80000000
li t1,0x00000001
li t3,0
bgeu t0,t1,branch_2378
j branch_2378_done
branch_2378:
li t3,1
branch_2378_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2380
li t0,0xffffffff
li t1,0x80000000
li t3,0
bgeu t0,t1,branch_2379
j branch_2379_done
branch_2379:
li t3,1
branch_2379_done:
li t2, 0x00000001
bne t3, t2, fail
li a0, 2381
li t0,7
li t1,0
backward_loop:
addi t1,t1,1
addi t0,t0,-1
bne t0,zero,backward_loop
li t2, 0x00000007
bne t1, t2, fail
jal ra,jump_target
jump_return:
j after_jump
jump_target:
la t0,jump_return
bne ra,t0,fail
la t0,jump_indirect
ori t0,t0,1
jalr t1,0(t0)
jalr_return:
j fail
jump_indirect:
la t0,jalr_return
bne t1,t0,fail
j after_jump
after_jump:
la t0,data
li t1,0x80ff7f01
sw t1,0(t0)
li a0, 2382
lb t1,0(t0)
li t2, 0x00000001
bne t1, t2, fail
li a0, 2383
lb t1,1(t0)
li t2, 0x0000007f
bne t1, t2, fail
li a0, 2384
lb t1,2(t0)
li t2, 0xffffffff
bne t1, t2, fail
li a0, 2385
lb t1,3(t0)
li t2, 0xffffff80
bne t1, t2, fail
li a0, 2386
lbu t1,2(t0)
li t2, 0x000000ff
bne t1, t2, fail
li a0, 2387
lh t1,0(t0)
li t2, 0x00007f01
bne t1, t2, fail
li a0, 2388
lh t1,2(t0)
li t2, 0xffff80ff
bne t1, t2, fail
li a0, 2389
lhu t1,2(t0)
li t2, 0x000080ff
bne t1, t2, fail
li a0, 2390
lw t1,0(t0)
li t2, 0x80ff7f01
bne t1, t2, fail
li a0, 2391
li t1,0x55
sb t1,1(t0)
lw t1,0(t0)
li t2, 0x80ff5501
bne t1, t2, fail
li a0, 2392
li t1,0x1122
sh t1,2(t0)
lw t1,0(t0)
li t2, 0x11225501
bne t1, t2, fail
fence rw,rw
fence.i
li a0,0
ebreak
fail:
ebreak
.section .data
.balign 4
data:
.word 0
