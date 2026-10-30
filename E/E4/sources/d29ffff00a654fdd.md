<!-- SOURCE: https://nju-projectn.github.io/dlco-lecture-note/exp/02.html | VERSION: unversioned snapshot; edition not asserted | CAPTURED: 2026-10-23T11:14:36.814591+00:00 | RAW_SHA256: 1cfae55f0aebb501a749b17b033b210b7f693b1152acc8729d2978970cc83ac2 -->

[南京大学 计算机科学与技术系 数字逻辑与计算机组成 课程实验](https://nju-projectn.github.io/dlco-lecture-note/index.html)

<a id="rtd-search-form"></a>



- [实验一 选择器](https://nju-projectn.github.io/dlco-lecture-note/exp/01.html)
- [实验二 译码器和编码器](#)
  - [译码器](#id2)
    - [2-4译码器](#id3)
  - [编码器](#id4)
    - [4-2编码器](#id5)
    - [优先编码器](#id6)
    - [七段数码管](#id7)
    - [模块实例化](#id8)
  - [实验验收内容](#id9)
- [实验三 加法器与ALU](1a5b5cc32fc96bd9.md)
- [实验四 计数器和时钟](https://nju-projectn.github.io/dlco-lecture-note/exp/04.html)
- [实验五 寄存器组及存储器](https://nju-projectn.github.io/dlco-lecture-note/exp/05.html)
- [实验六 移位寄存器及桶形移位器](fc7e85498e5708ad.md)
- [实验七 状态机及键盘输入](c203ed4c183393ac.md)
- [实验八 VGA接口控制器实现](8eb56251b0d9d092.md)
- [实验九 字符输入界面](https://nju-projectn.github.io/dlco-lecture-note/exp/09.html)
- [实验十 CPU数据通路](https://nju-projectn.github.io/dlco-lecture-note/exp/10.html)
- [实验十一 RV32I单周期CPU](https://nju-projectn.github.io/dlco-lecture-note/exp/11.html)
- [实验十二 计算机系统](https://nju-projectn.github.io/dlco-lecture-note/exp/12.html)

[南京大学 计算机科学与技术系 数字逻辑与计算机组成 课程实验](https://nju-projectn.github.io/dlco-lecture-note/index.html)

- 实验二 译码器和编码器

---

<a id="id1"></a>



# 实验二 译码器和编码器[](#id1 "Permalink to this heading")

> 伊吉斯将另一面白色的帆交给领航，特别交代他在回航的时候，如果帖修斯平安归来，就将这面船帆升起来；要是事与愿违就用黑色的船帆，等于是悬挂出不幸的信号。
>
> —《希腊罗马名人传》，普鲁塔克

译码器和编码器是数字系统中的常用电路，也是组合逻辑电路中的主要组成元件之一。本实验首先介绍常用的译码器和编码器的设计方法以及七段数码管的使用。本实验还将介绍Verilog语言中for循环的使用。最后，请读者自行设计一个8-3优先编码器及七段数码管显示。

<a id="id2"></a>



## 译码器[](#id2 "Permalink to this heading")

译码器也是组合逻辑电路的一个重要器件，译码器是将某一输入信息转换为某一特定输出的逻辑电路，通常是多路输入/输出电路，它将 \(n\) 位的输入编码转换为 \(m\) 位的编码输出，一般情况下 \(n<m\) ，输入编码和输出编码之间存在着一一对应的映射关系，每个输入编码产生唯一的一个不同于其他的输出编码。

常用的二进制译码器（如下图所示）是一个有 \(n\) 路输入和 \(m=2^n\) 路输出的逻辑电路。译码器有一个使能信号En，当En=0时，无论输入为什么，译码器没有任何有效值输出；当En=1时，输入的值决定了输出信号的值。在二进制码中，最常用的输出编码是 \(m=2^n\) 位中取1位编码，即任何时刻， \(m\) 位输出编码中只能有1位有效，其余各位都为0，这样的二进制编码被称为独热编码（one-hot encoded），意思是那个被置为1的码看起来是“热”的，而二进制译码器输出的信号就是独热编码。

<a id="id10"></a>


![../_images/decoder1.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/decoder1.png)

Fig. 8 \(n\) 位输入， \(2^n\) 位输出的译码器[](#id10 "Permalink to this image")

本次实验首先具体介绍2-4译码器和3-8译码器的工作原理，学习译码器的设计。

<a id="id3"></a>



### 2-4译码器[](#id3 "Permalink to this heading")

2-4译码器（如下图所示），它的输入信号是 \(x\_0\) 和 \(x\_1\) ，对每一个二进制输入信号 \(x\_0\) 和 \(x\_1\) 进行译码，译码输出是在 \(y\_0\) 、 \(y\_1\) 、 \(y\_2\) 和 \(y\_3\) 四位中选择一位使其有效。译码器的输出可以设计成高电平有效或低电平有效，在本例中采用的是高电平有效。

<a id="id11"></a>


![../_images/decoder24.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/decoder24.png)

Fig. 9 2-4译码器[](#id11 "Permalink to this image")

译码器的逻辑电路图如下所示。

<a id="id12"></a>


![../_images/decoder242.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/decoder242.png)

Fig. 10 2-4译码器逻辑电路[](#id12 "Permalink to this image")

可以采用硬件描述语言来实现2-4译码器电路。以下是一个带有使能端的2-4译码器的代码：

<a id="id13"></a>



Listing 9 2-4译码器代码[](#id13 "Permalink to this code")



```
module decode24(x,en,y);
  input  [1:0] x;
  input  en;
  output reg [3:0]y;

  always @(x or en)
    if (en)
    begin
      case (x)
            2'd0 : y = 4'b0001;
            2'd1 : y = 4'b0010;
            2'd2 : y = 4'b0100;
            2'd3 : y = 4'b1000;
      endcase
    end
    else  y = 4'b0000;

endmodule
```



程序中用到了数值字串（literal） `n'Bdd...d` ，其中n是字串的位数，用十进制表示，这里字串的位数是 `dd...d` ，这个值存放在机器中（二进制）所用的位数，而不是其用 `B` 进制表示的位数。 `B` 是指定基数的单个字母，可以是b（二进制），o（八进制），d（十进制，可省略）和h（十六进制）。 `dd...d` 是此数值字串，用 `B` 进制表示的值。

输入设计好的程序代码后，再输入激励代码，对设计进行仿真。

<a id="id14"></a>



Listing 10 2-4译码器测试代码[](#id14 "Permalink to this code")



```
int main() {
  sim_init();

  top->en = 0b0;  top->x = 0b00;  step_and_dump_wave();
                  top->x = 0b01;  step_and_dump_wave();
                  top->x = 0b10;  step_and_dump_wave();
                  top->x = 0b11;  step_and_dump_wave();
  top->en = 0b1;  top->x = 0b00;  step_and_dump_wave();
                  top->x = 0b01;  step_and_dump_wave();
                  top->x = 0b10;  step_and_dump_wave();
                  top->x = 0b11;  step_and_dump_wave();
  sim_exit();
}
```



对所设计电路进行功能仿真，如下图所示，分析时序图发现，结果和真值表一致。

<a id="id15"></a>


![../_images/decodersim.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/decodersim.png)

Fig. 11 2-4译码器仿真结果[](#id15 "Permalink to this image")

for循环语句

我们也可以利用一个for循环语句来实现3-8译码器。



```
module decode38(x,en,y);
  input  [2:0] x;
  input  en;
  output reg [7:0]y;
  integer i;

  always @(x or en)
    if (en) begin
      for( i = 0; i <= 7; i = i+1)
          if(x == i)
                y[i] = 1;
          else
                y[i] = 0;
    end
    else
      y = 8'b00000000;

endmodule
```



此代码中重复使用了if-else语句，请注意if和else之间的配对情况。

另外代码中还使用了for 循环语句。for 循环语句也是Verilog HDL常用的语句之一，一个for 循环语句按照指定的次数重复执行过程赋值语句若干次。其格式为：



```
for ( initial_assignment; condition; step_assignment )
```



初始赋值initial\_assignment给出循环变量的初始值。condition条件表达式指定循环在什么情况下必须结束；只要条件为真，循环中的语句就执行。而step\_assignment给出要修改的赋值，通常为增加或减少循环变量计数。

for循环的条件表达式

在Verilog HDL代码中，for循环的condition条件表达式必须为常数，不能是可改变的量。

<a id="id4"></a>



## 编码器[](#id4 "Permalink to this heading")

编码器是一种与译码器功能相反的逻辑电路，编码器的输出编码比其输入编码位数少。

常用的二进制编码器把来自于 \(2^n\) 条输入线的信息编码转换成 \(n\) 位二进制码，如下图所示。二进制编码器每次输入的 \(2^n\) 位信号中只能有一位为1，其余均为0（即独热码），编码器的输出端为一个二进制数，用来指示对应的哪一个位输入为1。

<a id="id16"></a>


![../_images/encoder1.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/encoder1.png)

Fig. 12 \(2^n\) 位输入， \(n\) 位输出的编码器[](#id16 "Permalink to this image")

<a id="id5"></a>



### 4-2编码器[](#id5 "Permalink to this heading")

4-2编码器即为4位输入2位输出的编码器（如下所示），它的输入信号是 \(x\_0\) 、 \(x\_1\) 、 \(x\_2\) 和 \(x\_3\) ，输出是 \(y\_0\) 和 \(y\_1\) 。本例中采用独热码，每次输入中只有一位为1，对于有两位或者两位以上为1的情况，则将输出置为高阻态。

<a id="id17"></a>



Table 1 4-2编码器真值表[](#id17 "Permalink to this table")








| \(x\_3\) | \(x\_2\) | \(x\_1\) | \(x\_0\) | \(y\_1\) | \(y\_0\) |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 |

4-2编码器的代码如下所示：

<a id="id18"></a>



Listing 11 4-2编码器代码[](#id18 "Permalink to this code")



```
module encode42(x,en,y);
  input  [3:0] x;
  input  en;
  output reg [1:0]y;

  always @(x or en) begin
    if (en) begin
      case (x)
          4'b0001 : y = 2'b00;
          4'b0010 : y = 2'b01;
          4'b0100 : y = 2'b10;
          4'b1000 : y = 2'b11;
          default: y = 2'b00;
      endcase
    end
    else  y = 2'b00;
  end
endmodule
```



以下为该4-2编码器的测试代码。

<a id="id19"></a>



Listing 12 4-2编码器测试代码[](#id19 "Permalink to this code")



```
int main() {
  sim_init();

  top->en=0b0; top->x =0b0000; step_and_dump_wave();
               top->x =0b0001; step_and_dump_wave();
               top->x =0b0010; step_and_dump_wave();
               top->x =0b0100; step_and_dump_wave();
               top->x =0b1000; step_and_dump_wave();
  top->en=0b1; top->x =0b0000; step_and_dump_wave();
               top->x =0b0001; step_and_dump_wave();
               top->x =0b0010; step_and_dump_wave();
               top->x =0b0100; step_and_dump_wave();
               top->x =0b1000; step_and_dump_wave();
  sim_exit();
}
```



其仿真结果如下图所示：

<a id="id20"></a>


![../_images/encoder42sim.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/encoder42sim.png)

Fig. 13 4-2编码器仿真结果[](#id20 "Permalink to this image")

<a id="id6"></a>



### 优先编码器[](#id6 "Permalink to this heading")

优先编码器允许同时在几个输入端有输入信号，即输入不止一个 `1` ，编码器按输入信号排定的优先顺序，只对同时输入的几个信号中优先权最高的一个进行编码。

我们可以利用for循环语句可以很方便地实现优先编码器，一个4-2优先编码器的示例如下所示。



```
module encode42(x,en,y);
  input  [3:0] x;
  input  en;
  output reg [1:0]y;
  integer i;
  always @(x or en) begin
    if (en) begin
      y = 0;
      for( i = 0; i <= 3; i = i+1)
          if(x[i] == 1)  y = i[1:0];
    end
    else  y = 0;
  end
endmodule
```



请大家为上述代码编写一段测试代码，并对其进行仿真，查看仿真结果。

<a id="id7"></a>



### 七段数码管[](#id7 "Permalink to this heading")

七段LED数码管是一种常用的显示元件，常应用于手表、计算器等仪器中，用于显示数值。下图是数码管的原理图，数码管分为共阴极和共阳极两种类型，共阴极就是将七个LED的阴极连在一起，让其接低电平。这样给任何一个LED的另一端高电平，它便能点亮。而共阳极就是将七个LED的阳极连在一起，让其接高电平。这样，给任何一个LED的另一端低电平，它就能点亮。

<a id="id21"></a>


![../_images/7seg1.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7seg1.png)

Fig. 14 数码管原理图[](#id21 "Permalink to this image")

DE10-Standard 开发板上的数码管就是七段共阳极的。每个数码管的七段LED的一端连接在一个共同的阳极上，另一端和开发板上Cyclone V SoC FPGA的某一个引脚连接在一起，如下图所示，如果从这个引脚输出一个逻辑0，则此段数码管被点亮。

<a id="id22"></a>


![../_images/7seg2.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7seg2.png)

Fig. 15 DE10-Standard数码管连接[](#id22 "Permalink to this image")

DE10-Standard 开发板共有六个数码管，各数码管和FPGA的引脚连接如下图所示

![../_images/7seg3.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7seg3.png)
<a id="id23"></a>


![../_images/7seg4.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7seg4.png)

Fig. 16 DE10-Standard数码管引脚[](#id23 "Permalink to this image")

数字1~9及十六进制的a~f在数码管上的显示方式如下图所示。

<a id="id24"></a>



Table 2 七段数码管显示方式[](#id24 "Permalink to this table")

|  |  |
| --- | --- |
| ![../_images/7seg5.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7seg5.png) | ![../_images/7segabcd.png](../../assets/offline/nju-projectn.github.io/dlco-lecture-note/_images/7segabcd.png) |

以HEX0为例，如果要在此数码管上显示数字 `1` ，则只要在和HEX0[1]以及 HEX0[2]两段LED相连的FPGA引脚PIN\_V18 和PIN\_AG17端输出逻辑 `0` ，其他输出 `1` 即可。

请自行设计数码管的对应编码。

<a id="id8"></a>



### 模块实例化[](#id8 "Permalink to this heading")

在数字系统设计过程中，我们经常需要将一个大的系统切分成多个小的子模块。
这样一方面可以将复杂的系统分层简化，对每个小模块进行单独设计，编码和调试。
另一方面也可以将小模块做为一个可重复使用的单元，在不同的项目中重复使用。

本实验中的七段数码管就是一个典型的可复用模块，在后续实验中如果需要利用数码管来显示调试数据可以直接调用本实验写好的模块。
七段数码管模块bcd7seg的输入输出接口如下所示。输入是四位的BCD码b,输出是七段数码管的译码结果h。

<a id="id25"></a>



Listing 13 七段数码管编码的模块接口[](#id25 "Permalink to this code")



```
module bcd7seg(
  input  [3:0] b,
  output reg [6:0] h
);
// detailed implementation ...

endmodule
```



在使用该模块时，我们可以对模块进行实例化。

例如，我们需要对六个数码管HEX0~HEX5进行编码输出时，可以实例化六个bcd7seg模块，如下所示。

<a id="id26"></a>



Listing 14 模块实例化[](#id26 "Permalink to this code")



```
//output debuginfo to bcd
bcd7seg seg5(cpudbgdata[23:20],HEX5);
bcd7seg seg4(cpudbgdata[19:16],HEX4);
bcd7seg seg3(cpudbgdata[15:12],HEX3);
bcd7seg seg2(cpudbgdata[11:8],HEX2);
bcd7seg seg1(cpudbgdata[7:4],HEX1);
bcd7seg seg0(cpudbgdata[3:0],HEX0);
```



Verilog的模块实例化

Verilog的模块实例化与高级语言函数调用有本质区别，实例化更加类似于从芯片库中取出一块芯片，给它起一个名字（实例名），然后连接输入输出引脚。因此，模块实例化同assign语句一样，只能在always语句块之外进行。

<a id="id9"></a>



## 实验验收内容[](#id9 "Permalink to this heading")

上板实验: 实现一个8-3优先编码器并在七段数码管上显示

**功能描述**

查找8-3优先编码器相关原理和实现方法，实现一个8-3编码器，完成8-3编码器的设计、功能仿真和硬件实现。

输入一个8位二进制数，对此8位二进制数进行高位优先编码成一个3位二进制值，并根据是否有输入增加一位输入指示位，即8个输入全0时指示位为0，有任何一个输入为1时指示位为1。编码器的使能端可选实现。将此编码结果及指示位以二进制形式显示在四个发光二极管LED上。再将此结果跟据七段数码管的显示进行译码，将二进制的优先编码结果以十进制的形式显示在数码管上。

**输入输出建议**

输入可以使用拨动开关SW7-SW0。使能端可以用SW8。输出为LED2-0，输出指示可以是LED4，数码管输出为HEX0。

例：我们从SW7—SW0输入00001110，因为我们设计的是一个高位优先的优先编码器，从左（高位）开始，第一位为1的是第3号位，那么优先编码器的编码二进制结果就为011，将这个值显示在发光二极管上，并且指示位也同时置为1。再对这个数值跟据七段数码管的显示进行译码，此时应显示为 `3` ，用HEX0显示，所以HEX0[6:0]应该译码为0110000（注意高低位顺序），那么在七段数码管上就会显示 `3` 这个字符。

casex和casez语句

查阅相关资料，了解casex和casez语句的使用，思考如何用casex语句来完成优先编码器的设计？

在线测试

在线验证优先编码器和数码管显示代码

在线测试

格雷码

[Previous](865441e486a9b3d5.md "实验一 选择器")
[Next](1a5b5cc32fc96bd9.md "实验三 加法器与ALU")

---

© Copyright 2022, 王炜 吴海军 陈璐.

Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme)
provided by [Read the Docs](https://readthedocs.org).
