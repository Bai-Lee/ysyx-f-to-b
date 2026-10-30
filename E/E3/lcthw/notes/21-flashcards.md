# 练习 21：类型与运算教学卡片

材料已经制作并以 types.c 实测；“每天 15 分钟”的个人练习时间不伪造为完成。可折叠答案或遮住右栏复习。具体平台值见 实测表（原完整交付引用：`../../../../artifacts/E3/LCT/types_table.json`）。

| 问题 | 答案及易错点 |
|---|---|
| char、short、int、long、long long 大小是否固定？ | 只保证标准规定的最小范围和大小次序；char 为一字节但字节不普遍等于 8 位。本机另行实测，不能套用 Windows/Linux 的相同 long 大小。 |
| signed 与 unsigned 的溢出？ | unsigned 按模 2^N 计算；signed 溢出为未定义行为，不能依赖回绕。 |
| int8_t/uint32_t？ | 条件提供的恰好位宽整数，无相应类型时可不存在。 |
| int_leastN_t 与 int_fastN_t？ | 至少 N 位的最小存储类型与实现选择的快速类型，不保证大小相同。 |
| intptr_t 与 uintptr_t？ | 若实现提供，可保存 void 指针并往返，不能泛化为所有函数指针。 |
| intmax_t/uintmax_t？ | 标准最大宽度整数类型；扩展类型仍需查实现约束。 |
| size_t/ptrdiff_t？ | sizeof 返回无符号 size_t；同一数组合法指针差用有符号 ptrdiff_t。 |
| float/double/long double？ | 浮点精度与范围不同，十进制小数通常不精确；变参 float 提升为 double。 |
| void 与 void *？ | void 表示无值；void * 可保存对象地址，标准 C 不允许对 void * 做元素算术。 |
| const？ | 约束通过该表达式修改；不能以它代替线程安全或认为所有别名都不可修改。 |
| volatile？ | 保留实现定义的可观察访问，不保证原子性，不是线程同步。 |
| register？ | 编译器提示并限制取地址，不强制分配物理寄存器。 |
| static？ | 函数内对象有静态存储期；文件作用域名字有内部链接。两层含义不可混淆。 |
| extern？ | 通常声明其它位置定义的对象/函数；存储期、作用域、链接分别分析。 |
| ++i 与 i++？ | 都加一，但表达式分别产生新值和旧值；避免在未排序求值的表达式中多次修改。 |
| + - * / %？ | 算术运算；整数除法截去小数，除零和 INT_MIN/-1 需防护，% 仅整数。 |
| == != < > <= >=？ | 比较结果为 0/1，混合 signed/unsigned 先发生通常算术转换。 |
| && || !？ | 逻辑运算且前两者短路；与 &、|、~ 的逐位操作不同。 |
| & | ^ ~ << >>？ | 位运算；移位数不得负或大于等于提升后类型位宽；有符号右移查实现。 |
| = 与 += -= *= /= %=？ | 赋值/复合赋值，左侧需可修改 lvalue；不能用 = 当相等判断。 |
| &= |= ^= <<= >>=？ | 对相应位运算结果赋回左侧；仍遵守提升和移位约束。 |
| &x 与 *p？ | 取地址与解引用；指针必须指向有效、合适类型且尚存活的对象。 |
| . 与 ->？ | 对结构体值访问成员；对结构体指针解引用后访问成员。 |
| a[i]、sizeof、?:、逗号？ | 合法范围的指针索引；对象/类型尺寸；条件选择；左到右求值并返回右值。 |
| if/switch？ | 条件分支/整数分派；switch 注意 case 穿透和 break。 |
| for/while/do while？ | 前两者先判条件，do 至少执行一次；边界和更新必须匹配。 |
| break/continue？ | 退出最近循环/switch；进入最近循环的下一轮，for 会先执行更新。 |
| return/goto？ | 返回调用者；跳到同函数标签，可集中错误清理但不能跳过必要初始化。 |
| enum、struct、union、typedef？ | 命名整数集合、聚合成员、共享存储成员、类型别名；typedef 不创建新对象。 |
| va_arg 为什么必须类型匹配？ | 无通用运行时类型信息；按调用契约和默认参数提升读取，最后 va_end。 |

依据：课程第 21 章、已安装的 stdint.h/编译器宏、[GNU C 手册](https://www.gnu.org/software/c-intro-and-ref/manual/c-intro-and-ref.html)与[GCC volatile 文档](https://gcc.gnu.org/onlinedocs/gcc/Volatiles.html)。
