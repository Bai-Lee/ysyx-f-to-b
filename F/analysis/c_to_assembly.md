# F4：C 与汇编的对应

Compiler Explorer 的真实 gcc 15.1 API 编译结果。用 API 的 source.line 对应代替网页颜色高亮；不是从手写汇编伪造映射。原始请求/响应在 artifacts/F4/compiler_explorer。

| C行号 | 汇编 |
|---|---|
| 2 | `        push    rbp     #` |
| 2 | `        mov     rbp, rsp  #,` |
| 2 | `        sub     rsp, 16   #,` |
| 3 | `        mov     DWORD PTR [rbp-4], 1      # x,` |
| 4 | `        mov     DWORD PTR [rbp-8], 2      # y,` |
| 5 | `        mov     edx, DWORD PTR [rbp-4]    # tmp104, x` |
| 5 | `        mov     eax, DWORD PTR [rbp-8]    # tmp105, y` |
| 5 | `        add     eax, edx  # z_3, tmp104` |
| 5 | `        mov     DWORD PTR [rbp-12], eax   # z, z_3` |
| 6 | `        mov     eax, DWORD PTR [rbp-12]   # tmp106, z` |
| 6 | `        mov     esi, eax  #, tmp106` |
| 6 | `        mov     edi, OFFSET FLAT:.LC0     #,` |
| 6 | `        mov     eax, 0    #,` |
| 6 | `        call    printf  #` |
| 7 | `        mov     eax, 0    # _6,` |
| 8 | `        leave   ` |
| 8 | `        ret     ` |

同一源程序也用已安装的 MinGW GCC 本地编译和执行。宿主 Windows x86-64 与线上 Linux x86-64 的 ABI/启动代码不同，因此不要求两份汇编逐字相同。均实测得到 z=3；修改例为42，求和为55。

把 x/y/z 的赋值与相应源行的栈槽写入、读出和加法指令对照；printf 对应调用及参数准备；return 对应返回值与函数退栈。这里不要求先掌握每一条 x86 指令，也不声称编译器经过形式化验证。
