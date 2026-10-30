# E1：HDLBits 逐题要求

E1 给出九道较难题作为自检；遇到困难时走指定基础路径。此处完整列出基础路径及建议语法练习，不把全站 182 题都改成必做。九道自检题已包含在 FSM 题中，不重复计数。所有题状态均为 NOT_RUN。

同名的两个 “Mux and DFF” 和两个 “Shift register” 在网站上是不同题；E1 未给子题 URL，此处保留两题，注明同名歧义，审阅时可决定采用哪题或都做。

题目图、真值表、时序图、端口声明保留在各题本地原文。这里只列目标、接口和验收交付，不下载/展示网站参考答案，不要求在线提交或账号。

<a id="hdl-001"></a>

### HDL-001 Getting Started

来源：本地原文（原完整交付引用：`<../references/markdown/24a46b4ef8d49b2d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/step_one)

**实现要求**（保留原题的代码、列表及子问）：

[*Index*](../references/markdown/dbe4a81cda9a0a03.md "Problem sets")Previous

Next[zero](../references/markdown/13af1bfb56e32a4e.md "zero")

Welcome to HDLBits!

Getting started in digital logic design can be overwhelming at first because you need to learn new concepts, a new **H**ardware **D**escription **L**anguage (e.g., Verilog), several new software packages, and often an FPGA board, *all at the same time*. HDLBits provides a way to practice designing and debugging simple circuits with a single click of "Simulate".

Designing a circuit requires several steps: Writing HDL (Verilog) code, compiling the code to produce a circuit, then simulating the circuit and fixing bugs.

### Writing Code

The easiest way to write your code is to do so in the code editor box below. For this problem, we have filled in most of the code for you already. Go ahead and finish the code for this circuit.

Click **Simulate** to compile and simulate your design.

### Compiling (Logic Synthesis)

Your code is compiled using Altera Quartus to produce a circuit. Quartus produces a large number of messages. Click **Show Quartus messages** to show/hide them. It's good practice to reduce the number of warnings, but it is sometimes not practical to remove them all.

### Simulation

Your compiled circuit is simulated to test whether it functions correctly. HDLBits use ModelSim to simulate your circuit and our reference solution in parallel, then compares the outputs of the modules. The simulation reports back two things:

First, it reports whether your circuit matches the reference circuit exactly (zero "mismatches") or how many "mismatches" occurred. A mismatch is the number of samples where the output of your circuit does not match the reference output.

Second, it may produce timing diagrams that show your circuit outputs when running our test vectors. The simulation waveform is grouped into three sections: "Inputs", "Yours", and "Ref". In a correct circuit, "Your" outputs will be the same as the "Ref" outputs. The "Mismatch" signals tells you which samples have a mismatch.

The module name and port names of the top-level `top_module` must not be changed, or you will get a simulation error.

### Final Status

If your circuit was correct, you will see **Status: Success!**. There are a few other possibilities:

- **Compile Error** — Circuit did not compile.
- **Simulation Error** — Circuit compiled successfully, but simulation did not complete.
- **Incorrect** — Circuit compiled and simulated, but the outputs did not match the reference.
- **Success!** — Circuit was correct

You can track or share your progress on the **[My Stats](https://hdlbits.01xz.net/wiki/Special:VlgStats/Me "Special:VlgStats/Me")** page.

### Problem Statement

We're going to start with a small bit of HDL to get familiar with the interface used by HDLBits. Here's the description of the circuit you need to build for this exercise:

Build a circuit with no inputs and one output. That output should always drive 1 (or logic high).

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- ·

**step\_one**

- · [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")

[*Index*](../references/markdown/dbe4a81cda9a0a03.md "Problem sets")Previous

Next[zero](../references/markdown/13af1bfb56e32a4e.md "zero")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( output one );
```

<a id="hdl-002"></a>

### HDL-002 Output Zero

来源：本地原文（原完整交付引用：`<../references/markdown/13af1bfb56e32a4e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/zero)

**实现要求**（保留原题的代码、列表及子问）：

[step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")Previous

Next[wire](../references/markdown/7718f7c36bb79a09.md "wire")

Build a circuit with no inputs and one output that outputs a constant 0

Now that you've worked through the previous problem, let's see if you can do a simple problem without the hints.

HDLBits uses Verilog-2001 ANSI-style port declaration syntax because it's easier to read and reduces typos. You may use the older Verilog-1995 syntax if you wish. For example, the two module declarations below are acceptable and equivalent:
  



```
module top_module ( zero );
    output zero;
    // Verilog-1995
endmodule
```





```
module top_module ( output zero ); 

    // Verilog-2001
endmodule
```



***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one") ·

**zero**

- · [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")

[step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")Previous

Next[wire](../references/markdown/7718f7c36bb79a09.md "wire")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( zero );
    output zero;
    // Verilog-1995
endmodule
```

<a id="hdl-003"></a>

### HDL-003 Simple wire

来源：本地原文（原完整交付引用：`<../references/markdown/7718f7c36bb79a09.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/wire)

**实现要求**（保留原题的代码、列表及子问）：

[zero](../references/markdown/13af1bfb56e32a4e.md "zero")Previous

Next[wire4](../references/markdown/8252b824e0612819.md "wire4")

Create a module with one input and one output that behaves like a wire.

Unlike physical wires, wires (and other signals) in Verilog are *directional*. This means information flows in only one direction, from (usually one) *source* to the *sinks* (The source is also often called a *driver* that *drives* a value onto a wire). In a Verilog "continuous assignment" (`assign left_side = right_side;`), the value of the signal on the right side is driven onto the wire on the left side. The assignment is "continuous" because the assignment continues all the time even if the right side's value changes. A continuous assignment is not a one-time event.

The ports on a module also have a direction (usually input or output). An input port is *driven by* something from outside the module, while an output port *drives* something outside. When viewed from inside the module, an input port is a driver or source, while an output port is a sink.

The diagram below illustrates how each part of the circuit corresponds to each bit of Verilog code. The module and port declarations create the black portions of the circuit. Your task is to create a wire (in green) by adding an `assign` statement to connect `in` to `out`. The parts outside the box are not your concern, but you should know that your circuit is tested by connecting signals from our test harness to the ports on your `top_module`.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/7/77/Wire.png`）](https://hdlbits.01xz.net/wiki/File:Wire.png)

In addition to continuous assignments, Verilog has three other assignment types that are used in procedural blocks, two of which are synthesizable. We won't be using them until we start using procedural blocks.

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero") ·

**wire**

- · [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")

[zero](../references/markdown/13af1bfb56e32a4e.md "zero")Previous

Next[wire4](../references/markdown/8252b824e0612819.md "wire4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( input in, output out );
```

<a id="hdl-004"></a>

### HDL-004 Four wires

来源：本地原文（原完整交付引用：`<../references/markdown/8252b824e0612819.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/wire4)

**实现要求**（保留原题的代码、列表及子问）：

[wire](../references/markdown/7718f7c36bb79a09.md "wire")Previous

Next[notgate](../references/markdown/66299c9368857a86.md "notgate")

Create a module with 3 inputs and 4 outputs that behaves like wires that makes these connections:



```
a -> w
b -> x
b -> y
c -> z
```



The diagram below illustrates how each part of the circuit corresponds to each bit of Verilog code.
From outside the module, there are three input ports and four output ports.

When you have multiple assign statements, the **order** in which they appear in the code **does not matter**. Unlike a programming language, assign statements ("continuous assignments") describe *connections* between things, not the *action* of copying a value from one thing to another.

One potential source of confusion that should perhaps be clarified now: The green arrows here represent
connections *between* wires, but are not wires in themselves. The module itself *already* has 7 wires declared (named a, b, c, w, x, y, and z). This is because `input` and `output` declarations
actually declare a wire unless otherwise specified. Writing `input wire a` is the same as `input a`. Thus, the `assign` statements are not creating wires, they are creating the connections between
the 7 wires that already exist.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/1/15/Wire4.png`）](https://hdlbits.01xz.net/wiki/File:Wire4.png)

***Expected solution length:** Around 4 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire") ·

**wire4**

- · [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")

[wire](../references/markdown/7718f7c36bb79a09.md "wire")Previous

Next[notgate](../references/markdown/66299c9368857a86.md "notgate")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input a,b,c,
    output w,x,y,z );
```

<a id="hdl-005"></a>

### HDL-005 Inverter

来源：本地原文（原完整交付引用：`<../references/markdown/66299c9368857a86.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/notgate)

**实现要求**（保留原题的代码、列表及子问）：

[wire4](../references/markdown/8252b824e0612819.md "wire4")Previous

Next[andgate](../references/markdown/6ae043af8880cc6d.md "andgate")

Create a module that implements a NOT gate.

This circuit is similar to [wire](../references/markdown/7718f7c36bb79a09.md "wire"), but with a slight difference. When making the connection from the wire `in` to the wire `out` we're going to implement an inverter (or "NOT-gate") instead of a plain wire.

Use an assign statement. The `assign` statement will *continuously drive* the inverse of `in` onto wire `out`.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/9/9e/Notgate.png`）](https://hdlbits.01xz.net/wiki/File:Notgate.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4") ·

**notgate**

- · [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")

[wire4](../references/markdown/8252b824e0612819.md "wire4")Previous

Next[andgate](../references/markdown/6ae043af8880cc6d.md "andgate")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( input in, output out );
```

<a id="hdl-006"></a>

### HDL-006 AND gate

来源：本地原文（原完整交付引用：`<../references/markdown/6ae043af8880cc6d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/andgate)

**实现要求**（保留原题的代码、列表及子问）：

[notgate](../references/markdown/66299c9368857a86.md "notgate")Previous

Next[norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")

Create a module that implements an AND gate.

This circuit now has three wires (`a`, `b`, and `out`). Wires `a` and `b` already have values driven onto them by the input ports. But wire `out` currently is not driven by anything. Write an `assign` statement that drives `out` with the AND of signals `a` and `b`.

Note that this circuit is very similar to the [NOT gate](../references/markdown/66299c9368857a86.md "notgate"), just with one more input. If it sounds different, it's because I've started describing signals as being *driven* (has a known value determined by something attached to it) or *not driven* by something. `Input wires` are driven by something outside the module. `assign` statements will drive a logic level onto a wire. As you might expect, a wire cannot have more than one driver (what is its logic level if there is?), and a wire that has no drivers will have an undefined value (often treated as 0 when synthesizing hardware).

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/7/78/Andgate.png`）](https://hdlbits.01xz.net/wiki/File:Andgate.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate") ·

**andgate**

- · [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")

[notgate](../references/markdown/66299c9368857a86.md "notgate")Previous

Next[norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input a, 
    input b, 
    output out );
```

<a id="hdl-007"></a>

### HDL-007 NOR gate

来源：本地原文（原完整交付引用：`<../references/markdown/cc5eeeb9282026ce.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/norgate)

**实现要求**（保留原题的代码、列表及子问）：

[andgate](../references/markdown/6ae043af8880cc6d.md "andgate")Previous

Next[xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")

Create a module that implements a NOR gate. A NOR gate is an OR gate with its output inverted. A NOR function needs two operators when written in Verilog.

An `assign` statement drives a wire (or "net", as it's more formally called) with a value. This value can be as complex a function as you want, as long as it's a *combinational* (i.e., memory-less, with no hidden state) function. An `assign` statement is a *continuous assignment* because the output is "recomputed" whenever any of its inputs change, forever, much like a simple logic gate.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/5/5b/Norgate.png`）](https://hdlbits.01xz.net/wiki/File:Norgate.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate") ·

**norgate**

- · [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")

[andgate](../references/markdown/6ae043af8880cc6d.md "andgate")Previous

Next[xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input a, 
    input b, 
    output out );
```

<a id="hdl-008"></a>

### HDL-008 XNOR gate

来源：本地原文（原完整交付引用：`<../references/markdown/2eaf7265d46dd9b6.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/xnorgate)

**实现要求**（保留原题的代码、列表及子问）：

[norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")Previous

Next[wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")

Create a module that implements an XNOR gate.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/6/6d/Xnorgate.png`）](https://hdlbits.01xz.net/wiki/File:Xnorgate.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate") ·

**xnorgate**

- · [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")

[norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")Previous

Next[wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input a, 
    input b, 
    output out );
```

<a id="hdl-009"></a>

### HDL-009 Declaring wires

来源：本地原文（原完整交付引用：`<../references/markdown/24f5dc891e06259d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/wire_decl)

**实现要求**（保留原题的代码、列表及子问）：

[xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")Previous

Next[7458](../references/markdown/09ec3ebf14cf3512.md "7458")

## Declaring wires

The circuits so far have been simple enough that the outputs are simple functions of the inputs. As circuits become more complex, you will need wires to connect internal components together. When you need to use a wire, you should declare it in the body of the module, somewhere before it is first used. (In the future, you will encounter more types of signals and variables that are also declared the same way, but for now, we'll start with a signal of type wire).

### Example

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/6/6a/Wiredecl1.png`）](https://hdlbits.01xz.net/wiki/File:Wiredecl1.png)



```
module top_module (
    input in,              // Declare an input wire named "in"
    output out             // Declare an output wire named "out"
);

    wire not_in;           // Declare a wire named "not_in"

    assign out = ~not_in;  // Assign a value to out (create a NOT gate).
    assign not_in = ~in;   // Assign a value to not_in (create another NOT gate).

endmodule   // End of module "top_module"
```



In the above module, there are three wires (in, out, and not\_in), two of which are already declared as part of the module's input and output ports (This is why you didn't need to declare any wires in the earlier exercises). The wire not\_in needs to be declared inside the module. It is not visible from outside the module. Then, two NOT gates are created using two assign statements. Note that it doesn't matter which of the NOT gates you create first: You still end up with the same circuit.

## Practice

Implement the following circuit. Create two intermediate wires (named anything you want) to connect the AND and OR gates together. Note that the wire that feeds the NOT gate is really wire out, so you do not necessarily need to declare a third wire here. Notice how wires are driven by exactly one source (output of a gate), but can feed multiple inputs.

If you're following the circuit structure in the diagram, you should end up with four assign statements, as there are four signals that need a value assigned.

(Yes, it is possible to create a circuit with the same functionality without the intermediate wires.)

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/3/3a/Wiredecl2.png`）](https://hdlbits.01xz.net/wiki/File:Wiredecl2.png)

***Expected solution length:** Around 5 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [step\_one](../references/markdown/24a46b4ef8d49b2d.md "step_one")
- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate") ·

**wire\_decl**

- · [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")

[xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")Previous

Next[7458](../references/markdown/09ec3ebf14cf3512.md "7458")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input in,              // Declare an input wire named "in"
    output out             // Declare an output wire named "out"
);

    wire not_in;           // Declare a wire named "not_in"

    assign out = ~not_in;  // Assign a value to out (create a NOT gate).
    assign not_in = ~in;   // Assign a value to not_in (create another NOT gate).

endmodule   // End of module "top_module"
```

<a id="hdl-010"></a>

### HDL-010 7458 chip

来源：本地原文（原完整交付引用：`<../references/markdown/09ec3ebf14cf3512.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/7458)

**实现要求**（保留原题的代码、列表及子问）：

[wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")Previous

Next[vector0](../references/markdown/1c057655620ee342.md "vector0")

The 7458 is a chip with four AND gates and two OR gates. This problem is slightly more complex than [7420](../references/markdown/99ab7ded006d728b.md "7420").

Create a module with the same functionality as the 7458 chip. It has 10 inputs and 2 outputs. You may choose to use an `assign` statement to drive each of the output wires, or you may choose to declare (four) wires for use as intermediate signals, where each internal wire is driven by the output of one of the AND gates. For extra practice, try it both ways.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/e/e1/7458.png`）](https://hdlbits.01xz.net/wiki/File:7458.png)

***Expected solution length:** Around 2–10 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [zero](../references/markdown/13af1bfb56e32a4e.md "zero")
- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl") ·

**7458**

- · [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")

[wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")Previous

Next[vector0](../references/markdown/1c057655620ee342.md "vector0")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( 
    input p1a, p1b, p1c, p1d, p1e, p1f,
    output p1y,
    input p2a, p2b, p2c, p2d,
    output p2y );
```

<a id="hdl-011"></a>

### HDL-011 Vectors

来源：本地原文（原完整交付引用：`<../references/markdown/1c057655620ee342.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector0)

**实现要求**（保留原题的代码、列表及子问）：

[7458](../references/markdown/09ec3ebf14cf3512.md "7458")Previous

Next[vector1](../references/markdown/f2d96056c06db7ca.md "vector1")

Vectors are used to group related signals using one name to make it more convenient to manipulate. For example, wire [7:0] w; declares an 8-bit vector named w that is functionally equivalent to having 8 separate wires.

Notice that the *declaration* of a vector places the dimensions *before* the name of the vector, which is unusual compared to C syntax. However, the *part select* has the dimensions *after* the vector name as you would expect.

`wire [99:0] my_vector; // Declare a 100-element vector
assign out = my_vector[10]; // Part-select one bit out of the vector`

Build a circuit that has one 3-bit input, then outputs the same vector, and also splits it into three separate 1-bit outputs. Connect output `o0` to the input vector's position 0, `o1` to position 1, etc.

In a diagram, a tick mark with a number next to it indicates the width of the vector (or "bus"), rather than drawing a separate line for each bit in the vector.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/ae/Vector0.png`）](https://hdlbits.01xz.net/wiki/File:Vector0.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [wire](../references/markdown/7718f7c36bb79a09.md "wire")
- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458") ·

**vector0**

- · [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")

[7458](../references/markdown/09ec3ebf14cf3512.md "7458")Previous

Next[vector1](../references/markdown/f2d96056c06db7ca.md "vector1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( 
    input wire [2:0] vec,
    output wire [2:0] outv,
    output wire o2,
    output wire o1,
    output wire o0  );
```

<a id="hdl-012"></a>

### HDL-012 Vectors in more detail

来源：本地原文（原完整交付引用：`<../references/markdown/f2d96056c06db7ca.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector1)

**实现要求**（保留原题的代码、列表及子问）：

[vector0](../references/markdown/1c057655620ee342.md "vector0")Previous

Next[vector2](../references/markdown/b98b67dfe943102e.md "vector2")

Vectors are used to group related signals using one name to make it more convenient to manipulate. For example, wire [7:0] w; declares an 8-bit vector named w that is equivalent to having 8 separate wires.

### Declaring Vectors

Vectors must be declared:

type [upper:lower] vector\_name;

type specifies the datatype of the vector. This is usually wire or reg. If you are declaring a input or output port, the type can additionally include the port type (e.g., input or output) as well. Some examples:



```
wire [7:0] w;         // 8-bit wire
reg  [4:1] x;         // 4-bit reg
output reg [0:0] y;   // 1-bit reg that is also an output port (this is still a vector)
input wire [3:-2] z;  // 6-bit wire input (negative ranges are allowed)
output [3:0] a;       // 4-bit output wire. Type is 'wire' unless specified otherwise.
wire [0:7] b;         // 8-bit wire where b[0] is the most-significant bit.
```



The *endianness* (or, informally, "direction") of a vector is whether the the least significant bit has a lower index (little-endian, e.g., [3:0]) or a higher index (big-endian, e.g., [0:3]). In Verilog, once a vector is declared with a particular endianness, it must always be used the same way. e.g., writing `vec[0:3]` when `vec` is declared `wire [3:0] vec;` is illegal. Being consistent with endianness is good practice, as weird bugs occur if vectors of different endianness are assigned or used together.

#### Implicit nets

Implicit nets are often a source of hard-to-detect bugs.
In Verilog, net-type signals can be implicitly created by an `assign` statement or by attaching something undeclared to a module port. Implicit nets are always one-bit wires and causes bugs if you had intended to use a vector. Disabling creation of implicit nets can be done using the `` `default_nettype none `` directive.

`wire [2:0] a, c; // Two vectors
assign a = 3'b101; // a = 101
assign b = a; // b = 1 implicitly-created wire
assign c = b; // c = 001 <-- bug
my_module i1 (d,e); // d and e are implicitly one-bit wide if not declared.  
 // This could be a bug if the port was intended to be a vector.`

Adding `` `default_nettype none `` would make the third line of code an error, which makes the bug more visible.

#### Unpacked vs. Packed Arrays

You may have noticed that in *declarations*, the vector indices are written *before* the vector name. This declares the "packed" dimensions of the array, where the bits are "packed" together into a blob (this is relevant in a simulator, but not in hardware). The *unpacked* dimensions are declared *after* the name. They are generally used to declare memory arrays. Since ECE253 didn't cover memory arrays, we have not used packed arrays in this course. See <http://www.asic-world.com/systemverilog/data_types10.html> for more details.



```
reg [7:0] mem [255:0];   // 256 unpacked elements, each of which is a 8-bit packed vector of reg.
reg mem2 [28:0];         // 29 unpacked elements, each of which is a 1-bit reg.
```



### Accessing Vector Elements: Part-Select

Accessing an entire vector is done using the vector name. For example:



```
assign w = a;
```



takes the entire 4-bit vector *a* and assigns it to the entire 8-bit vector *w* (declarations are taken from above). If the lengths of the right and left sides don't match, it is zero-extended or truncated as appropriate.

The part-select operator can be used to access a portion of a vector:



```
w[3:0]      // Only the lower 4 bits of w
x[1]        // The lowest bit of x
x[1:1]      // ...also the lowest bit of x
z[-1:-2]    // Two lowest bits of z
b[3:0]      // Illegal. Vector part-select must match the direction of the declaration.
b[0:3]      // The *upper* 4 bits of b.
assign w[3:0] = b[0:3];    // Assign upper 4 bits of b to lower 4 bits of w. w[3]=b[0], w[2]=b[1], etc.
```



## A Bit of Practice

Build a combinational circuit that splits an input half-word (16 bits, [15:0] ) into lower [7:0] and upper [15:8] bytes.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [wire4](../references/markdown/8252b824e0612819.md "wire4")
- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0") ·

**vector1**

- · [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")

[vector0](../references/markdown/1c057655620ee342.md "vector0")Previous

Next[vector2](../references/markdown/b98b67dfe943102e.md "vector2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
`default_nettype none     // Disable implicit nets. Reduces some types of bugs.
module top_module( 
    input wire [15:0] in,
    output wire [7:0] out_hi,
    output wire [7:0] out_lo );
```

<a id="hdl-013"></a>

### HDL-013 Vector part select

来源：本地原文（原完整交付引用：`<../references/markdown/b98b67dfe943102e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector2)

**实现要求**（保留原题的代码、列表及子问）：

[vector1](../references/markdown/f2d96056c06db7ca.md "vector1")Previous

Next[vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")

A 32-bit vector can be viewed as containing 4 bytes (bits [31:24], [23:16], etc.). Build a circuit that will reverse the *byte* ordering of the 4-byte word.



```
AaaaaaaaBbbbbbbbCcccccccDddddddd => DdddddddCcccccccBbbbbbbbAaaaaaaa
```



This operation is often used when the [endianness](https://en.wikipedia.org/wiki/Endianness) of a piece of data needs to be swapped, for example between little-endian x86 systems and the big-endian formats used in many Internet protocols.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [notgate](../references/markdown/66299c9368857a86.md "notgate")
- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1") ·

**vector2**

- · [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")

[vector1](../references/markdown/f2d96056c06db7ca.md "vector1")Previous

Next[vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [31:0] in,
    output [31:0] out );
```

<a id="hdl-014"></a>

### HDL-014 Bitwise operators

来源：本地原文（原完整交付引用：`<../references/markdown/e8ecaa747282f574.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vectorgates)

**实现要求**（保留原题的代码、列表及子问）：

[vector2](../references/markdown/b98b67dfe943102e.md "vector2")Previous

Next[gates4](../references/markdown/025ff45ba530f489.md "gates4")

Build a circuit that has two 3-bit inputs that computes the bitwise-OR of the two vectors, the logical-OR of the two vectors, and the inverse (NOT) of both vectors. Place the inverse of `b` in the upper half of `out_not` (i.e., bits [5:3]), and the inverse of `a` in the lower half.

### Bitwise vs. Logical Operators

Earlier, we mentioned that there are bitwise and logical versions of the various boolean operators (e.g., [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")). When using vectors, the distinction between the two operator types becomes important. A bitwise operation between two N-bit vectors replicates the operation for each bit of the vector and produces a N-bit output, while a logical operation treats the entire vector as a boolean value (true = non-zero, false = zero) and produces a 1-bit output.

Look at the simulation waveforms at how the bitwise-OR and logical-OR differ.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/1/1b/Vectorgates.png`）](https://hdlbits.01xz.net/wiki/File:Vectorgates.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [andgate](../references/markdown/6ae043af8880cc6d.md "andgate")
- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2") ·

**vectorgates**

- · [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")

[vector2](../references/markdown/b98b67dfe943102e.md "vector2")Previous

Next[gates4](../references/markdown/025ff45ba530f489.md "gates4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [2:0] a,
    input [2:0] b,
    output [2:0] out_or_bitwise,
    output out_or_logical,
    output [5:0] out_not
);
```

<a id="hdl-015"></a>

### HDL-015 Four-input gates

来源：本地原文（原完整交付引用：`<../references/markdown/025ff45ba530f489.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/gates4)

**实现要求**（保留原题的代码、列表及子问）：

[vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")Previous

Next[vector3](../references/markdown/c9c1f3730b421a10.md "vector3")

Build a combinational circuit with four inputs, in[3:0].

There are 3 outputs:

- out\_and: output of a 4-input AND gate.
- out\_or: output of a 4-input OR gate.
- out\_xor: output of a 4-input XOR gate.

To review the AND, OR, and XOR operators, see [andgate](../references/markdown/6ae043af8880cc6d.md "andgate"), [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate"), and [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate").

See also: [Even wider gates](../references/markdown/a28750136ece336b.md "gates100").

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [norgate](../references/markdown/cc5eeeb9282026ce.md "norgate")
- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates") ·

**gates4**

- · [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")

[vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")Previous

Next[vector3](../references/markdown/c9c1f3730b421a10.md "vector3")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [3:0] in,
    output out_and,
    output out_or,
    output out_xor
);
```

<a id="hdl-016"></a>

### HDL-016 Vector concatenation operator

来源：本地原文（原完整交付引用：`<../references/markdown/c9c1f3730b421a10.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector3)

**实现要求**（保留原题的代码、列表及子问）：

[gates4](../references/markdown/025ff45ba530f489.md "gates4")Previous

Next[vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")

[Part selection](https://hdlbits.01xz.net/wiki/Vector1 "Vector1") was used to select portions of a vector. The concatenation operator {a,b,c} is used to create larger vectors by concatenating smaller portions of a vector together.



```
{3'b111, 3'b000} => 6'b111000
{1'b1, 1'b0, 3'b101} => 5'b10101
{4'ha, 4'd10} => 8'b10101010     // 4'ha and 4'd10 are both 4'b1010 in binary
```



Concatenation needs to know the width of every component (or how would you know the length of the result?). Thus, {1, 2, 3} is illegal and results in the error message: unsized constants are not allowed in concatenations.

The concatenation operator can be used on both the left and right sides of assignments.



```
input [15:0] in;
output [23:0] out;
assign {out[7:0], out[15:8]} = in;         // Swap two bytes. Right side and left side are both 16-bit vectors.
assign out[15:0] = {in[7:0], in[15:8]};    // This is the same thing.
assign out = {in[7:0], in[15:8]};       // This is different. The 16-bit vector on the right is extended to
                                        // match the 24-bit vector on the left, so out[23:16] are zero.
                                        // In the first two examples, out[23:16] are not assigned.
```



## A Bit of Practice

Given several input vectors, concatenate them together then split them up into several output vectors. There are six 5-bit input vectors: a, b, c, d, e, and f, for a total of 30 bits of input. There are four 8-bit output vectors: w, x, y, and z, for 32 bits of output. The output should be a concatenation of the input vectors followed by two 1 bits:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/0/0c/Vector3.png`）](https://hdlbits.01xz.net/wiki/File:Vector3.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [xnorgate](../references/markdown/2eaf7265d46dd9b6.md "xnorgate")
- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4") ·

**vector3**

- · [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")

[gates4](../references/markdown/025ff45ba530f489.md "gates4")Previous

Next[vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input [4:0] a, b, c, d, e, f,
    output [7:0] w, x, y, z );
```

<a id="hdl-017"></a>

### HDL-017 Vector reversal 1

来源：本地原文（原完整交付引用：`<../references/markdown/47e5d50fe5de95ad.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vectorr)

**实现要求**（保留原题的代码、列表及子问）：

[vector3](../references/markdown/c9c1f3730b421a10.md "vector3")Previous

Next[vector4](../references/markdown/b63c1f13c650b833.md "vector4")

Given an 8-bit input vector [7:0], reverse its bit ordering.

See also: [Reversing a longer vector](https://hdlbits.01xz.net/wiki/Vector100r "Vector100r").

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [wire\_decl](../references/markdown/24f5dc891e06259d.md "wire_decl")
- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3") ·

**vectorr**

- · [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")

[vector3](../references/markdown/c9c1f3730b421a10.md "vector3")Previous

Next[vector4](../references/markdown/b63c1f13c650b833.md "vector4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [7:0] in,
    output [7:0] out
);
```

<a id="hdl-018"></a>

### HDL-018 Replication operator

来源：本地原文（原完整交付引用：`<../references/markdown/b63c1f13c650b833.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector4)

**实现要求**（保留原题的代码、列表及子问）：

[vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")Previous

Next[vector5](../references/markdown/0572c6851848d75b.md "vector5")

The [concatenation operator](https://hdlbits.01xz.net/wiki/Vector3 "Vector3") allowed concatenating together vectors to form a larger vector. But sometimes you want the same thing concatenated together many times, and it is still tedious to do something like assign a = {b,b,b,b,b,b};. The replication operator allows repeating a vector and concatenating them together:



```
{num{vector}}
```



This replicates *vector* by *num* times. *num* must be a constant. Both sets of braces are required.

Examples:



```
{5{1'b1}}           // 5'b11111 (or 5'd31 or 5'h1f)
{2{a,b,c}}          // The same as {a,b,c,a,b,c}
{3'd5, {2{3'd6}}}   // 9'b101_110_110. It's a concatenation of 101 with
                    // the second vector, which is two copies of 3'b110.
```



## A Bit of Practice

One common place to see a replication operator is when sign-extending a smaller number to a larger one, while preserving its signed value. This is done by replicating the sign bit (the most significant bit) of the smaller number to the left. For example, sign-extending 4'b**0**101 (5) to 8 bits results in 8'b**0000**0101 (5), while sign-extending 4'b**1**101 (-3) to 8 bits results in 8'b**1111**1101 (-3).

Build a circuit that sign-extends an 8-bit number to 32 bits. This requires a concatenation of 24 copies of the sign bit (i.e., replicate bit[7] 24 times) followed by the 8-bit number itself.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [7458](../references/markdown/09ec3ebf14cf3512.md "7458")
- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr") ·

**vector4**

- · [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")

[vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")Previous

Next[vector5](../references/markdown/0572c6851848d75b.md "vector5")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input [7:0] in,
    output [31:0] out );
```

<a id="hdl-019"></a>

### HDL-019 More replication

来源：本地原文（原完整交付引用：`<../references/markdown/0572c6851848d75b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector5)

**实现要求**（保留原题的代码、列表及子问）：

[vector4](../references/markdown/b63c1f13c650b833.md "vector4")Previous

Next[module](../references/markdown/1d9959f03f3c36ed.md "module")

Given five 1-bit signals (a, b, c, d, and e), compute all 25 pairwise one-bit comparisons in the 25-bit output vector. The output should be 1 if the two bits being compared are equal.



```
out[24] = ~a ^ a;   // a == a, so out[24] is always 1.
out[23] = ~a ^ b;
out[22] = ~a ^ c;
...
out[ 1] = ~e ^ d;
out[ 0] = ~e ^ e;
```



![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/ac/Vector5.png`）](https://hdlbits.01xz.net/wiki/File:Vector5.png)

As the diagram shows, this can be done more easily using the [replication](https://hdlbits.01xz.net/wiki/Vector4 "Vector4") and concatenation operators.

- The top vector is a concatenation of 5 repeats of each input
- The bottom vector is 5 repeats of a concatenation of the 5 inputs

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector0](../references/markdown/1c057655620ee342.md "vector0")
- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4") ·

**vector5**

- · [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")

[vector4](../references/markdown/b63c1f13c650b833.md "vector4")Previous

Next[module](../references/markdown/1d9959f03f3c36ed.md "module")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input a, b, c, d, e,
    output [24:0] out );
```

<a id="hdl-020"></a>

### HDL-020 Modules

来源：本地原文（原完整交付引用：`<../references/markdown/1d9959f03f3c36ed.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module)

**实现要求**（保留原题的代码、列表及子问）：

[vector5](../references/markdown/0572c6851848d75b.md "vector5")Previous

Next[module\_pos](../references/markdown/8633d439430db812.md "module_pos")

By now, you're familiar with a `module`, which is a circuit that interacts with its outside through input and output ports. Larger, more complex circuits are built by *composing* bigger modules out of smaller modules and other pieces (such as assign statements and always blocks) connected together. This forms a hierarchy, as modules can contain instances of other modules.

The figure below shows a very simple circuit with a sub-module. In this exercise, create one *instance* of module `mod_a`, then connect the module's three pins (`in1`, `in2`, and `out`) to your top-level module's three ports (wires `a`, `b`, and `out`). The module `mod_a` is provided for you — you must instantiate it.

When connecting modules, only the ports on the module are important. You do not need to know the code inside the module. The code for module `mod_a` looks like this:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.b0ce402142f2fadd.b0ce402142f2fadd.png`）](https://hdlbits.01xz.net/wiki/File:Module_moda.png)



```
module mod_a ( input in1, input in2, output out );
    // Module body
endmodule
```



The hierarchy of modules is created by instantiating one module inside another, as long as all of the modules used belong to the same project (so the compiler knows where to find the module). The code for one module is not written *inside* another module's body (Code for different modules are not nested).

You may connect signals to the module by port name or port position. For extra practice, try both methods.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/c/c0/Module.png`）](https://hdlbits.01xz.net/wiki/File:Module.png)

### Connecting Signals to Module Ports

There are two commonly-used methods to connect a wire to a port: by position or by name.

#### By position

The syntax to connect wires to ports by position should be familiar, as it uses a C-like syntax. When instantiating a module, ports are connected left to right according to the module's declaration. For example:

`mod_a instance1 ( wa, wb, wc );`

This instantiates a module of type `mod_a` and gives it an *instance name* of "instance1", then connects signal `wa` (outside the new module) to the **first** port (`in1`) of the new module, `wb` to the **second** port (`in2`), and `wc` to the **third** port (`out`). One drawback of this syntax is that if the module's port list changes, all instantiations of the module will also need to be found and changed to match the new module.

#### By name

Connecting signals to a module's ports *by name* allows wires to remain correctly connected even if the port list changes. This syntax is more verbose, however.

`mod_a instance2 ( .out(wc), .in1(wa), .in2(wb) );`

The above line instantiates a module of type `mod_a` named "instance2", then connects signal `wa` (outside the module) to the port **named** `in1`, `wb` to the port **named** `in2`, and `wc` to the port **named** `out`. Notice how the ordering of ports is irrelevant here because the connection will be made to the correct name, regardless of its position in the sub-module's port list. Also notice the period immediately preceding the port name in this syntax.

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector1](../references/markdown/f2d96056c06db7ca.md "vector1")
- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5") ·

**module**

- · [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")

[vector5](../references/markdown/0572c6851848d75b.md "vector5")Previous

Next[module\_pos](../references/markdown/8633d439430db812.md "module_pos")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module mod_a ( input in1, input in2, output out );
    // Module body
endmodule
```

<a id="hdl-021"></a>

### HDL-021 Connecting ports by position

来源：本地原文（原完整交付引用：`<../references/markdown/8633d439430db812.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_pos)

**实现要求**（保留原题的代码、列表及子问）：

[module](../references/markdown/1d9959f03f3c36ed.md "module")Previous

Next[module\_name](../references/markdown/5f282069004a8b30.md "module_name")

This problem is similar to the previous one ([module](../references/markdown/1d9959f03f3c36ed.md "module")). You are given a module named `mod_a` that has 2 outputs and 4 inputs, in that order. You must connect the 6 ports *by position* to your
top-level module's ports `out1`, `out2`, `a`, `b`, `c`, and `d`, in that order.

You are given the following module:

`module mod_a ( output, output, input, input, input, input );`

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/b/b7/Module_pos.png`）](https://hdlbits.01xz.net/wiki/File:Module_pos.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector2](../references/markdown/b98b67dfe943102e.md "vector2")
- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module") ·

**module\_pos**

- · [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")

[module](../references/markdown/1d9959f03f3c36ed.md "module")Previous

Next[module\_name](../references/markdown/5f282069004a8b30.md "module_name")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( 
    input a, 
    input b, 
    input c,
    input d,
    output out1,
    output out2
);
```

<a id="hdl-022"></a>

### HDL-022 Connecting ports by name

来源：本地原文（原完整交付引用：`<../references/markdown/5f282069004a8b30.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_name)

**实现要求**（保留原题的代码、列表及子问）：

[module\_pos](../references/markdown/8633d439430db812.md "module_pos")Previous

Next[module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")

This problem is similar to [module](../references/markdown/1d9959f03f3c36ed.md "module"). You are given a module named `mod_a` that has 2 outputs and 4 inputs, in some order. You must connect the 6 ports *by name* to your
top-level module's ports:

| Port in `mod_a` | Port in `top_module` |
| --- | --- |
| `output out1` | `out1` |
| `output out2` | `out2` |
| `input in1` | `a` |
| `input in2` | `b` |
| `input in3` | `c` |
| `input in4` | `d` |

You are given the following module:

`module mod_a ( output out1, output out2, input in1, input in2, input in3, input in4);`

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/d/dd/Module_name.png`）](https://hdlbits.01xz.net/wiki/File:Module_name.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vectorgates](../references/markdown/e8ecaa747282f574.md "vectorgates")
- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos") ·

**module\_name**

- · [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")

[module\_pos](../references/markdown/8633d439430db812.md "module_pos")Previous

Next[module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( 
    input a, 
    input b, 
    input c,
    input d,
    output out1,
    output out2
);
```

<a id="hdl-023"></a>

### HDL-023 Three modules

来源：本地原文（原完整交付引用：`<../references/markdown/a36ec3244f2d819b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_shift)

**实现要求**（保留原题的代码、列表及子问）：

[module\_name](../references/markdown/5f282069004a8b30.md "module_name")Previous

Next[module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")

You are given a module `my_dff` with two inputs and one output (that implements a D flip-flop). Instantiate three of them, then chain them together to make a shift register of length 3. The `clk` port needs to be connected to all instances.

The module provided to you is:
`module my_dff ( input clk, input d, output q );`

Note that to make the internal connections, you will need to declare some wires. Be careful about naming your wires and module instances: the names must be unique.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/6/60/Module_shift.png`）](https://hdlbits.01xz.net/wiki/File:Module_shift.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [gates4](../references/markdown/025ff45ba530f489.md "gates4")
- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name") ·

**module\_shift**

- · [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")

[module\_name](../references/markdown/5f282069004a8b30.md "module_name")Previous

Next[module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( input clk, input d, output q );
```

<a id="hdl-024"></a>

### HDL-024 Modules and vectors

来源：本地原文（原完整交付引用：`<../references/markdown/80a884be905ec48e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_shift8)

**实现要求**（保留原题的代码、列表及子问）：

[module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")Previous

Next[module\_add](../references/markdown/03cf4a90addf2490.md "module_add")

This exercise is an extension of [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift"). Instead of module ports being only single pins, we now have modules with vectors as ports, to which you will attach wire vectors instead of plain wires. Like everywhere else in Verilog, the vector length of the port does not have to match the wire connecting to it, but this will cause zero-padding or truncation of the vector. This exercise does not use connections with mismatched vector lengths.

You are given a module `my_dff8` with two inputs and one output (that implements a set of 8 D flip-flops). Instantiate three of them, then chain them together to make a 8-bit wide shift register of length 3. In addition, create a 4-to-1 multiplexer (not provided) that chooses what to output depending on `sel[1:0]`: The value at the input d, after the first, after the second, or after the third D flip-flop. (Essentially, `sel` selects how many cycles to delay the input, from zero to three clock cycles.)

The module provided to you is:
`module my_dff8 ( input clk, input [7:0] d, output [7:0] q );`

The multiplexer is not provided. One possible way to write one is inside an `always` block with a `case` statement inside. (See also: [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v"))

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/7/76/Module_shift8.png`）](https://hdlbits.01xz.net/wiki/File:Module_shift8.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector3](../references/markdown/c9c1f3730b421a10.md "vector3")
- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift") ·

**module\_shift8**

- · [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")

[module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")Previous

Next[module\_add](../references/markdown/03cf4a90addf2490.md "module_add")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module ( 
    input clk, 
    input [7:0] d, 
    input [1:0] sel, 
    output [7:0] q 
);
```

<a id="hdl-025"></a>

### HDL-025 Adder 1

来源：本地原文（原完整交付引用：`<../references/markdown/03cf4a90addf2490.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_add)

**实现要求**（保留原题的代码、列表及子问）：

[module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")Previous

Next[module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")

You are given a module `add16` that performs a 16-bit addition. Instantiate two of them to create a 32-bit adder. One add16 module computes the lower 16 bits of the addition result, while the second add16 module computes the upper 16 bits of the result, after receiving the carry-out from the first adder. Your 32-bit adder does not need to handle carry-in (assume 0) or carry-out (ignored), but the internal modules need to in order to function correctly. (In other words, the `add16` module performs 16-bit a + b + cin, while your module performs 32-bit a + b).

Connect the modules together as shown in the diagram below. The provided module `add16` has the following declaration:

`module add16 ( input[15:0] a, input[15:0] b, input cin, output[15:0] sum, output cout );`

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/a3/Module_add.png`）](https://hdlbits.01xz.net/wiki/File:Module_add.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vectorr](../references/markdown/47e5d50fe5de95ad.md "vectorr")
- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8") ·

**module\_add**

- · [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")

[module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")Previous

Next[module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
```

<a id="hdl-026"></a>

### HDL-026 Adder 2

来源：本地原文（原完整交付引用：`<../references/markdown/cc8203024edee10a.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_fadd)

**实现要求**（保留原题的代码、列表及子问）：

[module\_add](../references/markdown/03cf4a90addf2490.md "module_add")Previous

Next[module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")

In this exercise, you will create a circuit with two levels of hierarchy. Your `top_module` will instantiate two copies of `add16` (provided), each of which will instantiate 16 copies of `add1` (which you must write). Thus, you must write *two* modules: `top_module` and `add1`.

Like [module\_add](../references/markdown/03cf4a90addf2490.md "module_add"), you are given a module `add16` that performs a 16-bit addition. You must instantiate two of them to create a 32-bit adder. One `add16` module computes the lower 16 bits of the addition result, while the second `add16` module computes the upper 16 bits of the result. Your 32-bit adder does not need to handle carry-in (assume 0) or carry-out (ignored).

Connect the `add16` modules together as shown in the diagram below. The provided module `add16` has the following declaration:

`module add16 ( input[15:0] a, input[15:0] b, input cin, output[15:0] sum, output cout );`

Within each `add16`, 16 full adders (module `add1`, not provided) are instantiated to actually perform the addition. You must write the full adder module that has the following declaration:

`module add1 ( input a, input b, input cin, output sum, output cout );`

Recall that a full adder computes the sum and carry-out of a+b+cin.

In summary, there are three modules in this design:

- `top_module` — Your top-level module that contains two of...
- `add16`, provided — A 16-bit adder module that is composed of 16 of...
- `add1` — A 1-bit full adder module.

If your submission is missing a `module add1`, you will get an error message that says `Error (12006): Node instance "user_fadd[0].a1" instantiates undefined entity "add1"`.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/f/f3/Module_fadd.png`）](https://hdlbits.01xz.net/wiki/File:Module_fadd.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector4](../references/markdown/b63c1f13c650b833.md "vector4")
- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add") ·

**module\_fadd**

- · [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")

[module\_add](../references/markdown/03cf4a90addf2490.md "module_add")Previous

Next[module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
```

<a id="hdl-027"></a>

### HDL-027 Carry-select adder

来源：本地原文（原完整交付引用：`<../references/markdown/26a17e9830baba03.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_cseladd)

**实现要求**（保留原题的代码、列表及子问）：

[module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")Previous

Next[module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")

One drawback of the ripple carry adder (See [previous exercise](../references/markdown/03cf4a90addf2490.md "module_add")) is that the delay for an adder to compute the carry out (from the carry-in, in the worst case) is fairly slow, and the second-stage adder cannot begin computing *its* carry-out until the first-stage adder has finished. This makes the adder slow. One improvement is a carry-select adder, shown below. The first-stage adder is the same as before, but we duplicate the second-stage adder, one assuming carry-in=0 and one assuming carry-in=1, then using a fast 2-to-1 multiplexer to select which result happened to be correct.

In this exercise, you are provided with the same module `add16` as the previous exercise, which adds two 16-bit numbers with carry-in and produces a carry-out and 16-bit sum. You must instantiate *three* of these to build the carry-select adder, using your own 16-bit 2-to-1 multiplexer.

Connect the modules together as shown in the diagram below. The provided module `add16` has the following declaration:

`module add16 ( input[15:0] a, input[15:0] b, input cin, output[15:0] sum, output cout );`

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/3/3e/Module_cseladd.png`）](https://hdlbits.01xz.net/wiki/File:Module_cseladd.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [vector5](../references/markdown/0572c6851848d75b.md "vector5")
- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd") ·

**module\_cseladd**

- · [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")

[module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")Previous

Next[module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
```

<a id="hdl-028"></a>

### HDL-028 Adder-subtractor

来源：本地原文（原完整交付引用：`<../references/markdown/17902a3f46f08ef7.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/module_addsub)

**实现要求**（保留原题的代码、列表及子问）：

[module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")Previous

Next[alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")

An adder-subtractor can be built from an adder by optionally negating one of the inputs, which is equivalent to inverting the input then adding 1. The net result is a circuit that can do two operations: (a + b + 0) and (a + ~b + 1). See [Wikipedia](https://en.wikipedia.org/wiki/Adder%E2%80%93subtractor) if you want a more detailed explanation of how this circuit works.

Build the adder-subtractor below.

You are provided with a 16-bit adder module, which you need to instantiate twice:

`module add16 ( input[15:0] a, input[15:0] b, input cin, output[15:0] sum, output cout );`

Use a 32-bit wide XOR gate to invert the b input whenever sub is 1. (This can also be viewed as b[31:0] XORed with sub replicated 32 times. See [replication operator](../references/markdown/b63c1f13c650b833.md "vector4").). Also connect the sub input to the carry-in of the adder.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/ae/Module_addsub.png`）](https://hdlbits.01xz.net/wiki/File:Module_addsub.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

###### Changes

- 2020-02-15: Output signal name changed from result to sum.

- [module](../references/markdown/1d9959f03f3c36ed.md "module")
- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd") ·

**module\_addsub**

- · [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")

[module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")Previous

Next[alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module(
    input [31:0] a,
    input [31:0] b,
    input sub,
    output [31:0] sum
);
```

<a id="hdl-029"></a>

### HDL-029 Always blocks (combinational)

来源：本地原文（原完整交付引用：`<../references/markdown/1f71f00a1e4e8f64.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/alwaysblock1)

**实现要求**（保留原题的代码、列表及子问）：

[module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")Previous

Next[alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")

Since digital circuits are composed of logic gates connected with wires, any circuit can be expressed as some combination of modules and assign statements. However, sometimes this is not the most convenient way to describe the circuit. *Procedures* (of which always blocks are one example) provide an alternative syntax for describing circuits.

For synthesizing hardware, two types of always blocks are relevant:

- Combinational: always @(\*)
- Clocked: always @(posedge clk)

Combinational always blocks are equivalent to assign statements, thus there is always a way to express a combinational circuit both ways. The choice between which to use is mainly an issue of which syntax is more convenient. **The syntax for code inside a procedural block is different from code that is outside.** Procedural blocks have a richer set of statements (e.g., if-then, case), cannot contain continuous assignments\*, but also introduces many new non-intuitive ways of making errors.
(\**Procedural continuous assignments* do exist, but are somewhat different from *continuous assignments*, and are not synthesizable.)

For example, the assign and combinational always block describe the same circuit. Both create the same blob of combinational logic. Both will recompute the output whenever any of the inputs (right side) changes value.
`assign out1 = a & b | c ^ d;
always @(*) out2 = a & b | c ^ d;`

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/2/2b/Alwayscomb.png`）](https://hdlbits.01xz.net/wiki/File:Alwayscomb.png)

For combinational always blocks, always use a sensitivity list of (\*). Explicitly listing out the signals is error-prone (if you miss one), and is ignored for hardware synthesis. If you explicitly specify the sensitivity list and miss a signal, the synthesized hardware will still behave as though (\*) was specified, but the simulation will not and not match the hardware's behaviour. (In SystemVerilog, use always\_comb.)

A note on wire vs. reg: The left-hand-side of an assign statement must be a *net* type (e.g., wire), while the left-hand-side of a procedural assignment (in an always block) must be a *variable* type (e.g., reg). These types (wire vs. reg) have nothing to do with what hardware is synthesized, and is just syntax left over from Verilog's use as a hardware *simulation* language.

### A bit of practice

Build an AND gate using both an assign statement and a combinational always block. (Since assign statements and combinational always blocks function identically, there is no way to enforce that you're using both methods. But you're here for practice, right?...)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_pos](../references/markdown/8633d439430db812.md "module_pos")
- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub") ·

**alwaysblock1**

- · [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")

[module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")Previous

Next[alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module(
    input a, 
    input b,
    output wire out_assign,
    output reg out_alwaysblock
);
```

<a id="hdl-030"></a>

### HDL-030 Always blocks (clocked)

来源：本地原文（原完整交付引用：`<../references/markdown/0321f1ea7d56a6dd.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/alwaysblock2)

**实现要求**（保留原题的代码、列表及子问）：

[alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")Previous

Next[always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")

For hardware synthesis, there are two types of always blocks that are relevant:

- Combinational: always @(\*)
- Clocked: always @(posedge clk)

Clocked always blocks create a blob of combinational logic just like combinational always blocks, but also creates a set of flip-flops (or "registers") at the output of the blob of combinational logic. Instead of the outputs of the blob of logic being visible immediately, the outputs are visible only immediately after the next (posedge clk).

#### Blocking vs. Non-Blocking Assignment

There are three types of assignments in Verilog:

- **Continuous** assignments (assign x = y;). Can only be used when **not** inside a procedure ("always block").
- Procedural **blocking** assignment: (x = y;). Can only be used inside a procedure.
- Procedural **non-blocking** assignment: (x <= y;). Can only be used inside a procedure.

In a **combinational** always block, use **blocking** assignments. In a **clocked** always block, use **non-blocking** assignments. A full understanding of why is not particularly useful for hardware design and requires a good understanding of how Verilog simulators keep track of events. Not following this rule results in extremely hard to find errors that are both non-deterministic and differ between simulation and synthesized hardware.

### A bit of practice

Build an XOR gate three ways, using an assign statement, a combinational always block, and a clocked always block. Note that the clocked always block produces a different circuit from the other two: There is a flip-flop so the output is delayed.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/4/40/Alwaysff.png`）](https://hdlbits.01xz.net/wiki/File:Alwaysff.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_name](../references/markdown/5f282069004a8b30.md "module_name")
- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1") ·

**alwaysblock2**

- · [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")

[alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")Previous

Next[always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module(
    input clk,
    input a,
    input b,
    output wire out_assign,
    output reg out_always_comb,
    output reg out_always_ff   );
```

<a id="hdl-031"></a>

### HDL-031 If statement

来源：本地原文（原完整交付引用：`<../references/markdown/4a9997fef0c7d00e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_if)

**实现要求**（保留原题的代码、列表及子问）：

[alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")Previous

Next[always\_if2](../references/markdown/1aab92864d920945.md "always_if2")

An if statement usually creates a 2-to-1 multiplexer, selecting one input if the condition is true, and the other input if the condition is false.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/9/9d/Always_if_mux.png`）](https://hdlbits.01xz.net/wiki/File:Always_if_mux.png)





```
always @(*) begin
    if (condition) begin
        out = x;
    end
    else begin
        out = y;
    end
end
```



This is equivalent to using a continuous assignment with a conditional operator:



```
assign out = (condition) ? x : y;
```



However, the procedural if statement provides a new way to make mistakes. The circuit is combinational only if out is always assigned a value.

### A bit of practice

Build a 2-to-1 mux that chooses between a and b. Choose b if *both* sel\_b1 and sel\_b2 are true. Otherwise, choose a. Do the same twice, once using assign statements and once using a procedural if statement.

| sel\_b1 | sel\_b2 | out\_assign out\_always |
| --- | --- | --- |
| 0 | 0 | a |
| 0 | 1 | a |
| 1 | 0 | a |
| 1 | 1 | b |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_shift](../references/markdown/a36ec3244f2d819b.md "module_shift")
- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2") ·

**always\_if**

- · [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")

[alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")Previous

Next[always\_if2](../references/markdown/1aab92864d920945.md "always_if2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module(
    input a,
    input b,
    input sel_b1,
    input sel_b2,
    output wire out_assign,
    output reg out_always   );
```

<a id="hdl-032"></a>

### HDL-032 If statement latches

来源：本地原文（原完整交付引用：`<../references/markdown/1aab92864d920945.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_if2)

**实现要求**（保留原题的代码、列表及子问）：

[always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")Previous

Next[always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")

### A common source of errors: How to avoid making latches

When designing circuits, you *must* think first in terms of circuits:

- I want this logic gate
- I want a *combinational* blob of logic that has these inputs and produces these outputs
- I want a combinational blob of logic followed by a set of flip-flops

What you *must not* do is write the code first, then hope it generates a proper circuit.

- If (cpu\_overheated) then shut\_off\_computer = 1;
- If (~arrived) then keep\_driving = ~gas\_tank\_empty;

Syntactically-correct code does not necessarily result in a reasonable circuit (combinational logic + flip-flops). The usual reason is: "What happens in the cases other than those you specified?". Verilog's answer is: Keep the outputs unchanged.

This behaviour of "keep outputs unchanged" means the current state needs to be *remembered*, and thus produces a *latch*. Combinational logic (e.g., logic gates) cannot remember any state. Watch out for Warning (10240): ... inferring latch(es)" messages. Unless the latch was intentional, it almost always indicates a bug. Combinational circuits must have a value assigned to all outputs under all conditions. This usually means you always need else clauses or a default value assigned to the outputs.

### Demonstration

The following code contains incorrect behaviour that creates a latch. Fix the bugs so that you will shut off the computer only if it's really overheated, and stop driving if you've arrived at your destination or you need to refuel.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/d/d1/Always_if2.png`）](https://hdlbits.01xz.net/wiki/File:Always_if2.png)

This is the circuit described by the code, not the circuit you want to build.



```
always @(*) begin
    if (cpu_overheated)
       shut_off_computer = 1;
end

always @(*) begin
    if (~arrived)
       keep_driving = ~gas_tank_empty;
end
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_shift8](../references/markdown/80a884be905ec48e.md "module_shift8")
- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if") ·

**always\_if2**

- · [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")

[always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")Previous

Next[always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module (
    input      cpu_overheated,
    output reg shut_off_computer,
    input      arrived,
    input      gas_tank_empty,
    output reg keep_driving  );
```

<a id="hdl-033"></a>

### HDL-033 Case statement

来源：本地原文（原完整交付引用：`<../references/markdown/fdcfe9670d5929aa.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_case)

**实现要求**（保留原题的代码、列表及子问）：

[always\_if2](../references/markdown/1aab92864d920945.md "always_if2")Previous

Next[always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")

Case statements in Verilog are nearly equivalent to a sequence of if-elseif-else that compares one expression to a list of others. Its syntax and functionality differs from the switch statement in C.



```
always @(*) begin     // This is a combinational circuit
    case (in)
      1'b1: begin 
               out = 1'b1;  // begin-end if >1 statement
            end
      1'b0: out = 1'b0;
      default: out = 1'bx;
    endcase
end
```



- The case statement begins with case and each "case item" ends with a colon. There is no "switch".
- Each case item can execute *exactly one* statement. This makes the "break" used in C unnecessary. But this means that if you need more than one statement, you must use begin ... end.
- Duplicate (and partially overlapping) case items are permitted. The first one that matches is used. C does not allow duplicate case items.

### A bit of practice

Case statements are more convenient than if statements if there are a large number of cases. So, in this exercise, create a 6-to-1 multiplexer. When sel is between 0 and 5, choose the corresponding data input. Otherwise, output 0. The data inputs and outputs are all 4 bits wide.

Be careful of inferring latches (See.[always\_if2](../references/markdown/1aab92864d920945.md "always_if2"))

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_add](../references/markdown/03cf4a90addf2490.md "module_add")
- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2") ·

**always\_case**

- · [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")

[always\_if2](../references/markdown/1aab92864d920945.md "always_if2")Previous

Next[always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module ( 
    input [2:0] sel, 
    input [3:0] data0,
    input [3:0] data1,
    input [3:0] data2,
    input [3:0] data3,
    input [3:0] data4,
    input [3:0] data5,
    output reg [3:0] out   );
```

<a id="hdl-034"></a>

### HDL-034 Priority encoder

来源：本地原文（原完整交付引用：`<../references/markdown/cf018e4cc32b8f83.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_case2)

**实现要求**（保留原题的代码、列表及子问）：

[always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")Previous

Next[always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")

A *priority encoder* is a combinational circuit that, when given an input bit vector, outputs the position of the first 1 bit in the vector. For example, a 8-bit priority encoder given the input 8'b10010000 would output 3'd4, because bit[4] is first bit that is high.

Build a 4-bit priority encoder. For this problem, if none of the input bits are high (i.e., input is zero), output zero. Note that a 4-bit number has 16 possible combinations.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_fadd](../references/markdown/cc8203024edee10a.md "module_fadd")
- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case") ·

**always\_case2**

- · [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")

[always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")Previous

Next[always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module (
    input [3:0] in,
    output reg [1:0] pos  );
```

<a id="hdl-035"></a>

### HDL-035 Priority encoder with casez

来源：本地原文（原完整交付引用：`<../references/markdown/547736a87fac50b3.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_casez)

**实现要求**（保留原题的代码、列表及子问）：

[always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")Previous

Next[always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")

Build a priority encoder for 8-bit inputs. Given an 8-bit vector, the output should report the first (least significant) bit in the vector that is 1. Report zero if the input vector has no bits that are high. For example, the input 8'b10010000 should output 3'd4, because bit[4] is first bit that is high.

From the previous exercise ([always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")), there would be 256 cases in the case statement. We can reduce this (down to 9 cases) if the case items in the case statement supported don't-care bits. This is what case**z** is for: It treats bits that have the value z as don't-care in the comparison.

For example, this would implement the 4-input priority encoder from the previous exercise:



```
always @(*) begin
    casez (in[3:0])
        4'bzzz1: out = 0;   // in[3:1] can be anything
        4'bzz1z: out = 1;
        4'bz1zz: out = 2;
        4'b1zzz: out = 3;
        default: out = 0;
    endcase
end
```



A case statement behaves as though each item is checked sequentially (in reality, a big combinational logic function). Notice how there are certain inputs (e.g., 4'b1111) that will match more than one case item. The first match is chosen (so 4'b1111 matches the first item, out = 0, but not any of the later ones).

- There is also a similar casex that treats both x and z as don't-care. I don't see much purpose to using it over casez.
- The digit ? is a synonym for z. so 2'bz0 is the same as 2'b?0

It may be less error-prone to explicitly specify the priority behaviour rather than rely on the ordering of the case items. For example, the following will still behave the same way if some of the case items were reordered, because any bit pattern can only match at most one case item:



```
    casez (in[3:0])
        4'bzzz1: ...
        4'bzz10: ...
        4'bz100: ...
        4'b1000: ...
        default: ...
    endcase
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_cseladd](../references/markdown/26a17e9830baba03.md "module_cseladd")
- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2") ·

**always\_casez**

- · [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")

[always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")Previous

Next[always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
always @(*) begin
    casez (in[3:0])
        4'bzzz1: out = 0;   // in[3:1] can be anything
        4'bzz1z: out = 1;
        4'bz1zz: out = 2;
        4'b1zzz: out = 3;
        default: out = 0;
    endcase
end
```

<a id="hdl-036"></a>

### HDL-036 Avoiding latches

来源：本地原文（原完整交付引用：`<../references/markdown/e769c858da53c60b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/always_nolatches)

**实现要求**（保留原题的代码、列表及子问）：

[always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")Previous

Next[conditional](../references/markdown/5345d19ef64578d9.md "conditional")

Suppose you're building a circuit to process scancodes from a PS/2 keyboard for a game. Given the last two bytes of scancodes received, you need to indicate whether one of the arrow keys on the keyboard have been pressed. This involves a fairly simple mapping, which can be implemented as a case statement (or if-elseif) with four cases.

| Scancode [15:0] | Arrow key |
| --- | --- |
| 16'he06b | left arrow |
| 16'he072 | down arrow |
| 16'he074 | right arrow |
| 16'he075 | up arrow |
| Anything else | none |

Your circuit has one 16-bit input, and four outputs. Build this circuit that recognizes these four scancodes and asserts the correct output.

To avoid creating latches, all outputs must be assigned a value in all possible conditions (See also [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")). Simply having a default case is not enough. You must assign a value to all four outputs in all four cases and the default case. This can involve a lot of unnecessary typing. One easy way around this is to assign a "default value" to the outputs *before* the case statement:



```
always @(*) begin
    up = 1'b0; down = 1'b0; left = 1'b0; right = 1'b0;
    case (scancode)
        ... // Set to 1 as necessary.
    endcase
end
```



This style of code ensures the outputs are assigned a value (of 0) in all possible cases unless the case statement overrides the assignment. This also means that a default: case item becomes unnecessary.

**Reminder:** The logic synthesizer generates a combinational circuit that *behaves* equivalently to what the code describes. Hardware does not "execute" the lines of code in sequence.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [module\_addsub](../references/markdown/17902a3f46f08ef7.md "module_addsub")
- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez") ·

**always\_nolatches**

- · [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")

[always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")Previous

Next[conditional](../references/markdown/5345d19ef64578d9.md "conditional")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
// synthesis verilog_input_version verilog_2001
module top_module (
    input [15:0] scancode,
    output reg left,
    output reg down,
    output reg right,
    output reg up  );
```

<a id="hdl-037"></a>

### HDL-037 Conditional ternary operator

来源：本地原文（原完整交付引用：`<../references/markdown/5345d19ef64578d9.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/conditional)

**实现要求**（保留原题的代码、列表及子问）：

[always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")Previous

Next[reduction](../references/markdown/9c307f46759789f6.md "reduction")

Verilog has a ternary conditional operator ( ? : ) much like C:

(condition ? if\_true : if\_false)

This can be used to choose one of two values based on *condition* (a mux!) on one line, without using an if-then inside a combinational always block.

Examples:



```
(0 ? 3 : 5)     // This is 5 because the condition is false.
(sel ? b : a)   // A 2-to-1 multiplexer between a and b selected by sel.

always @(posedge clk)         // A T-flip-flop.
  q <= toggle ? ~q : q;

always @(*)                   // State transition logic for a one-input FSM
  case (state)
    A: next = w ? B : A;
    B: next = w ? A : B;
  endcase

assign out = ena ? q : 1'bz;  // A tri-state buffer

((sel[1:0] == 2'h0) ? a :     // A 3-to-1 mux
 (sel[1:0] == 2'h1) ? b :
                      c )
```



## A Bit of Practice

Given four unsigned numbers, find the minimum. Unsigned numbers can be compared with standard comparison operators (a < b). Use the conditional operator to make two-way *min* circuits, then compose a few of them to create a 4-way *min* circuit. You'll probably want some wire vectors for the intermediate results.

***Expected solution length:** Around 5 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [alwaysblock1](../references/markdown/1f71f00a1e4e8f64.md "alwaysblock1")
- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches") ·

**conditional**

- · [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")

[always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")Previous

Next[reduction](../references/markdown/9c307f46759789f6.md "reduction")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input [7:0] a, b, c, d,
    output [7:0] min);
```

<a id="hdl-038"></a>

### HDL-038 Reduction operators

来源：本地原文（原完整交付引用：`<../references/markdown/9c307f46759789f6.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/reduction)

**实现要求**（保留原题的代码、列表及子问）：

[conditional](../references/markdown/5345d19ef64578d9.md "conditional")Previous

Next[gates100](../references/markdown/a28750136ece336b.md "gates100")

You're already familiar with bitwise operations between two values, e.g., a & b or a ^ b. Sometimes, you want to create a wide gate that operates on all of the bits of *one* vector, like (a[0] & a[1] & a[2] & a[3] ... ), which gets tedious if the vector is long.

The *reduction* operators can do AND, OR, and XOR of the bits of a vector, producing one bit of output:



```
& a[3:0]     // AND: a[3]&a[2]&a[1]&a[0]. Equivalent to (a[3:0] == 4'hf)
| b[3:0]     // OR:  b[3]|b[2]|b[1]|b[0]. Equivalent to (b[3:0] != 4'h0)
^ c[2:0]     // XOR: c[2]^c[1]^c[0]
```



These are *unary* operators that have only one operand (similar to the NOT operators ! and ~). You can also invert the outputs of these to create NAND, NOR, and XNOR gates, e.g., (~& d[7:0]).

Now you can revisit [4-input gates](../references/markdown/025ff45ba530f489.md "gates4") and [100-input gates](../references/markdown/a28750136ece336b.md "gates100").

## A Bit of Practice

Parity checking is often used as a simple method of detecting errors when transmitting data through an imperfect channel. Create a circuit that will compute a parity bit for a 8-bit byte (which will add a 9th bit to the byte). We will use "even" parity, where the parity bit is just the XOR of all 8 data bits.

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")
- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional") ·

**reduction**

- · [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")

[conditional](../references/markdown/5345d19ef64578d9.md "conditional")Previous

Next[gates100](../references/markdown/a28750136ece336b.md "gates100")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module (
    input [7:0] in,
    output parity);
```

<a id="hdl-039"></a>

### HDL-039 Reduction: Even wider gates

来源：本地原文（原完整交付引用：`<../references/markdown/a28750136ece336b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/gates100)

**实现要求**（保留原题的代码、列表及子问）：

[reduction](../references/markdown/9c307f46759789f6.md "reduction")Previous

Next[vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")

Build a combinational circuit with 100 inputs, in[99:0].

There are 3 outputs:

- out\_and: output of a 100-input AND gate.
- out\_or: output of a 100-input OR gate.
- out\_xor: output of a 100-input XOR gate.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [always\_if](../references/markdown/4a9997fef0c7d00e.md "always_if")
- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction") ·

**gates100**

- · [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")

[reduction](../references/markdown/9c307f46759789f6.md "reduction")Previous

Next[vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [99:0] in,
    output out_and,
    output out_or,
    output out_xor 
);
```

<a id="hdl-040"></a>

### HDL-040 Combinational for-loop: Vector reversal 2

来源：本地原文（原完整交付引用：`<../references/markdown/a5b4a1941aa2e15e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/vector100r)

**实现要求**（保留原题的代码、列表及子问）：

[gates100](../references/markdown/a28750136ece336b.md "gates100")Previous

Next[popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")

Given a 100-bit input vector [99:0], reverse its bit ordering.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [always\_if2](../references/markdown/1aab92864d920945.md "always_if2")
- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100") ·

**vector100r**

- · [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")

[gates100](../references/markdown/a28750136ece336b.md "gates100")Previous

Next[popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [99:0] in,
    output [99:0] out
);
```

<a id="hdl-041"></a>

### HDL-041 Combinational for-loop: 255-bit population count

来源：本地原文（原完整交付引用：`<../references/markdown/cf6a892d0c3d0578.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/popcount255)

**实现要求**（保留原题的代码、列表及子问）：

[vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")Previous

Next[adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")

A "population count" circuit counts the number of '1's in an input vector. Build a population count circuit for a 255-bit input vector.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [always\_case](../references/markdown/fdcfe9670d5929aa.md "always_case")
- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r") ·

**popcount255**

- · [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")

[vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")Previous

Next[adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [254:0] in,
    output [7:0] out );
```

<a id="hdl-042"></a>

### HDL-042 Generate for-loop: 100-bit binary adder 2

来源：本地原文（原完整交付引用：`<../references/markdown/a1fc1c4803f510da.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/adder100i)

**实现要求**（保留原题的代码、列表及子问）：

[popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")Previous

Next[bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")

Create a 100-bit binary ripple-carry adder by instantiating 100 [full adders](https://hdlbits.01xz.net/wiki/Fadd "Fadd"). (You also need to write the full adder module, possibly by reusing your solution to [fadd](../references/markdown/7996800470bc1562.md "fadd").)

The adder adds two 100-bit numbers and a carry-in to produce a 100-bit sum and carry out. To encourage you to actually instantiate full adders, also output the carry-out from *each* full adder in the ripple-carry adder. cout[99] is the final carry-out from the last full adder, and is the carry-out you usually see.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [always\_case2](../references/markdown/cf018e4cc32b8f83.md "always_case2")
- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255") ·

**adder100i**

- · [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420")

[popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")Previous

Next[bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [99:0] a, b,
    input cin,
    output [99:0] cout,
    output [99:0] sum );
```

<a id="hdl-043"></a>

### HDL-043 Generate for-loop: 100-digit BCD adder

来源：本地原文（原完整交付引用：`<../references/markdown/4d96080bd12c225d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/bcdadd100)

**实现要求**（保留原题的代码、列表及子问）：

[adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")Previous

Next[exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")

You are provided with a BCD one-digit adder named bcd\_fadd that adds two BCD digits and carry-in, and produces a sum and carry-out.



```
module bcd_fadd (
    input [3:0] a,
    input [3:0] b,
    input     cin,
    output   cout,
    output [3:0] sum );
```



Instantiate 100 copies of bcd\_fadd to create a 100-digit BCD ripple-carry adder. Your adder should add two 100-digit BCD numbers (packed into 400-bit vectors) and a carry-in to produce a 100-digit sum and carry out.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [always\_casez](../references/markdown/547736a87fac50b3.md "always_casez")
- [always\_nolatches](../references/markdown/e769c858da53c60b.md "always_nolatches")
- [conditional](../references/markdown/5345d19ef64578d9.md "conditional")
- [reduction](../references/markdown/9c307f46759789f6.md "reduction")
- [gates100](../references/markdown/a28750136ece336b.md "gates100")
- [vector100r](../references/markdown/a5b4a1941aa2e15e.md "vector100r")
- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i") ·

**bcdadd100**

- · [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")

[adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")Previous

Next[exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：原文建议的语法基础题。

接口原样保留：

```verilog
module top_module( 
    input [399:0] a, b,
    input cin,
    output cout,
    output [399:0] sum );
```

<a id="hdl-049"></a>

### HDL-049 More logic gates

来源：本地原文（原完整交付引用：`<../references/markdown/fe2b28ccd51ba018.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/gates)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")Previous

Next[7420](../references/markdown/99ab7ded006d728b.md "7420")

Ok, let's try building several logic gates at the same time. Build a combinational circuit with two inputs, a and b.

There are 7 outputs, each with a logic gate driving it:

- out\_and: a and b
- out\_or: a or b
- out\_xor: a xor b
- out\_nand: a nand b
- out\_nor: a nor b
- out\_xnor: a xnor b
- out\_anotb: a and-not b

***Expected solution length:** Around 7 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [popcount255](../references/markdown/cf6a892d0c3d0578.md "popcount255")
- [adder100i](../references/markdown/a1fc1c4803f510da.md "adder100i")
- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g") ·

**gates**

- · [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")
- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")

[exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")Previous

Next[7420](../references/markdown/99ab7ded006d728b.md "7420")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input a, b,
    output out_and,
    output out_or,
    output out_xor,
    output out_nand,
    output out_nor,
    output out_xnor,
    output out_anotb
);
```

<a id="hdl-051"></a>

### HDL-051 Truth tables

来源：本地原文（原完整交付引用：`<../references/markdown/40048da3295749c9.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/truthtable1)

**实现要求**（保留原题的代码、列表及子问）：

[7420](../references/markdown/99ab7ded006d728b.md "7420")Previous

Next[mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")

In the previous exercises, we used simple logic gates and combinations of several logic gates. These circuits are examples of *combinational* circuits. Combinational means the outputs of the circuit is a function (in the mathematics sense) of only its inputs. This means that for any given input value, there is only one possible output value. Thus, one way to describe the behaviour of a combinational function is to explicitly list what the output should be for every possible value of the inputs. This is a truth table.

For a boolean function of N inputs, there are 2N possible input combinations. Each row of the truth table lists one input combination, so there are always 2N rows. The output column shows what the output should be for each input value.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Row | *Inputs* | | | *Outputs* |
| number | x3 | x2 | x1 | f |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 |
| 2 | 0 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 | 1 |
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 0 | 1 | 1 |
| 6 | 1 | 1 | 0 | 0 |
| 7 | 1 | 1 | 1 | 1 |

The above truth table is for a three-input, one-output function. It has 8 rows for each of the 8 possible input combinations, and one output column. There are four inputs combinations where the output is 1, and four where the output is 0.

### Synthesizing a circuit from a truth table

Suppose we want to build the above circuit, but we're limited to using only the set of standard logic gates.
How would you build arbitrary logic functions (expressed as a truth table)?

One simple method to create a circuit that implements the truth table's function is to express the function in sum-of-products form. **Sum** (meaning OR) of **products** (meaning AND) means using one *N*-input AND gate per row of the truth table (to detect when the input matches each row), followed by an OR gate that chooses only those rows that result in a '1' output.

For the above example, the output is '1' if the input matches row 2 **or** row 3 **or** row 5 **or** row 7 (This is a 4-input OR gate). The input matches row 2 if x3=0 **and** x2=1 **and** x1=0 (This is a 3-input AND gate). Thus, this truth table can be implemented in canonical form by using 4 AND gates that are ORed together.

## A Bit of Practice

Create a combinational circuit that implements the above truth table.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/f/f6/Truthtable1.png`）](https://hdlbits.01xz.net/wiki/File:Truthtable1.png)

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [bcdadd100](../references/markdown/4d96080bd12c225d.md "bcdadd100")
- [exams/m2014\_q4h](../references/markdown/179059ad0a3cf363.md "exams/m2014_q4h")
- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420") ·

**truthtable1**

- · [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")

[7420](../references/markdown/99ab7ded006d728b.md "7420")Previous

Next[mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input x3,
    input x2,
    input x1,  // three inputs
    output f   // one output
);
```

<a id="hdl-053"></a>

### HDL-053 Simple circuit A

来源：本地原文（原完整交付引用：`<../references/markdown/b8d588a26bf186a7.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mt2015_q4a)

**实现要求**（保留原题的代码、列表及子问）：

[mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")Previous

Next[mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")

Taken from 2015 midterm question 4

Module A is supposed to implement the function z = (x^y) & x. Implement this module.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4i](../references/markdown/45c8c3ef49365994.md "exams/m2014_q4i")
- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")
- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2") ·

**mt2015\_q4a**

- · [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")

[mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")Previous

Next[mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (input x, input y, output z);
```

<a id="hdl-054"></a>

### HDL-054 Simple circuit B

来源：本地原文（原完整交付引用：`<../references/markdown/5dbcf7b7dbed8b0e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mt2015_q4b)

**实现要求**（保留原题的代码、列表及子问）：

[mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")Previous

Next[mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")

Taken from 2015 midterm question 4

Circuit B can be described by the following simulation waveform:
![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.1574b9d23d7fff1b.1574b9d23d7fff1b.png`）](https://hdlbits.01xz.net/wiki/File:Mt2015_q4b.png)

Implement this circuit.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4e](../references/markdown/96071379ebbf6282.md "exams/m2014_q4e")
- [exams/m2014\_q4f](../references/markdown/5cfd93a6e8d38ba3.md "exams/m2014_q4f")
- [exams/m2014\_q4g](../references/markdown/33476ea48de1b2ed.md "exams/m2014_q4g")
- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")
- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a") ·

**mt2015\_q4b**

- · [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")

[mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")Previous

Next[mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module ( input x, input y, output z );
```

<a id="hdl-057"></a>

### HDL-057 Thermostat

来源：本地原文（原完整交付引用：`<../references/markdown/0c512b90d5c509ed.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/thermostat)

**实现要求**（保留原题的代码、列表及子问）：

[ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")Previous

Next[popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")

A heating/cooling thermostat controls both a heater (during winter) and an air conditioner (during summer). Implement a circuit that will turn on and off the heater, air conditioning, and blower fan as appropriate.

The thermostat can be in one of two modes: heating (`mode = 1`) and cooling (`mode = 0`).
In heating mode, turn the heater on when it is too cold (`too_cold = 1`) but do not use the air conditioner. In cooling mode, turn the air conditioner on when it is too hot (`too_hot = 1`), but do not turn on the heater. When the heater or air conditioner are on, also turn on the fan to circulate the air. In addition, the user can also request the fan to turn on (`fan_on = 1`), even if the heater and air conditioner are off.

Try to use only `assign` statements, to see whether you can translate a problem description into a collection of logic gates.

***Expected solution length:** Around 3 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [gates](../references/markdown/fe2b28ccd51ba018.md "gates")
- [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")
- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer") ·

**thermostat**

- · [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")

[ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")Previous

Next[popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input too_cold,
    input too_hot,
    input mode,
    input fan_on,
    output heater,
    output aircon,
    output fan
);
```

<a id="hdl-058"></a>

### HDL-058 3-bit population count

来源：本地原文（原完整交付引用：`<../references/markdown/f5cd4b0acb291896.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/popcount3)

**实现要求**（保留原题的代码、列表及子问）：

[thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")Previous

Next[gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")

A "population count" circuit counts the number of '1's in an input vector. Build a population count circuit for a 3-bit input vector.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [7420](../references/markdown/99ab7ded006d728b.md "7420")
- [truthtable1](../references/markdown/40048da3295749c9.md "truthtable1")
- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat") ·

**popcount3**

- · [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")

[thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")Previous

Next[gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input [2:0] in,
    output [1:0] out );
```

<a id="hdl-060"></a>

### HDL-060 Even longer vectors

来源：本地原文（原完整交付引用：`<../references/markdown/c82faaf923f64256.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/gatesv100)

**实现要求**（保留原题的代码、列表及子问）：

[gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")Previous

Next[mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")

See also the shorter version: [Gates and vectors](../references/markdown/872c5371b38cafa2.md "gatesv").

You are given a 100-bit input vector in[99:0]. We want to know some relationships between each bit and its neighbour:

- **out\_both**: Each bit of this output vector should indicate whether *both* the corresponding input bit and its neighbour to the **left** are '1'. For example, out\_both[98] should indicate if in[98] and in[99] are both 1. Since in[99] has no neighbour to the left, the answer is obvious so we don't need to know out\_both[99].
- **out\_any**: Each bit of this output vector should indicate whether *any* of the corresponding input bit and its neighbour to the **right** are '1'. For example, out\_any[2] should indicate if either in[2] or in[1] are 1. Since in[0] has no neighbour to the right, the answer is obvious so we don't need to know out\_any[0].
- **out\_different**: Each bit of this output vector should indicate whether the corresponding input bit is different from its neighbour to the **left**. For example, out\_different[98] should indicate if in[98] is different from in[99]. For this part, treat the vector as wrapping around, so in[99]'s neighbour to the left is in[0].

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mt2015\_eq2](../references/markdown/b81a22044891e1ac.md "mt2015_eq2")
- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv") ·

**gatesv100**

- · [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")

[gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")Previous

Next[mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input [99:0] in,
    output [98:0] out_both,
    output [99:1] out_any,
    output [99:0] out_different );
```

<a id="hdl-061"></a>

### HDL-061 2-to-1 multiplexer

来源：本地原文（原完整交付引用：`<../references/markdown/732621f4f2296189.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mux2to1)

**实现要求**（保留原题的代码、列表及子问）：

[gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")Previous

Next[mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")

Create a one-bit wide, 2-to-1 multiplexer. When sel=0, choose a. When sel=1, choose b.

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mt2015\_q4a](../references/markdown/b8d588a26bf186a7.md "mt2015_q4a")
- [mt2015\_q4b](../references/markdown/5dbcf7b7dbed8b0e.md "mt2015_q4b")
- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100") ·

**mux2to1**

- · [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")
- [exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")

[gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")Previous

Next[mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input a, b, sel,
    output out );
```

<a id="hdl-063"></a>

### HDL-063 9-to-1 multiplexer

来源：本地原文（原完整交付引用：`<../references/markdown/6057ef8dc18aa6f6.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mux9to1v)

**实现要求**（保留原题的代码、列表及子问）：

[mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")Previous

Next[mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")

Create a 16-bit wide, 9-to-1 multiplexer. sel=0 chooses a, sel=1 chooses b, etc.
For the unused cases (sel=9 to 15), set all output bits to '1'.

***Expected solution length:** Around 15 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mt2015\_q4](../references/markdown/93bc6d07f57e2d24.md "mt2015_q4")
- [ringer](../references/markdown/5c6175a4ace8a0ff.md "ringer")
- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v") ·

**mux9to1v**

- · [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")
- [exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")
- [exams/ece241\_2014\_q1c](../references/markdown/b98164a4421e17e5.md "exams/ece241_2014_q1c")
- [adder100](../references/markdown/4f273f0b269bdf0f.md "adder100")

[mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")Previous

Next[mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input [15:0] a, b, c, d, e, f, g, h, i,
    input [3:0] sel,
    output [15:0] out );
```

<a id="hdl-065"></a>

### HDL-065 256-to-1 4-bit multiplexer

来源：本地原文（原完整交付引用：`<../references/markdown/31de27ed95a5dec7.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mux256to1v)

**实现要求**（保留原题的代码、列表及子问）：

[mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")Previous

Next[hadd](../references/markdown/2d2561f66844853a.md "hadd")

Create a 4-bit wide, 256-to-1 multiplexer. The 256 4-bit inputs are all packed into a single 1024-bit input vector. sel=0 should select bits in[3:0], sel=1 selects bits in[7:4], sel=2 selects bits in[11:8], etc.

***Expected solution length:** Around 1–5 lines.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [thermostat](../references/markdown/0c512b90d5c509ed.md "thermostat")
- [popcount3](../references/markdown/f5cd4b0acb291896.md "popcount3")
- [gatesv](../references/markdown/872c5371b38cafa2.md "gatesv")
- [gatesv100](../references/markdown/c82faaf923f64256.md "gatesv100")
- [mux2to1](../references/markdown/732621f4f2296189.md "mux2to1")
- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1") ·

**mux256to1v**

- · [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")
- [exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")
- [exams/ece241\_2014\_q1c](../references/markdown/b98164a4421e17e5.md "exams/ece241_2014_q1c")
- [adder100](../references/markdown/4f273f0b269bdf0f.md "adder100")
- [bcdadd4](../references/markdown/2d3caa0229e8863b.md "bcdadd4")
- [kmap1](../references/markdown/d4f7d25b7700d829.md "kmap1")

[mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")Previous

Next[hadd](../references/markdown/2d2561f66844853a.md "hadd")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input [1023:0] in,
    input [7:0] sel,
    output [3:0] out );
```

<a id="hdl-070"></a>

### HDL-070 Signed addition overflow

来源：本地原文（原完整交付引用：`<../references/markdown/b98164a4421e17e5.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2014_q1c)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")Previous

Next[adder100](../references/markdown/4f273f0b269bdf0f.md "adder100")

Assume that you have two 8-bit 2's complement numbers, a[7:0] and b[7:0]. These numbers are added to produce s[7:0]. Also compute whether a (signed) overflow has occurred.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mux2to1v](../references/markdown/9f8a8d41bbd63168.md "mux2to1v")
- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")
- [exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j") ·

**exams/ece241\_2014\_q1c**

- · [adder100](../references/markdown/4f273f0b269bdf0f.md "adder100")
- [bcdadd4](../references/markdown/2d3caa0229e8863b.md "bcdadd4")
- [kmap1](../references/markdown/d4f7d25b7700d829.md "kmap1")
- [kmap2](../references/markdown/7be615f07e064caf.md "kmap2")
- [kmap3](../references/markdown/2df6cc69f79c70db.md "kmap3")
- [kmap4](../references/markdown/f08c6848376be516.md "kmap4")
- [exams/ece241\_2013\_q2](../references/markdown/6a3cd294414d5a58.md "exams/ece241_2013_q2")
- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")

[exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")Previous

Next[adder100](../references/markdown/4f273f0b269bdf0f.md "adder100")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input [7:0] a,
    input [7:0] b,
    output [7:0] s,
    output overflow
);
```

<a id="hdl-071"></a>

### HDL-071 100-bit binary adder

来源：本地原文（原完整交付引用：`<../references/markdown/4f273f0b269bdf0f.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/adder100)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q1c](../references/markdown/b98164a4421e17e5.md "exams/ece241_2014_q1c")Previous

Next[bcdadd4](../references/markdown/2d3caa0229e8863b.md "bcdadd4")

Create a 100-bit binary adder. The adder adds two 100-bit numbers and a carry-in to produce a 100-bit sum and carry out.

***Expected solution length:** Around 1 line.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mux9to1v](../references/markdown/6057ef8dc18aa6f6.md "mux9to1v")
- [mux256to1](../references/markdown/b1ec0af7861c16a5.md "mux256to1")
- [mux256to1v](../references/markdown/31de27ed95a5dec7.md "mux256to1v")
- [hadd](../references/markdown/2d2561f66844853a.md "hadd")
- [fadd](../references/markdown/7996800470bc1562.md "fadd")
- [adder3](../references/markdown/0067ab5b61a0d972.md "adder3")
- [exams/m2014\_q4j](../references/markdown/9e25fbaed77eb13f.md "exams/m2014_q4j")
- [exams/ece241\_2014\_q1c](../references/markdown/b98164a4421e17e5.md "exams/ece241_2014_q1c") ·

**adder100**

- · [bcdadd4](../references/markdown/2d3caa0229e8863b.md "bcdadd4")
- [kmap1](../references/markdown/d4f7d25b7700d829.md "kmap1")
- [kmap2](../references/markdown/7be615f07e064caf.md "kmap2")
- [kmap3](../references/markdown/2df6cc69f79c70db.md "kmap3")
- [kmap4](../references/markdown/f08c6848376be516.md "kmap4")
- [exams/ece241\_2013\_q2](../references/markdown/6a3cd294414d5a58.md "exams/ece241_2013_q2")
- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")
- [exams/2012\_q1g](../references/markdown/fe9cae1924fd70b3.md "exams/2012_q1g")

[exams/ece241\_2014\_q1c](../references/markdown/b98164a4421e17e5.md "exams/ece241_2014_q1c")Previous

Next[bcdadd4](../references/markdown/2d3caa0229e8863b.md "bcdadd4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module( 
    input [99:0] a, b,
    input cin,
    output cout,
    output [99:0] sum );
```

<a id="hdl-081"></a>

### HDL-081 D flip-flop

来源：本地原文（原完整交付引用：`<../references/markdown/659cf231925109fa.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/dff)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3")Previous

Next[dff8](../references/markdown/da17353c04d5d74c.md "dff8")

A D flip-flop is a circuit that stores a bit and is updated periodically, at the (usually) positive edge of a clock signal.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/6/6c/Dff.png`）](https://hdlbits.01xz.net/wiki/File:Dff.png)

D flip-flops are created by the logic synthesizer when a clocked always block is used (See [alwaysblock2](../references/markdown/0321f1ea7d56a6dd.md "alwaysblock2")). A D flip-flop is the simplest form of "blob of combinational logic followed by a flip-flop" where the combinational logic portion is just a wire.

Create a single D flip-flop.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [kmap1](../references/markdown/d4f7d25b7700d829.md "kmap1")
- [kmap2](../references/markdown/7be615f07e064caf.md "kmap2")
- [kmap3](../references/markdown/2df6cc69f79c70db.md "kmap3")
- [kmap4](../references/markdown/f08c6848376be516.md "kmap4")
- [exams/ece241\_2013\_q2](../references/markdown/6a3cd294414d5a58.md "exams/ece241_2013_q2")
- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")
- [exams/2012\_q1g](../references/markdown/fe9cae1924fd70b3.md "exams/2012_q1g")
- [exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3") ·

**dff**

- · [dff8](../references/markdown/da17353c04d5d74c.md "dff8")
- [dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")
- [dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")
- [dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")
- [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")

[exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3")Previous

Next[dff8](../references/markdown/da17353c04d5d74c.md "dff8")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,    // Clocks are used in sequential circuits
    input d,
    output reg q );
```

<a id="hdl-084"></a>

### HDL-084 DFF with reset value

来源：本地原文（原完整交付引用：`<../references/markdown/9344f0a1f99a2ce2.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/dff8p)

**实现要求**（保留原题的代码、列表及子问）：

[dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")Previous

Next[dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")

Create 8 D flip-flops with active high synchronous reset. The flip-flops must be reset to 0x34 rather than zero. All DFFs should be triggered by the **negative** edge of clk.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [kmap4](../references/markdown/f08c6848376be516.md "kmap4")
- [exams/ece241\_2013\_q2](../references/markdown/6a3cd294414d5a58.md "exams/ece241_2013_q2")
- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")
- [exams/2012\_q1g](../references/markdown/fe9cae1924fd70b3.md "exams/2012_q1g")
- [exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3")
- [dff](../references/markdown/659cf231925109fa.md "dff")
- [dff8](../references/markdown/da17353c04d5d74c.md "dff8")
- [dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r") ·

**dff8p**

- · [dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")
- [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")

[dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")Previous

Next[dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,
    input [7:0] d,
    output [7:0] q
);
```

<a id="hdl-085"></a>

### HDL-085 DFF with asynchronous reset

来源：本地原文（原完整交付引用：`<../references/markdown/5cd0b5614bbb6da8.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/dff8ar)

**实现要求**（保留原题的代码、列表及子问）：

[dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")Previous

Next[dff16e](../references/markdown/2bc75c749404c522.md "dff16e")

Create 8 D flip-flops with active high asynchronous reset. All DFFs should be triggered by the positive edge of clk.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2013\_q2](../references/markdown/6a3cd294414d5a58.md "exams/ece241_2013_q2")
- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")
- [exams/2012\_q1g](../references/markdown/fe9cae1924fd70b3.md "exams/2012_q1g")
- [exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3")
- [dff](../references/markdown/659cf231925109fa.md "dff")
- [dff8](../references/markdown/da17353c04d5d74c.md "dff8")
- [dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")
- [dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p") ·

**dff8ar**

- · [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")

[dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")Previous

Next[dff16e](../references/markdown/2bc75c749404c522.md "dff16e")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input areset,   // active high asynchronous reset
    input [7:0] d,
    output [7:0] q
);
```

<a id="hdl-086"></a>

### HDL-086 DFF with byte enable

来源：本地原文（原完整交付引用：`<../references/markdown/2bc75c749404c522.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/dff16e)

**实现要求**（保留原题的代码、列表及子问）：

[dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")Previous

Next[exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")

Create 16 D flip-flops. It's sometimes useful to only modify parts of a group of flip-flops. The byte-enable inputs control whether each byte of the 16 registers should be written to on that cycle. byteena[1] controls the upper byte d[15:8], while byteena[0] controls the lower byte d[7:0].

resetn is a synchronous, active-low reset.

All DFFs should be triggered by the positive edge of clk.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q3](../references/markdown/3fca32db766b422e.md "exams/m2014_q3")
- [exams/2012\_q1g](../references/markdown/fe9cae1924fd70b3.md "exams/2012_q1g")
- [exams/ece241\_2014\_q3](../references/markdown/7cf3204f2b98126f.md "exams/ece241_2014_q3")
- [dff](../references/markdown/659cf231925109fa.md "dff")
- [dff8](../references/markdown/da17353c04d5d74c.md "dff8")
- [dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")
- [dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")
- [dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar") ·

**dff16e**

- · [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")

[dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")Previous

Next[exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input resetn,
    input [1:0] byteena,
    input [15:0] d,
    output [15:0] q
);
```

<a id="hdl-091"></a>

### HDL-091 Mux and DFF

来源：本地原文（原完整交付引用：`<../references/markdown/918c137acd15c1ee.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/mt2015_muxdff)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")Previous

Next[exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")

Taken from ECE253 2015 midterm question 5

Consider the sequential circuit below:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.eca55e8acfbf4bbf.eca55e8acfbf4bbf.png`）](https://hdlbits.01xz.net/wiki/File:Mt2015_muxdff.png)

Assume that you want to implement hierarchical Verilog code for this circuit, using three instantiations of a submodule that has a flip-flop and multiplexer in it. Write a Verilog module (containing one flip-flop and multiplexer) named top\_module for this submodule.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [dff8r](../references/markdown/fc91940b2f4faf10.md "dff8r")
- [dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")
- [dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")
- [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d") ·

**mt2015\_muxdff**

- · [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")

[exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")Previous

Next[exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 同名题按各自原图分别建 TB，不合并成同一道。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
	input clk,
	input L,
	input r_in,
	input q_in,
	output reg Q);
```

<a id="hdl-092"></a>

### HDL-092 Mux and DFF

来源：本地原文（原完整交付引用：`<../references/markdown/24823d4b6666b37b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2014_q4a)

**实现要求**（保留原题的代码、列表及子问）：

[mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")Previous

Next[exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")

Consider the *n*-bit shift register circuit shown below:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.e674472e9a7d5482.e674472e9a7d5482.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2014q4.png)

Write a Verilog module named top\_module for one stage of this circuit, including both the flip-flop and multiplexers.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [dff8p](../references/markdown/9344f0a1f99a2ce2.md "dff8p")
- [dff8ar](../references/markdown/5cd0b5614bbb6da8.md "dff8ar")
- [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff") ·

**exams/2014\_q4a**

- · [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")

[mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")Previous

Next[exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 同名题按各自原图分别建 TB，不合并成同一道。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input w, R, E, L,
    output Q
);
```

<a id="hdl-094"></a>

### HDL-094 Create circuit from truth table

来源：本地原文（原完整交付引用：`<../references/markdown/ad3d76f5fa691b07.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2013_q7)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")Previous

Next[edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")

A JK flip-flop has the below truth table. Implement a JK flip-flop with only a D-type flip-flop and gates. Note: Qold is the output of the D flip-flop before the positive clock edge.

| J | K | Q |
| --- | --- | --- |
| 0 | 0 | Qold |
| 0 | 1 | 0 |
| 1 | 0 | 1 |
| 1 | 1 | ~Qold |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [dff16e](../references/markdown/2bc75c749404c522.md "dff16e")
- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4") ·

**exams/ece241\_2013\_q7**

- · [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")

[exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")Previous

Next[edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input j,
    input k,
    output Q);
```

<a id="hdl-095"></a>

### HDL-095 Detect an edge

来源：本地原文（原完整交付引用：`<../references/markdown/95cba20f30db53f7.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/edgedetect)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")Previous

Next[edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")

For each bit in an 8-bit vector, detect when the input signal changes from 0 in one clock cycle to 1 the next (similar to positive edge detection). The output bit should be set the cycle after a 0 to 1 transition occurs.

Here are some examples. For clarity, in[1] and pedge[1] are shown separately.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4a](../references/markdown/9466c674480bbc71.md "exams/m2014_q4a")
- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7") ·

**edgedetect**

- · [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")

[exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")Previous

Next[edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input [7:0] in,
    output [7:0] pedge
);
```

<a id="hdl-096"></a>

### HDL-096 Detect both edges

来源：本地原文（原完整交付引用：`<../references/markdown/3074c6099e9a4cde.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/edgedetect2)

**实现要求**（保留原题的代码、列表及子问）：

[edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")Previous

Next[edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")

For each bit in an 8-bit vector, detect when the input signal changes from one clock cycle to the next (detect any edge). The output bit should be set the cycle after a 0 to 1 transition occurs.

Here are some examples. For clarity, in[1] and anyedge[1] are shown separately

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4b](../references/markdown/9a5ace999f7b1724.md "exams/m2014_q4b")
- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect") ·

**edgedetect2**

- · [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")

[edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")Previous

Next[edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input [7:0] in,
    output [7:0] anyedge
);
```

<a id="hdl-097"></a>

### HDL-097 Edge capture register

来源：本地原文（原完整交付引用：`<../references/markdown/a901d2224de8d362.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/edgecapture)

**实现要求**（保留原题的代码、列表及子问）：

[edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")Previous

Next[dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")

For each bit in a 32-bit vector, capture when the input signal changes from 1 in one clock cycle to 0 the next. "Capture" means that the output will remain 1 until the register is reset (synchronous reset).

Each output bit behaves like a SR flip-flop: The output bit should be set (to 1) the cycle after a 1 to 0 transition occurs. The output bit should be reset (to 0) at the positive clock edge when reset is high. If both of the above events occur at the same time, reset has precedence. In the last 4 cycles of the example waveform below, the 'reset' event occurs one cycle earlier than the 'set' event, so there is no conflict here.

In the example waveform below, reset, in[1] and out[1] are shown again separately for clarity.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4c](../references/markdown/2841a21f43f6612b.md "exams/m2014_q4c")
- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2") ·

**edgecapture**

- · [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")

[edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")Previous

Next[dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,
    input [31:0] in,
    output [31:0] out
);
```

<a id="hdl-098"></a>

### HDL-098 Dual-edge triggered flip-flop

来源：本地原文（原完整交付引用：`<../references/markdown/bd7700a9a71ba62d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/dualedge)

**实现要求**（保留原题的代码、列表及子问）：

[edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")Previous

Next[count15](../references/markdown/7b23dc918089c762.md "count15")

You're familiar with flip-flops that are triggered on the positive edge of the clock, or negative edge of the clock. A dual-edge triggered flip-flop is triggered on both edges of the clock. However, FPGAs don't have dual-edge triggered flip-flops, and always @(posedge clk or negedge clk) is not accepted as a legal sensitivity list.

Build a circuit that functionally behaves like a dual-edge triggered flip-flop:

(Note: It's not necessarily perfectly equivalent: The output of flip-flops have no glitches, but a larger combinational circuit that emulates this behaviour might. But we'll ignore this detail here.)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4d](../references/markdown/5af9f9695ae8f506.md "exams/m2014_q4d")
- [mt2015\_muxdff](../references/markdown/918c137acd15c1ee.md "mt2015_muxdff")
- [exams/2014\_q4a](../references/markdown/24823d4b6666b37b.md "exams/2014_q4a")
- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture") ·

**dualedge**

- · [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")

[edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")Previous

Next[count15](../references/markdown/7b23dc918089c762.md "count15")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 此题的双沿实现仅用于语言练习，不得直接带入 E8/B5 禁下降沿时钟的 DUT。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input d,
    output q
);
```

<a id="hdl-101"></a>

### HDL-101 Decade counter again

来源：本地原文（原完整交付引用：`<../references/markdown/eaab293e1b7d948a.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/count1to10)

**实现要求**（保留原题的代码、列表及子问）：

[count10](../references/markdown/50068896f0fea3f2.md "count10")Previous

Next[countslow](../references/markdown/8a07c2c64dac5215.md "countslow")

Make a decade counter that counts 1 through 10, inclusive. The reset input is synchronous, and should reset the counter to 1.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2014\_q4](../references/markdown/7e36c8e5f19f655e.md "exams/ece241_2014_q4")
- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10") ·

**count1to10**

- · [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")

[count10](../references/markdown/50068896f0fea3f2.md "count10")Previous

Next[countslow](../references/markdown/8a07c2c64dac5215.md "countslow")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,
    output [3:0] q);
```

<a id="hdl-102"></a>

### HDL-102 Slow decade counter

来源：本地原文（原完整交付引用：`<../references/markdown/8a07c2c64dac5215.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/countslow)

**实现要求**（保留原题的代码、列表及子问）：

[count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")Previous

Next[exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")

Build a decade counter that counts from 0 through 9, inclusive, with a period of 10. The reset input is synchronous, and should reset the counter to 0. We want to be able to pause the counter rather than always incrementing every clock cycle, so the slowena input indicates when the counter should increment.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2013\_q7](../references/markdown/ad3d76f5fa691b07.md "exams/ece241_2013_q7")
- [edgedetect](../references/markdown/95cba20f30db53f7.md "edgedetect")
- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10") ·

**countslow**

- · [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")

[count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")Previous

Next[exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input slowena,
    input reset,
    output [3:0] q);
```

<a id="hdl-104"></a>

### HDL-104 Counter 1000

来源：本地原文（原完整交付引用：`<../references/markdown/54f9f0f82b1587e8.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2014_q7b)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")Previous

Next[countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")

From a 1000 Hz clock, derive a 1 Hz signal, called **OneHertz**, that could be used to drive an Enable signal for a set of hour/minute/second counters to create a digital wall clock. Since we want the clock to count once per second, the **OneHertz** signal must be asserted for exactly one cycle each second. Build the frequency divider using modulo-10 (BCD) counters and as few other gates as possible. Also output the enable signals from each of the BCD counters you use (c\_enable[0] for the fastest counter, c\_enable[2] for the slowest).

The following BCD counter is provided for you. **Enable** must be high for the counter to run. **Reset** is synchronous and set high to force the counter to zero. All counters in your circuit must directly use the same 1000 Hz signal.



```
module bcdcount (
	input clk,
	input reset,
	input enable,
	output reg [3:0] Q
);
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [edgedetect2](../references/markdown/3074c6099e9a4cde.md "edgedetect2")
- [edgecapture](../references/markdown/a901d2224de8d362.md "edgecapture")
- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a") ·

**exams/ece241\_2014\_q7b**

- · [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")

[exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")Previous

Next[countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,
    output OneHertz,
    output [2:0] c_enable
);
```

<a id="hdl-106"></a>

### HDL-106 12-hour clock

来源：本地原文（原完整交付引用：`<../references/markdown/6419e79796d34234.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/count_clock)

**实现要求**（保留原题的代码、列表及子问）：

[countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")Previous

Next[shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")

Create a set of counters suitable for use as a 12-hour clock (with am/pm indicator). Your counters are clocked by a fast-running clk, with a pulse on ena whenever your clock should increment (i.e., once per second).

reset resets the clock to 12:00 AM. pm is 0 for AM and 1 for PM. hh, mm, and ss are two **BCD** (Binary-Coded Decimal) digits each for hours (01-12), minutes (00-59), and seconds (00-59). Reset has higher priority than enable, and can occur even when not enabled.

The following timing diagram shows the rollover behaviour from 11:59:59 AM to 12:00:00 PM and the synchronous reset and enable behaviour.


```json5
{ signal: [{ name: "clk", wave: "p........" },
  { name: "reset", wave: "0...10..." },
  { name: "ena", wave:   "1...x1.0." },
  { name: "pm", wave: "0..1.0...", data: ["57", "58", "59", "00", "01", "00", "01", "02" ] },
  { name: "hh[7:0]", wave: "=..=.....", data: ["8'h11", "8'h12"] },
  { name: "mm[7:0]", wave: "=..=.....", data: ["8'h59", "8'h00"] },
  { name: "ss[7:0]", wave: "========.", data: ["8'h57", "8'h58", "8'h59", "8'h00", "8'h01", "8'h00", "8'h01", "8'h02" ] }
] }
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [dualedge](../references/markdown/bd7700a9a71ba62d.md "dualedge")
- [count15](../references/markdown/7b23dc918089c762.md "count15")
- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd") ·

**count\_clock**

- · [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")

[countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")Previous

Next[shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input reset,
    input ena,
    output pm,
    output [7:0] hh,
    output [7:0] mm,
    output [7:0] ss);
```

<a id="hdl-108"></a>

### HDL-108 Left/right rotator

来源：本地原文（原完整交付引用：`<../references/markdown/03581c4141024d71.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/rotate100)

**实现要求**（保留原题的代码、列表及子问）：

[shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")Previous

Next[shift18](../references/markdown/0f207e129a1b3014.md "shift18")

Build a 100-bit left/right rotator, with synchronous load and left/right enable. A rotator shifts-in the shifted-out bit from the other end of the register, unlike a shifter that discards the shifted-out bit and shifts in a zero. If enabled, a rotator rotates the bits around and does not modify/discard them.

- load: Loads shift register with data[99:0] instead of rotating.
- ena[1:0]: Chooses whether and which direction to rotate.
  - 2'b01 rotates right by one bit
  - 2'b10 rotates left by one bit
  - 2'b00 and 2'b11 do not rotate.
- q: The contents of the rotator.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [count10](../references/markdown/50068896f0fea3f2.md "count10")
- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4") ·

**rotate100**

- · [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")

[shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")Previous

Next[shift18](../references/markdown/0f207e129a1b3014.md "shift18")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input load,
    input [1:0] ena,
    input [99:0] data,
    output reg [99:0] q);
```

<a id="hdl-109"></a>

### HDL-109 Left/right arithmetic shift by 1 or 8

来源：本地原文（原完整交付引用：`<../references/markdown/0f207e129a1b3014.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/shift18)

**实现要求**（保留原题的代码、列表及子问）：

[rotate100](../references/markdown/03581c4141024d71.md "rotate100")Previous

Next[lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")

Build a 64-bit *arithmetic* shift register, with synchronous load. The shifter can shift both left and right, and by 1 or 8 bit positions, selected by amount.

An *arithmetic* right shift shifts in the sign bit of the number in the shift register (q[63] in this case) instead of zero as done by a *logical* right shift. Another way of thinking about an arithmetic right shift is that it assumes the number being shifted is signed and preserves the sign, so that arithmetic right shift divides a signed number by a power of two.

There is no difference between logical and arithmetic *left* shifts.

- load: Loads shift register with data[63:0] instead of shifting.
- ena: Chooses whether to shift.
- amount: Chooses which direction and how much to shift.
  - 2'b00: shift left by 1 bit.
  - 2'b01: shift left by 8 bits.
  - 2'b10: shift right by 1 bit.
  - 2'b11: shift right by 8 bits.
- q: The contents of the shifter.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [count1to10](../references/markdown/eaab293e1b7d948a.md "count1to10")
- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100") ·

**shift18**

- · [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")

[rotate100](../references/markdown/03581c4141024d71.md "rotate100")Previous

Next[lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input load,
    input ena,
    input [1:0] amount,
    input [63:0] data,
    output reg [63:0] q);
```

<a id="hdl-110"></a>

### HDL-110 5-bit LFSR

来源：本地原文（原完整交付引用：`<../references/markdown/e44607c44f1915e8.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/lfsr5)

**实现要求**（保留原题的代码、列表及子问）：

[shift18](../references/markdown/0f207e129a1b3014.md "shift18")Previous

Next[mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")

A [linear feedback shift register](https://en.wikipedia.org/wiki/Linear_feedback_shift_register) is a shift register usually with a few XOR gates to produce the next state of the shift register. A Galois LFSR is one particular arrangement where bit positions with a "tap" are XORed with the output bit to produce its next value, while bit positions without a tap shift. If the taps positions are carefully chosen, the LFSR can be made to be "maximum-length". A maximum-length LFSR of n bits cycles through 2n-1 states before repeating (the all-zero state is never reached).

The following diagram shows a 5-bit maximal-length Galois LFSR with taps at bit positions 5 and 3. (Tap positions are usually numbered starting from 1). Note that I drew the XOR gate at position 5 for consistency, but one of the XOR gate inputs is 0.  
![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/9/9a/Lfsr5.png`）](https://hdlbits.01xz.net/wiki/File:Lfsr5.png)

Build this LFSR. The reset should reset the LFSR to 1.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [countslow](../references/markdown/8a07c2c64dac5215.md "countslow")
- [exams/ece241\_2014\_q7a](../references/markdown/8524d38886179beb.md "exams/ece241_2014_q7a")
- [exams/ece241\_2014\_q7b](../references/markdown/54f9f0f82b1587e8.md "exams/ece241_2014_q7b")
- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18") ·

**lfsr5**

- · [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")

[shift18](../references/markdown/0f207e129a1b3014.md "shift18")Previous

Next[mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input reset,    // Active-high synchronous reset to 5'h1
    output [4:0] q
);
```

<a id="hdl-113"></a>

### HDL-113 Shift register

来源：本地原文（原完整交付引用：`<../references/markdown/ff6fbf2b046c1148.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/m2014_q4k)

**实现要求**（保留原题的代码、列表及子问）：

[lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")Previous

Next[exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")

Implement the following circuit:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/1/15/Exams_m2014q4k.png`）](https://hdlbits.01xz.net/wiki/File:Exams_m2014q4k.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [countbcd](../references/markdown/fb9ceaba1a605add.md "countbcd")
- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32") ·

**exams/m2014\_q4k**

- · [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")

[lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")Previous

Next[exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 同名题按各自原图分别建 TB，不合并成同一道。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input resetn,   // synchronous reset
    input in,
    output out);
```

<a id="hdl-114"></a>

### HDL-114 Shift register

来源：本地原文（原完整交付引用：`<../references/markdown/8a468338f383e85d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2014_q4b)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")Previous

Next[exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")

Consider the *n*-bit shift register circuit shown below:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.e674472e9a7d5482.e674472e9a7d5482.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2014q4.png)

Write a top-level Verilog module (named top\_module) for the shift register, assuming that *n* = 4. Instantiate four
copies of your MUXDFF subcircuit in your top-level module. Assume that you are going to implement the circuit on the DE2 board.

- Connect the *R* inputs to the *SW* switches,
- *clk* to *KEY[0]*,
- *E* to *KEY[1]*,
- *L* to *KEY[2]*, and
- *w* to *KEY[3]*.
- Connect the outputs to the red lights *LEDR[3:0]*.

(Reuse your MUXDFF from [exams/2014\_q4a](https://hdlbits.01xz.net/wiki/Exams/2014_q4a "Exams/2014 q4a").)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [count\_clock](../references/markdown/6419e79796d34234.md "count_clock")
- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k") ·

**exams/2014\_q4b**

- · [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")

[exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")Previous

Next[exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 同名题按各自原图分别建 TB，不合并成同一道。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input [3:0] SW,
    input [3:0] KEY,
    output [3:0] LEDR
);
```

<a id="hdl-115"></a>

### HDL-115 3-input LUT

来源：本地原文（原完整交付引用：`<../references/markdown/ffd1f0eb7e2a4e9d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2013_q12)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")Previous

Next[rule90](../references/markdown/33ef5003c6c93530.md "rule90")

In this question, you will design a circuit for an 8x1 memory, where writing to the memory is accomplished by shifting-in bits, and reading is "random access", as in a typical RAM. You will then use the circuit to realize a 3-input logic function.

First, create an 8-bit shift register with 8 D-type flip-flops. Label the flip-flop outputs from Q[0]...Q[7]. The shift register input should be called **S**, which feeds the input of Q[0] (MSB is shifted in first). The **enable** input controls whether to shift. Then, extend the circuit to have 3 additional inputs **A**,**B**,**C** and an output **Z**. The circuit's behaviour should be as follows: when ABC is 000, Z=Q[0], when ABC is 001, Z=Q[1], and so on. Your circuit should contain ONLY the 8-bit shift register, and multiplexers. (Aside: this circuit is called a 3-input look-up-table (LUT)).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [shift4](../references/markdown/e3fa4e3c9fc96635.md "shift4")
- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b") ·

**exams/ece241\_2013\_q12**

- · [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")

[exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")Previous

Next[rule90](../references/markdown/33ef5003c6c93530.md "rule90")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input enable,
    input S,
    input A, B, C,
    output Z );
```

<a id="hdl-116"></a>

### HDL-116 Rule 90

来源：本地原文（原完整交付引用：`<../references/markdown/33ef5003c6c93530.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/rule90)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")Previous

Next[rule110](../references/markdown/52d53bbb3a53b028.md "rule110")

[Rule 90](https://en.wikipedia.org/wiki/Rule_90) is a one-dimensional cellular automaton with interesting properties.

The rules are simple. There is a one-dimensional array of cells (on or off). At each time step, the next state of each cell is the XOR of the cell's two current neighbours. A more verbose way of expressing this rule is the following table, where a cell's next state is a function of itself and its two neighbours:

| Left | Center | Right | Center's next state |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 |

(The name "Rule 90" comes from reading the "next state" column: 01011010 is decimal 90.)

In this circuit, create a 512-cell system (q[511:0]), and advance by one time step each clock cycle. The load input indicates the state of the system should be loaded with data[511:0]. Assume the boundaries (q[-1] and q[512]) are both zero (off).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [rotate100](../references/markdown/03581c4141024d71.md "rotate100")
- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12") ·

**rule90**

- · [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")

[exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")Previous

Next[rule110](../references/markdown/52d53bbb3a53b028.md "rule110")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input load,
    input [511:0] data,
    output [511:0] q );
```

<a id="hdl-117"></a>

### HDL-117 Rule 110

来源：本地原文（原完整交付引用：`<../references/markdown/52d53bbb3a53b028.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/rule110)

**实现要求**（保留原题的代码、列表及子问）：

[rule90](../references/markdown/33ef5003c6c93530.md "rule90")Previous

Next[conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")

[Rule 110](https://en.wikipedia.org/wiki/Rule_110) is a one-dimensional cellular automaton with interesting properties (such as being [Turing-complete](https://en.wikipedia.org/wiki/Turing_completeness)).

There is a one-dimensional array of cells (on or off). At each time step, the state of each cell changes. In Rule 110, the next state of each cell depends only on itself and its two neighbours, according to the following table:

| Left | Center | Right | Center's next state |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 |
| 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 |

(The name "Rule 110" comes from reading the "next state" column: 01101110 is decimal 110.)

In this circuit, create a 512-cell system (q[511:0]), and advance by one time step each clock cycle. The load input indicates the state of the system should be loaded with data[511:0]. Assume the boundaries (q[-1] and q[512]) are both zero (off).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [shift18](../references/markdown/0f207e129a1b3014.md "shift18")
- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90") ·

**rule110**

- · [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")

[rule90](../references/markdown/33ef5003c6c93530.md "rule90")Previous

Next[conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input load,
    input [511:0] data,
    output [511:0] q
);
```

<a id="hdl-118"></a>

### HDL-118 Conway's Game of Life 16x16

来源：本地原文（原完整交付引用：`<../references/markdown/69da8d3ebdffae27.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/conwaylife)

**实现要求**（保留原题的代码、列表及子问）：

[rule110](../references/markdown/52d53bbb3a53b028.md "rule110")Previous

Next[fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")

[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life) is a two-dimensional cellular automaton.

The "game" is played on a two-dimensional grid of cells, where each cell is either 1 (alive) or 0 (dead). At each time step, each cell changes state depending on how many neighbours it has:

- 0-1 neighbour: Cell becomes 0.
- 2 neighbours: Cell state does not change.
- 3 neighbours: Cell becomes 1.
- 4+ neighbours: Cell becomes 0.

The game is formulated for an infinite grid. In this circuit, we will use a 16x16 grid. To make things more interesting, we will use a 16x16 toroid, where the sides wrap around to the other side of the grid. For example, the corner cell (0,0) has 8 neighbours: (15,1), (15,0), (15,15), (0,1), (0,15), (1,1), (1,0), and (1,15). The 16x16 grid is represented by a length 256 vector, where each row of 16 cells is represented by a sub-vector: q[15:0] is row 0, q[31:16] is row 1, etc. (This tool accepts SystemVerilog, so you may use 2D vectors if you wish.)

- load: Loads data into q at the next clock edge, for loading initial state.
- q: The 16x16 current state of the game, updated every clock cycle.

The game state should advance by one timestep every clock cycle.

*[John Conway](https://en.wikipedia.org/wiki/John_Horton_Conway), mathematician and creator of the Game of Life cellular automaton, passed away from COVID-19 on April 11, 2020.*

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lfsr5](../references/markdown/e44607c44f1915e8.md "lfsr5")
- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110") ·

**conwaylife**

- · [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")

[rule110](../references/markdown/52d53bbb3a53b028.md "rule110")Previous

Next[fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input load,
    input [255:0] data,
    output [255:0] q );
```

<a id="hdl-119"></a>

### HDL-119 Simple FSM 1 (asynchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/76a0bdd17a04d8ce.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm1)

**实现要求**（保留原题的代码、列表及子问）：

[conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")Previous

Next[fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")

This is a Moore state machine with two states, one input, and one output. Implement this state machine. Notice that the reset state is B.

This exercise is the same as [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s"), but using asynchronous reset.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/7/70/Fsm1.png`）](https://hdlbits.01xz.net/wiki/File:Fsm1.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [mt2015\_lfsr](../references/markdown/a5f0fed46b552e71.md "mt2015_lfsr")
- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife") ·

**fsm1**

- · [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")

[conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")Previous

Next[fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Asynchronous reset to state B
    input in,
    output out);
```

<a id="hdl-120"></a>

### HDL-120 Simple FSM 1 (synchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/35b85c4e8f126c0e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm1s)

**实现要求**（保留原题的代码、列表及子问）：

[fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")Previous

Next[fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")

This is a Moore state machine with two states, one input, and one output. Implement this state machine. Notice that the reset state is B.

This exercise is the same as [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1"), but using synchronous reset.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/8/82/Fsm1s.png`）](https://hdlbits.01xz.net/wiki/File:Fsm1s.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lfsr32](../references/markdown/511c15a894b9c848.md "lfsr32")
- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1") ·

**fsm1s**

- · [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")

[fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")Previous

Next[fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
// Note the Verilog-1995 module declaration syntax here:
module top_module(clk, reset, in, out);
    input clk;
    input reset;    // Synchronous reset to state B
    input in;
    output out;
```

<a id="hdl-121"></a>

### HDL-121 Simple FSM 2 (asynchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/41f2db0c81bcad5a.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm2)

**实现要求**（保留原题的代码、列表及子问）：

[fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")Previous

Next[fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")

This is a Moore state machine with two states, two inputs, and one output. Implement this state machine.

This exercise is the same as [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s"), but using asynchronous reset.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/b/b8/Fsmjk.png`）](https://hdlbits.01xz.net/wiki/File:Fsmjk.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/m2014\_q4k](../references/markdown/ff6fbf2b046c1148.md "exams/m2014_q4k")
- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s") ·

**fsm2**

- · [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")

[fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")Previous

Next[fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Asynchronous reset to OFF
    input j,
    input k,
    output out);
```

<a id="hdl-122"></a>

### HDL-122 Simple FSM 2 (synchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/6751f58ebe64cc6e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm2s)

**实现要求**（保留原题的代码、列表及子问）：

[fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")Previous

Next[fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")

This is a Moore state machine with two states, two inputs, and one output. Implement this state machine.

This exercise is the same as [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2"), but using synchronous reset.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/5/5d/Fsmjks.png`）](https://hdlbits.01xz.net/wiki/File:Fsmjks.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/2014\_q4b](../references/markdown/8a468338f383e85d.md "exams/2014_q4b")
- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2") ·

**fsm2s**

- · [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")

[fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")Previous

Next[fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input reset,    // Synchronous reset to OFF
    input j,
    input k,
    output out);
```

<a id="hdl-123"></a>

### HDL-123 Simple state transitions 3

来源：本地原文（原完整交付引用：`<../references/markdown/406afb44395b2edf.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm3comb)

**实现要求**（保留原题的代码、列表及子问）：

[fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")Previous

Next[fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")

The following is the state transition table for a Moore state machine with one input, one output, and four states. Use the following state encoding: A=2'b00, B=2'b01, C=2'b10, D=2'b11.

**Implement only the state transition logic and output logic** (the combinational logic portion) for this state machine. Given the current state (`state`), compute the `next_state` and output (`out`) based on the state transition table.

| State | Next state | | Output |
| --- | --- | --- | --- |
| in=0 | in=1 |
| A | A | B | 0 |
| B | C | B | 0 |
| C | A | D | 0 |
| D | C | B | 1 |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2013\_q12](../references/markdown/ffd1f0eb7e2a4e9d.md "exams/ece241_2013_q12")
- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s") ·

**fsm3comb**

- · [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")

[fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")Previous

Next[fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input in,
    input [1:0] state,
    output [1:0] next_state,
    output out);
```

<a id="hdl-124"></a>

### HDL-124 Simple one-hot state transitions 3

来源：本地原文（原完整交付引用：`<../references/markdown/708391a43c8f1d33.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm3onehot)

**实现要求**（保留原题的代码、列表及子问）：

[fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")Previous

Next[fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")

The following is the state transition table for a Moore state machine with one input, one output, and four states. Use the following one-hot state encoding: A=4'b0001, B=4'b0010, C=4'b0100, D=4'b1000.

**Derive state transition and output logic equations by inspection** assuming a one-hot encoding. Implement only the state transition logic and output logic (the combinational logic portion) for this state machine. (The testbench will test with non-one hot inputs to make sure you're not trying to do something more complicated).

| State | Next state | | Output |
| --- | --- | --- | --- |
| in=0 | in=1 |
| A | A | B | 0 |
| B | C | B | 0 |
| C | A | D | 0 |
| D | C | B | 1 |

#### What does "derive equations by inspection" mean?

One-hot state machine encoding guarantees that exactly one state bit is 1. This means that it is possible to determine whether the state machine is in a particular state by examining only *one* state bit, not *all* state bits. This leads to simple logic equations for the state transitions by examining the incoming edges for each state in the state transition diagram.

For example, in the above state machine, how can the state machine can reach state A? It must use one of the two incoming edges: "Currently in state A and in=0" or "Currently in state C and in = 0". Due to the one-hot encoding, the logic equation to test for "currently in state A" is simply the state bit for state A. This leads to the final logic equation for the next state of state bit A: `next_state[0] = state[0]&(~in) | state[2]&(~in)`. The one-hot encoding guarantees that at most one clause (product term) will be "active" at a time, so the clauses can just be ORed together.

When an exercise asks for state transition equations "by inspection", use this particular method. The judge will test with non-one-hot inputs to ensure your logic equations follow this method, rather that doing something else (such as resetting the FSM) for illegal (non-one-hot) combinations of the state bits.

Although knowing this algorithm isn't necessary for RTL-level design (the logic synthesizer handles this), it is illustrative of why one-hot FSMs often have simpler logic (at the expense of more state bit storage), and this topic frequently shows up on exams in digital logic courses.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [rule90](../references/markdown/33ef5003c6c93530.md "rule90")
- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb") ·

**fsm3onehot**

- · [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")

[fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")Previous

Next[fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input in,
    input [3:0] state,
    output [3:0] next_state,
    output out);
```

<a id="hdl-125"></a>

### HDL-125 Simple FSM 3 (asynchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/283a7148cd6d78c4.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm3)

**实现要求**（保留原题的代码、列表及子问）：

[fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")Previous

Next[fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")

See also: [State transition logic for this FSM](https://hdlbits.01xz.net/wiki/Fsm3comb "Fsm3comb")

The following is the state transition table for a Moore state machine with one input, one output, and four states. Implement this state machine. Include an asynchronous reset that resets the FSM to state A.

| State | Next state | | Output |
| --- | --- | --- | --- |
| in=0 | in=1 |
| A | A | B | 0 |
| B | C | B | 0 |
| C | A | D | 0 |
| D | C | B | 1 |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [rule110](../references/markdown/52d53bbb3a53b028.md "rule110")
- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot") ·

**fsm3**

- · [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")

[fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")Previous

Next[fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input in,
    input areset,
    output out);
```

<a id="hdl-126"></a>

### HDL-126 Simple FSM 3 (synchronous reset)

来源：本地原文（原完整交付引用：`<../references/markdown/149bc8ab6b32919d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm3s)

**实现要求**（保留原题的代码、列表及子问）：

[fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")Previous

Next[exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")

See also: [State transition logic for this FSM](https://hdlbits.01xz.net/wiki/Fsm3comb "Fsm3comb")

The following is the state transition table for a Moore state machine with one input, one output, and four states. Implement this state machine. Include a synchronous reset that resets the FSM to state A. (This is the same problem as [Fsm3](https://hdlbits.01xz.net/wiki/Fsm3 "Fsm3") but with a synchronous reset.)

| State | Next state | | Output |
| --- | --- | --- | --- |
| in=0 | in=1 |
| A | A | B | 0 |
| B | C | B | 0 |
| C | A | D | 0 |
| D | C | B | 1 |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [conwaylife](../references/markdown/69da8d3ebdffae27.md "conwaylife")
- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3") ·

**fsm3s**

- · [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")

[fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")Previous

Next[exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input in,
    input reset,
    output out);
```

<a id="hdl-127"></a>

### HDL-127 Design a Moore FSM

来源：本地原文（原完整交付引用：`<../references/markdown/c24eb30f8cef5e63.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2013_q4)

**实现要求**（保留原题的代码、列表及子问）：

[fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")Previous

Next[lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.57acd2bcb5b7457a.57acd2bcb5b7457a.png`）](https://hdlbits.01xz.net/wiki/File:Ece241_2013_q4.png)

Also include an active-high synchronous reset that resets the state machine to a state equivalent to if the water level had been low for a long time (no sensors asserted, and all four outputs asserted).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm1](../references/markdown/76a0bdd17a04d8ce.md "fsm1")
- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s") ·

**exams/ece241\_2013\_q4**

- · [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")

[fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")Previous

Next[lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,
    input [3:1] s,
    output fr3,
    output fr2,
    output fr1,
    output dfr
);
```

<a id="hdl-128"></a>

### HDL-128 Lemmings 1

来源：本地原文（原完整交付引用：`<../references/markdown/a83eb8a3dded5175.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/lemmings1)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")Previous

Next[lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/d/de/Lemmings.gif`）](https://hdlbits.01xz.net/wiki/File:Lemmings.gif)

The game [Lemmings](https://en.wikipedia.org/wiki/Lemmings_%28video_game%29) involves critters with fairly simple brains. So simple that we are going to model it using a finite state machine.

In the Lemmings' 2D world, Lemmings can be in one of two states: walking left or walking right. It will switch directions if it hits an obstacle. In particular, if a Lemming is bumped on the left, it will walk right. If it's bumped on the right, it will walk left. If it's bumped on both sides at the same time, it will still switch directions.

Implement a Moore state machine with two states, two inputs, and one output that models this behaviour.

See also: [Lemmings2](https://hdlbits.01xz.net/wiki/Lemmings2 "Lemmings2"), [Lemmings3](https://hdlbits.01xz.net/wiki/Lemmings3 "Lemmings3"), and [Lemmings4](https://hdlbits.01xz.net/wiki/Lemmings4 "Lemmings4").

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm1s](../references/markdown/35b85c4e8f126c0e.md "fsm1s")
- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4") ·

**lemmings1**

- · [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")

[exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")Previous

Next[lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。 覆盖碰墙/悬空/落地/挖掘优先级；Lemmings4 的坠落阈值按原题逐拍边界检查。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    output walk_left,
    output walk_right);
```

<a id="hdl-129"></a>

### HDL-129 Lemmings 2

来源：本地原文（原完整交付引用：`<../references/markdown/b51b08821d94c444.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/lemmings2)

**实现要求**（保留原题的代码、列表及子问）：

[lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")Previous

Next[lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/7/70/Lemmings2.gif`）](https://hdlbits.01xz.net/wiki/File:Lemmings2.gif)

See also: [Lemmings1](https://hdlbits.01xz.net/wiki/Lemmings1 "Lemmings1").

In addition to walking left and right, Lemmings will fall (and presumably go "aaah!") if the ground disappears underneath them.

In addition to walking left and right and changing direction when bumped, when ground=0, the Lemming will fall and say "aaah!". When the ground reappears (ground=1), the Lemming will resume walking in the same direction as before the fall. Being bumped while falling does not affect the walking direction, and being bumped in the same cycle as ground disappears (but not yet falling), or when the ground reappears while still falling, also does not affect the walking direction.

Build a finite state machine that models this behaviour.

See also: [Lemmings3](https://hdlbits.01xz.net/wiki/Lemmings3 "Lemmings3") and [Lemmings4](https://hdlbits.01xz.net/wiki/Lemmings4 "Lemmings4").

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm2](../references/markdown/41f2db0c81bcad5a.md "fsm2")
- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1") ·

**lemmings2**

- · [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")

[lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")Previous

Next[lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。 覆盖碰墙/悬空/落地/挖掘优先级；Lemmings4 的坠落阈值按原题逐拍边界检查。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    input ground,
    output walk_left,
    output walk_right,
    output aaah );
```

<a id="hdl-130"></a>

### HDL-130 Lemmings 3

来源：本地原文（原完整交付引用：`<../references/markdown/6b28c15d5960c9f6.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/lemmings3)

**实现要求**（保留原题的代码、列表及子问）：

[lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")Previous

Next[lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/a2/Lemmings3.gif`）](https://hdlbits.01xz.net/wiki/File:Lemmings3.gif)

See also: [Lemmings1](https://hdlbits.01xz.net/wiki/Lemmings1 "Lemmings1") and [Lemmings2](https://hdlbits.01xz.net/wiki/Lemmings2 "Lemmings2").

In addition to walking and falling, Lemmings can sometimes be told to do useful things, like dig (it starts digging when dig=1). A Lemming can dig if it is currently walking on ground (ground=1 and not falling), and will continue digging until it reaches the other side (ground=0). At that point, since there is no ground, it will fall (aaah!), then continue walking in its original direction once it hits ground again. As with falling, being bumped while digging has no effect, and being told to dig when falling or when there is no ground is ignored.

(In other words, a walking Lemming can fall, dig, or switch directions. If more than one of these conditions are satisfied, fall has higher precedence than dig, which has higher precedence than switching directions.)

Extend your finite state machine to model this behaviour.

See also: [Lemmings4](https://hdlbits.01xz.net/wiki/Lemmings4 "Lemmings4").

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm2s](../references/markdown/6751f58ebe64cc6e.md "fsm2s")
- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2") ·

**lemmings3**

- · [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")

[lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")Previous

Next[lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。 覆盖碰墙/悬空/落地/挖掘优先级；Lemmings4 的坠落阈值按原题逐拍边界检查。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    input ground,
    input dig,
    output walk_left,
    output walk_right,
    output aaah,
    output digging );
```

<a id="hdl-131"></a>

### HDL-131 Lemmings 4

来源：本地原文（原完整交付引用：`<../references/markdown/0e4028830111a85a.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/lemmings4)

**实现要求**（保留原题的代码、列表及子问）：

[lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")Previous

Next[fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/e/e8/Lemmings4.gif`）](https://hdlbits.01xz.net/wiki/File:Lemmings4.gif)

See also: [Lemmings1](https://hdlbits.01xz.net/wiki/Lemmings1 "Lemmings1"), [Lemmings2](https://hdlbits.01xz.net/wiki/Lemmings2 "Lemmings2"), and [Lemmings3](https://hdlbits.01xz.net/wiki/Lemmings3 "Lemmings3").

Although Lemmings can walk, fall, and dig, Lemmings aren't invulnerable. If a Lemming falls for too long then hits the ground, it can splatter. In particular, if a Lemming falls for more than 20 clock cycles then hits the ground, it will splatter and cease walking, falling, or digging (all 4 outputs become 0), forever (Or until the FSM gets reset). There is no upper limit on how far a Lemming can fall before hitting the ground. Lemmings only splatter when hitting the ground; they do not splatter in mid-air.

Extend your finite state machine to model this behaviour.

Falling for 20 cycles is survivable:


```json5
{ signal: [
  { name: "clk", wave: "p............" },
      { name: "ground",       wave: "1.0...|..1..." },
      { name: "walk_left",    wave: "1..0..|...1.." },
      { name: "aaah",         wave: "0..1..|...0.." }, 
 ], 
foot:{
   tock:['', '', '',1,2,3, '...', 18, 19, 20] 
 }
}
```



Falling for 21 cycles causes splatter:


```json5
{ signal: [
  { name: "clk", wave: "p............" },
      { name: "ground",       wave: "1.0...|...1.." },
      { name: "walk_left",    wave: "1..0..|......" },
      { name: "aaah",         wave: "0..1..|....0." }, 
 ], 
foot:{
   tock:['', '', '',1,2,3, '...', 18, 19, 20, 21, 'oops'] 
 }
}
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm3comb](../references/markdown/406afb44395b2edf.md "fsm3comb")
- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3") ·

**lemmings4**

- · [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")

[lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")Previous

Next[fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。 覆盖碰墙/悬空/落地/挖掘优先级；Lemmings4 的坠落阈值按原题逐拍边界检查。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input areset,    // Freshly brainwashed Lemmings walk left.
    input bump_left,
    input bump_right,
    input ground,
    input dig,
    output walk_left,
    output walk_right,
    output aaah,
    output digging );
```

<a id="hdl-132"></a>

### HDL-132 One-hot FSM

来源：本地原文（原完整交付引用：`<../references/markdown/745013775b0fd13e.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_onehot)

**实现要求**（保留原题的代码、列表及子问）：

[lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")Previous

Next[fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")

Given the following state machine with 1 input and 2 outputs:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/a/a7/Fsmonehot.png`）](https://hdlbits.01xz.net/wiki/File:Fsmonehot.png)

Suppose this state machine uses one-hot encoding, where state[0] through state[9] correspond to the states S0 though S9, respectively. The outputs are zero unless otherwise specified.

Implement the **state transition logic** and **output logic** portions of the state machine (but not the state flip-flops). You are given the current state in state[9:0] and must produce next\_state[9:0] and the two outputs. Derive the logic equations by inspection assuming a one-hot encoding. (The testbench will test with non-one hot inputs to make sure you're not trying to do something more complicated).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm3onehot](../references/markdown/708391a43c8f1d33.md "fsm3onehot")
- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4") ·

**fsm\_onehot**

- · [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")

[lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")Previous

Next[fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input in,
    input [9:0] state,
    output [9:0] next_state,
    output out1,
    output out2);
```

<a id="hdl-133"></a>

### HDL-133 PS/2 packet parser

来源：本地原文（原完整交付引用：`<../references/markdown/a7126c946eeae72d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_ps2)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")Previous

Next[fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")

The PS/2 mouse protocol sends messages that are three bytes long. However, within a continuous byte stream, it's not obvious where messages start and end. The only indication is that the first byte of each three byte message always has bit[3]=1 (but bit[3] of the other two bytes may be 1 or 0 depending on data).

We want a finite state machine that will search for message boundaries when given an input byte stream. The algorithm we'll use is to discard bytes until we see one with bit[3]=1. We then assume that this is byte 1 of a message, and signal the receipt of a message once all 3 bytes have been received (done).

The FSM should signal done in the cycle immediately after the third byte of each message was successfully received.

### Some timing diagrams to explain the desired behaviour

Under error-free conditions, every three bytes form a message:


```json5
{ signal: [{ name: "clk", wave: "p........." },
  { name: "reset", wave:"10........" },
  { name: "in[3]", wave:"x1x.1x.1x." },
  { name: "done", wave: "x0..10.10." },
],
foot:{
   tock:['', 'byte1', 'byte2', 'byte3','byte1', 'byte2', 'byte3','byte1', 'byte2', 'byte3'] } }
```



When an error occurs, search for byte 1:


```json5
{ signal: [{ name: "clk", wave: "p..........." },
  { name: "reset", wave:"10.........." },
  { name: "in[3]", wave:"x1x.0.1x.1x." },
  { name: "done", wave: "x0..10...10." },
],
foot:{
   tock:['', 'byte1', 'byte2', 'byte3','?', '?', 'byte1','byte2', 'byte3', 'byte1', 'byte2', 'byte3'] } }
```



Note that this is not the same as a 1xx sequence recognizer. Overlapping sequences are not allowed here:

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm3](../references/markdown/283a7148cd6d78c4.md "fsm3")
- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot") ·

**fsm\_ps2**

- · [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")

[fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")Previous

Next[fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input [7:0] in,
    input reset,    // Synchronous reset
    output done);
```

<a id="hdl-134"></a>

### HDL-134 PS/2 packet parser and datapath

来源：本地原文（原完整交付引用：`<../references/markdown/40f8c235cc74e458.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_ps2data)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")Previous

Next[fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")

See also: [PS/2 packet parser](https://hdlbits.01xz.net/wiki/Fsm_ps2 "Fsm ps2").

Now that you have a state machine that will identify three-byte messages in a PS/2 byte stream, add a datapath that will also output the 24-bit (3 byte) message whenever a packet is received (out\_bytes[23:16] is the first byte, out\_bytes[15:8] is the second byte, etc.).

out\_bytes needs to be valid whenever the done signal is asserted. You may output anything at other times (i.e., don't-care).

For example:


```json5
{ 
config:{hscale:2},
signal: [{ name: "clk", wave: "p........." },
  { name: "reset", wave:"10........" },
  { name: "in[7:0]", wave:"x=========", data:['08', '01', '02', '38', 'ff', 'fe', '08', '03', '04'] },
  { name: "in[3]", wave:"x10.10.10." },
  { name: "done", wave: "x0..10.10." },
  { name: "out_bytes", wave:"x...=x.=x.", data:['080102', '38fffe', '080304'] },
],
foot:{
   tock:['', 'byte1', 'byte2', 'byte3','byte1', 'byte2', 'byte3','byte1', 'byte2', 'byte3'] } }
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm3s](../references/markdown/149bc8ab6b32919d.md "fsm3s")
- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2") ·

**fsm\_ps2data**

- · [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")

[fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")Previous

Next[fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input [7:0] in,
    input reset,    // Synchronous reset
    output [23:0] out_bytes,
    output done);
```

<a id="hdl-135"></a>

### HDL-135 Serial receiver

来源：本地原文（原完整交付引用：`<../references/markdown/c64bb996909dd665.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_serial)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")Previous

Next[fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")

In many (older) serial communications protocols, each data byte is sent along with a start bit and a stop bit, to help the receiver delimit bytes from the stream of bits. One common scheme is to use one start bit (0), 8 data bits, and 1 stop bit (1). The line is also at logic 1 when nothing is being transmitted (idle).

Design a finite state machine that will identify when bytes have been correctly received when given a stream of bits. It needs to identify the start bit, wait for all 8 data bits, then verify that the stop bit was correct. If the stop bit does not appear when expected, the FSM must wait until it finds a stop bit before attempting to receive the next byte.

### Some timing diagrams

Error-free:


```json5
{ signal: [{ name: "clk", wave: "p.........................." },
  { name: "reset", wave:"10........................." },
  { name: "in",    wave:"1.0x.......10x.......1..0x." },
  { name: "done", wave: "0...........10........10..." },
],
foot:{
   tock:['idle', '', 'start', '', '', '', 'data', '', '', '', '', 'stop', '', '', '', '', '', '', '', '', '', 'stop', '', '', 'start'] } }
```



Stop bit not found. First byte is discarded:


```json5
{ signal: [{ name: "clk", wave: "p.........................." },
  { name: "reset", wave:"10........................." },
  { name: "in",    wave:"1.0x.......0.10x.......10x." },
  { name: "done", wave: "0.......................10." },
],
foot:{
   tock:['idle', '', 'start', '', '', '', 'data', '', '', '', '', '?','?!', '', 'start', '', '', '', 'data', '', '', '', '', 'stop' ] } }
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2013\_q4](../references/markdown/c24eb30f8cef5e63.md "exams/ece241_2013_q4")
- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data") ·

**fsm\_serial**

- · [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")

[fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")Previous

Next[fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input in,
    input reset,    // Synchronous reset
    output done
);
```

<a id="hdl-136"></a>

### HDL-136 Serial receiver and datapath

来源：本地原文（原完整交付引用：`<../references/markdown/e2edcdc387fa4a18.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_serialdata)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")Previous

Next[fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")

See also: [Serial receiver](https://hdlbits.01xz.net/wiki/Fsm_serial "Fsm serial")

Now that you have a finite state machine that can identify when bytes are correctly received in a serial bitstream, add a datapath that will output the correctly-received data byte. out\_byte needs to be valid when done is 1, and is don't-care otherwise.

Note that the serial protocol sends the *least* significant bit first.

### Some timing diagrams

Error-free:


```json5
{ signal: [{ name: "clk", wave: "p.........................." },
  { name: "reset", wave:"10........................." },
  { name: "in",    wave: "1.01.010.1010.10..1.01..0x." , node: "...A.......B.C.......D.", phase:0 },
  { name: "done",  wave: "0...........10........10..." },
{ name: "out_byte",wave: "x...........=x........=x...", data:['4b', '62'] },
],
edge: ['A<->B 0x4b', 'C<->D 0x62'],
foot:{
   tock:['idle', '', 'start', '', '', '', 'data', '', '', '', '', 'stop', '', '', '', '', '', '', '', '', '', 'stop', '', '', 'start'] } }
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lemmings1](../references/markdown/a83eb8a3dded5175.md "lemmings1")
- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial") ·

**fsm\_serialdata**

- · [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")

[fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")Previous

Next[fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input in,
    input reset,    // Synchronous reset
    output [7:0] out_byte,
    output done
);
```

<a id="hdl-137"></a>

### HDL-137 Serial receiver with parity checking

来源：本地原文（原完整交付引用：`<../references/markdown/983e83bf12c1ed42.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_serialdp)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")Previous

Next[fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")

See also: [Serial receiver and datapath](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")

We want to add parity checking to the serial receiver. Parity checking adds one extra bit after each data byte. We will use odd parity, where the number of 1s in the 9 bits received must be odd. For example, 101001011 satisfies odd parity (there are 5 1s), but 001001011 does not.

Change your FSM and datapath to perform odd parity checking. Assert the done signal only if a byte is correctly received *and* its parity check passes. Like the [serial receiver FSM](../references/markdown/c64bb996909dd665.md "fsm_serial"), this FSM needs to identify the start bit, wait for all 9 (data and parity) bits, then verify that the stop bit was correct. If the stop bit does not appear when expected, the FSM must wait until it finds a stop bit before attempting to receive the next byte.

You are provided with the following module that can be used to calculate the parity of the input stream (It's a TFF with reset). The intended use is that it should be given the input bit stream, and reset at appropriate times so it counts the number of 1 bits in each byte.



```
module parity (
    input clk,
    input reset,
    input in,
    output reg odd);

    always @(posedge clk)
        if (reset) odd <= 0;
        else if (in) odd <= ~odd;

endmodule

```



Note that the serial protocol sends the least significant bit first, and the parity bit after the 8 data bits.

### Some timing diagrams

No framing errors. Odd parity passes for first byte, fails for second byte.


```json5
{ signal: [{ name: "clk", wave: "p............................" },
  { name: "reset", wave:"10..........................." },
  { name: "in",    wave: "1.01.010.101.0.10..1.01...0x." , node: "...A.......B..C.......D.", phase:0 },
  { name: "done",  wave: "0............10.............." },
{ name: "out_byte",wave: "x............=x..............", data:['4b', '62'] },
],
edge: ['A<->B 0x4b', 'C<->D 0x62'],
foot:{
   tock:['idle', '', 'start', '', '', '', 'data', '', '', '', '', 'parity', '', '', '', '', '', '', '', '', '', '', 'parity', '', '', '', 'start'] } }
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lemmings2](../references/markdown/b51b08821d94c444.md "lemmings2")
- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata") ·

**fsm\_serialdp**

- · [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")

[fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")Previous

Next[fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题；九题自检之一。

接口原样保留：

```verilog
module top_module(
    input clk,
    input in,
    input reset,    // Synchronous reset
    output [7:0] out_byte,
    output done
);
```

<a id="hdl-138"></a>

### HDL-138 Sequence recognition

来源：本地原文（原完整交付引用：`<../references/markdown/b857abe1781f43b7.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/fsm_hdlc)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")Previous

Next[exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")

[Synchronous HDLC framing](https://en.wikipedia.org/wiki/High-Level_Data_Link_Control#Synchronous_framing) involves decoding a continuous bit stream of data to look for bit patterns that indicate the beginning and end of frames (packets). Seeing exactly 6 consecutive 1s (i.e., 01111110) is a "flag" that indicate frame boundaries. To avoid the data stream from accidentally containing "flags", the sender inserts a zero after every 5 consecutive 1s which the receiver must detect and discard. We also need to signal an error if there are 7 or more consecutive 1s.

Create a finite state machine to recognize these three sequences:

- 0111110: Signal a bit needs to be discarded (disc).
- 01111110: Flag the beginning/end of a frame (flag).
- 01111111...: Error (7 or more 1s) (err).

When the FSM is reset, it should be in a state that behaves as though the previous input were 0.

Here are some example sequences that illustrate the desired operation.

Discard 0111110:


```json5
{ signal: [{ name: "clk", wave: "p.........." },
  { name: "in", wave:   "x01....0x..", node:".......a..." },
  { name: "disc", wave: "0.......10.", node:"........b.." },
  { name: "flag", wave: "0.........." },
  { name: "err", wave: "0.........." },
], edge: [ 'a-~>b']
 }
```



Flag 01111110:


```json5
{ signal: [{ name: "clk", wave: "p..........." },
  { name: "in", wave:   "x01.....0x..", node:"........a..." },
  { name: "disc", wave: "0..........." },
  { name: "flag", wave: "0........10.", node:".........b.." },
  { name: "err", wave: "0..........." },
], edge: [ 'a-~>b']
 }
```



Reset behaviour and error 01111111...:


```json5
{ signal: [{ name: "clk", wave: "p.............." },
  { name: "reset", wave:"x10.......|...." },
  { name: "in", wave:   "x.1.......|.0x.", node:"........a...c." },
  { name: "disc", wave: "0.........|...." },
  { name: "flag", wave: "0.........|...." },
  { name: "err",  wave: "0........1|..0.", node:".........b...d." },
], edge: [ 'a-~>b', 'c-~>d']
 }
```



Implement this state machine.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lemmings3](../references/markdown/6b28c15d5960c9f6.md "lemmings3")
- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp") ·

**fsm\_hdlc**

- · [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")

[fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")Previous

Next[exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module(
    input clk,
    input reset,    // Synchronous reset
    input in,
    output disc,
    output flag,
    output err);
```

<a id="hdl-139"></a>

### HDL-139 Q8: Design a Mealy FSM

来源：本地原文（原完整交付引用：`<../references/markdown/d81048db8705209b.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2013_q8)

**实现要求**（保留原题的代码、列表及子问）：

[fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")Previous

Next[exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")

Implement a **Mealy**-type finite state machine that recognizes the sequence "101" on an input signal named **x**. Your FSM should have an output signal, **z**, that is asserted to logic-1 when the "101" sequence is detected. Your FSM should also have an active-low asynchronous reset. You may only have 3 states in your state machine. Your FSM should recognize overlapping sequences.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [lemmings4](../references/markdown/0e4028830111a85a.md "lemmings4")
- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc") ·

**exams/ece241\_2013\_q8**

- · [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")

[fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")Previous

Next[exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input aresetn,    // Asynchronous active-low reset
    input x,
    output z );
```

<a id="hdl-140"></a>

### HDL-140 Q5a: Serial two's complementer (Moore FSM)

来源：本地原文（原完整交付引用：`<../references/markdown/4a89847a77335dfd.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2014_q5a)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")Previous

Next[exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")

You are to design a one-input one-output serial 2's complementer **Moore** state machine.
The input (x) is a series of bits (one per clock cycle) beginning with the least-significant bit of the number, and the output (Z) is the 2's complement of the input. The machine will accept input numbers of arbitrary length. The circuit requires an asynchronous reset. The conversion begins when *Reset* is released and stops when *Reset* is asserted.

For example:


```json5
{signal: [
    {name: "Input (x)", wave:  '0.101.0.'},
    {name: "Output (z)", wave: "0..1.0.1"}
],
 foot: { tock: ['LSB', '', '', '', '', '', '', 'MSB'] }
}
```



### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_onehot](../references/markdown/745013775b0fd13e.md "fsm_onehot")
- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8") ·

**exams/ece241\_2014\_q5a**

- · [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")

[exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")Previous

Next[exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input areset,
    input x,
    output z
);
```

<a id="hdl-141"></a>

### HDL-141 Q5b: Serial two's complementer (Mealy FSM)

来源：本地原文（原完整交付引用：`<../references/markdown/93ddc9a89b50acfe.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/ece241_2014_q5b)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")Previous

Next[exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")

The following diagram is a **Mealy** machine implementation of the 2's complementer.
Implement using one-hot encoding.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/0/05/Ece241_2014_q5b.png`）](https://hdlbits.01xz.net/wiki/File:Ece241_2014_q5b.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_ps2](../references/markdown/a7126c946eeae72d.md "fsm_ps2")
- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a") ·

**exams/ece241\_2014\_q5b**

- · [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")

[exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")Previous

Next[exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input areset,
    input x,
    output z
);
```

<a id="hdl-142"></a>

### HDL-142 Q3a: FSM

来源：本地原文（原完整交付引用：`<../references/markdown/4faf0d1b386afc39.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2014_q3fsm)

**实现要求**（保留原题的代码、列表及子问）：

[exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")Previous

Next[exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")

Consider a finite state machine with inputs *s* and *w*. Assume that the FSM begins in a reset state called *A*,
as depicted below. The FSM remains in state *A* as long as *s* = 0, and it moves to state
*B* when *s* = 1. Once in state *B* the FSM examines the value of the input *w* in the next three
clock cycles. If *w* = 1 in exactly two of these clock cycles, then the FSM has to set an output *z*
to 1 in the following clock cycle. Otherwise *z* has to be 0. The FSM continues checking *w* for
the next three clock cycles, and so on. The timing diagram below illustrates the required values
of *z* for different values of *w*.

Use as few states as possible. Note that the *s* input is used only in state *A*, so you need to consider just the *w* input.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/d/d6/Exams_2014q3fsm.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2014q3fsm.png)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_ps2data](../references/markdown/40f8c235cc74e458.md "fsm_ps2data")
- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b") ·

**exams/2014\_q3fsm**

- · [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")

[exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")Previous

Next[exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,   // Synchronous reset
    input s,
    input w,
    output z
);
```

<a id="hdl-143"></a>

### HDL-143 Q3b: FSM

来源：本地原文（原完整交付引用：`<../references/markdown/1e604bb60027765f.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2014_q3bfsm)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")Previous

Next[exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")

Given the state-assigned table shown below, implement the finite-state machine. Reset should reset the FSM to state 000.

| Present state y[2:0] | Next state Y[2:0] | | Output z |
| --- | --- | --- | --- |
| x=0 | x=1 |
| 000 | 000 | 001 | 0 |
| 001 | 001 | 100 | 0 |
| 010 | 010 | 001 | 0 |
| 011 | 001 | 010 | 1 |
| 100 | 011 | 100 | 1 |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_serial](../references/markdown/c64bb996909dd665.md "fsm_serial")
- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm") ·

**exams/2014\_q3bfsm**

- · [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")

[exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")Previous

Next[exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,   // Synchronous reset
    input x,
    output z
);
```

<a id="hdl-144"></a>

### HDL-144 Q3c: FSM logic

来源：本地原文（原完整交付引用：`<../references/markdown/ad9567c5290d9bd4.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2014_q3c)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")Previous

Next[exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")

Given the state-assigned table shown below, implement the logic functions Y[0] and z.

| Present state y[2:0] | Next state Y[2:0] | | Output z |
| --- | --- | --- | --- |
| x=0 | x=1 |
| 000 | 000 | 001 | 0 |
| 001 | 001 | 100 | 0 |
| 010 | 010 | 001 | 0 |
| 011 | 001 | 010 | 1 |
| 100 | 011 | 100 | 1 |

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_serialdata](../references/markdown/e2edcdc387fa4a18.md "fsm_serialdata")
- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm") ·

**exams/2014\_q3c**

- · [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")

[exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")Previous

Next[exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input [2:0] y,
    input x,
    output Y0,
    output z
);
```

<a id="hdl-145"></a>

### HDL-145 Q6b: FSM next-state logic

来源：本地原文（原完整交付引用：`<../references/markdown/e0adf86c0a853f2d.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/m2014_q6b)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")Previous

Next[exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")

Consider the state machine shown below, which has one input *w* and one output *z*.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/e/e1/Exams_m2014q6.png`）](https://hdlbits.01xz.net/wiki/File:Exams_m2014q6.png)

Assume that you wish to implement the FSM using three flip-flops and state codes *y[3:1] =*
000, 001, ... , 101 for states A, B, ... , F, respectively. Show a state-assigned table for this FSM.
Derive a next-state expression for the flip-flop *y[2]*.

Implement just the next-state logic for *y[2]*. (This is much more a FSM question than a Verilog coding question. Oh well.)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_serialdp](../references/markdown/983e83bf12c1ed42.md "fsm_serialdp")
- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c") ·

**exams/m2014\_q6b**

- · [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")

[exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")Previous

Next[exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input [3:1] y,
    input w,
    output Y2);
```

<a id="hdl-146"></a>

### HDL-146 Q6c: FSM one-hot next-state logic

来源：本地原文（原完整交付引用：`<../references/markdown/b5942dab12b66e2f.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/m2014_q6c)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")Previous

Next[exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")

Consider the state machine shown below, which has one input *w* and one output *z*.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/e/e1/Exams_m2014q6.png`）](https://hdlbits.01xz.net/wiki/File:Exams_m2014q6.png)

For this part, assume that a one-hot code is used with the state assignment 'y[6:1] *= 000001, 000010, 000100, 001000, 010000, 100000 for states A, B,..., F, respectively.*

Write a logic expression for the next-state signals Y2 and Y4.
(Derive the logic equations by inspection assuming a one-hot encoding. The testbench will test with non-one hot inputs to make sure you're not trying to do something more complicated).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [fsm\_hdlc](../references/markdown/b857abe1781f43b7.md "fsm_hdlc")
- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b") ·

**exams/m2014\_q6c**

- · [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")

[exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")Previous

Next[exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input [6:1] y,
    input w,
    output Y2,
    output Y4);
```

<a id="hdl-147"></a>

### HDL-147 Q6: FSM

来源：本地原文（原完整交付引用：`<../references/markdown/cb3f4908bc86ad43.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/m2014_q6)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")Previous

Next[exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")

Consider the state machine shown below, which has one input *w* and one output *z*.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/images/e/e1/Exams_m2014q6.png`）](https://hdlbits.01xz.net/wiki/File:Exams_m2014q6.png)

Implement the state machine. (This part wasn't on the midterm, but coding up FSMs is good practice).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2013\_q8](../references/markdown/d81048db8705209b.md "exams/ece241_2013_q8")
- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c") ·

**exams/m2014\_q6**

- · [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")
- [exams/review2015\_fsmshift](../references/markdown/6ceeed3edd67060a.md "exams/review2015_fsmshift")

[exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")Previous

Next[exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,     // synchronous reset
    input w,
    output z);
```

<a id="hdl-148"></a>

### HDL-148 Q2a: FSM

来源：本地原文（原完整交付引用：`<../references/markdown/fde5f57bce40a68f.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2012_q2fsm)

**实现要求**（保留原题的代码、列表及子问）：

[exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")Previous

Next[exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")

Consider the state diagram shown below.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.85f24157a04c6df5.85f24157a04c6df5.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2012q2.png)

Write complete Verilog code that represents this FSM. Use separate **always** blocks for the state
table and the state flip-flops, as done in lectures. Describe the FSM output, which is called *z*,
using either continuous assignment statement(s) or an **always** block (at your discretion). Assign
any state codes that you wish to use.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2014\_q5a](../references/markdown/4a89847a77335dfd.md "exams/ece241_2014_q5a")
- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6") ·

**exams/2012\_q2fsm**

- · [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")
- [exams/review2015\_fsmshift](../references/markdown/6ceeed3edd67060a.md "exams/review2015_fsmshift")
- [exams/review2015\_fsm](../references/markdown/f9d739d83236fb98.md "exams/review2015_fsm")

[exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")Previous

Next[exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input reset,   // Synchronous active-high reset
    input w,
    output z
);
```

<a id="hdl-149"></a>

### HDL-149 Q2b: One-hot FSM equations

来源：本地原文（原完整交付引用：`<../references/markdown/84b9a324eda71029.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2012_q2b)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")Previous

Next[exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")

The state diagram for this question is shown again below.

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.85f24157a04c6df5.85f24157a04c6df5.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2012q2.png)

Assume that a one-hot code is used with the state assignment
*y[5:0]* = 000001(A), 000010(B), 000100(C), 001000(D), 010000(E), 100000(F)

Write a logic expression for the signal *Y1*, which is the input of state flip-flop *y[1]*.

Write a logic expression for the signal *Y3*, which is the input of state flip-flop *y[3]*.

(Derive the logic equations by inspection assuming a one-hot encoding. The testbench will test with non-one hot inputs to make sure you're not trying to do something more complicated).

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/ece241\_2014\_q5b](../references/markdown/93ddc9a89b50acfe.md "exams/ece241_2014_q5b")
- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm") ·

**exams/2012\_q2b**

- · [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")
- [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")
- [exams/review2015\_fsmshift](../references/markdown/6ceeed3edd67060a.md "exams/review2015_fsmshift")
- [exams/review2015\_fsm](../references/markdown/f9d739d83236fb98.md "exams/review2015_fsm")
- [exams/review2015\_fancytimer](../references/markdown/f3e60c5c9b38f996.md "exams/review2015_fancytimer")

[exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")Previous

Next[exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input [5:0] y,
    input w,
    output Y1,
    output Y3
);
```

<a id="hdl-150"></a>

### HDL-150 Q2a: FSM

来源：本地原文（原完整交付引用：`<../references/markdown/ac84c7f31ae37198.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2013_q2afsm)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")Previous

Next[exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")

Consider the FSM described by the state diagram shown below:

![（原完整交付引用：`../assets/offline/hdlbits.01xz.net/mw/thumb.91a382d26c5260e2.91a382d26c5260e2.png`）](https://hdlbits.01xz.net/wiki/File:Exams_2013q2.png)

This FSM acts as an arbiter circuit, which controls access to some type of resource by three
requesting devices. Each device makes its request for the resource by setting a signal *r[i]* = 1,
where *r[i]* is either *r[1]*, *r[2]*, or *r[3]*. Each r[i] is an input signal to the FSM, and represents one of the
three devices. The FSM stays in state *A* as long as there are no requests. When one or more
request occurs, then the FSM decides which device receives a grant to use the resource and
changes to a state that sets that device’s *g[i]* signal to 1. Each *g[i]* is an output from the FSM. There
is a priority system, in that device 1 has a higher priority than device 2, and device 3 has the
lowest priority. Hence, for example, device 3 will only receive a grant if it is the only device
making a request when the FSM is in state *A*. Once a device, *i*, is given a grant by the FSM, that
device continues to receive the grant as long as its request, *r[i]* = 1.

Write complete Verilog code that represents this FSM. Use separate always blocks for the state
table and the state flip-flops, as done in lectures. Describe the FSM outputs, *g[i]*, using either
continuous assignment statement(s) or an always block (at your discretion). Assign any state
codes that you wish to use.

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/2014\_q3fsm](../references/markdown/4faf0d1b386afc39.md "exams/2014_q3fsm")
- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b") ·

**exams/2013\_q2afsm**

- · [exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")
- [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")
- [exams/review2015\_fsmshift](../references/markdown/6ceeed3edd67060a.md "exams/review2015_fsmshift")
- [exams/review2015\_fsm](../references/markdown/f9d739d83236fb98.md "exams/review2015_fsm")
- [exams/review2015\_fancytimer](../references/markdown/f3e60c5c9b38f996.md "exams/review2015_fancytimer")
- [exams/review2015\_fsmonehot](../references/markdown/e5dcdd479a3b395a.md "exams/review2015_fsmonehot")

[exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")Previous

Next[exams/2013\_q2bfsm](../references/markdown/f79eea316bcddad0.md "exams/2013_q2bfsm")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input resetn,    // active-low synchronous reset
    input [3:1] r,   // request
    output [3:1] g   // grant
);
```

<a id="hdl-151"></a>

### HDL-151 Q2b: Another FSM

来源：本地原文（原完整交付引用：`<../references/markdown/f79eea316bcddad0.md>`） · [unversioned snapshot; edition not asserted 在线原文](https://hdlbits.01xz.net/wiki/exams/2013_q2bfsm)

**实现要求**（保留原题的代码、列表及子问）：

[exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")Previous

Next[exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")

Consider a finite state machine that is used to control some type of motor. The FSM has inputs
*x* and *y*, which come from the motor, and produces outputs *f* and *g*, which control the motor.
There is also a clock input called *clk* and a reset input called *resetn*.

The FSM has to work as follows. As long as the reset input is asserted, the FSM stays in a
beginning state, called state *A*. When the reset signal is de-asserted, then after the next clock
edge the FSM has to set the output *f* to 1 for one clock cycle. **Then**, the FSM has to monitor the
*x* input. When *x* has produced the values 1, 0, 1 in three successive clock cycles, then *g* should
be set to 1 on the following clock cycle. While maintaining *g* = 1 the FSM has to monitor the *y*
input. If *y* has the value 1 within at most two clock cycles, then the FSM should maintain *g* = 1
permanently (that is, until reset). But if *y* does not become 1 within two clock cycles, then the
FSM should set *g* = 0 permanently (until reset).

(The original exam question asked for a state diagram only. But here, implement the FSM.)

### Write your solution here

[Load a previous submission]Load

[Upload a source file...](#) 

### Or upload a file

Show solution

### Solution

- [exams/2014\_q3bfsm](../references/markdown/1e604bb60027765f.md "exams/2014_q3bfsm")
- [exams/2014\_q3c](../references/markdown/ad9567c5290d9bd4.md "exams/2014_q3c")
- [exams/m2014\_q6b](../references/markdown/e0adf86c0a853f2d.md "exams/m2014_q6b")
- [exams/m2014\_q6c](../references/markdown/b5942dab12b66e2f.md "exams/m2014_q6c")
- [exams/m2014\_q6](../references/markdown/cb3f4908bc86ad43.md "exams/m2014_q6")
- [exams/2012\_q2fsm](../references/markdown/fde5f57bce40a68f.md "exams/2012_q2fsm")
- [exams/2012\_q2b](../references/markdown/84b9a324eda71029.md "exams/2012_q2b")
- [exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm") ·

**exams/2013\_q2bfsm**

- · [exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")
- [exams/review2015\_shiftcount](../references/markdown/1231228995cf1381.md "exams/review2015_shiftcount")
- [exams/review2015\_fsmseq](../references/markdown/3561a957235d9109.md "exams/review2015_fsmseq")
- [exams/review2015\_fsmshift](../references/markdown/6ceeed3edd67060a.md "exams/review2015_fsmshift")
- [exams/review2015\_fsm](../references/markdown/f9d739d83236fb98.md "exams/review2015_fsm")
- [exams/review2015\_fancytimer](../references/markdown/f3e60c5c9b38f996.md "exams/review2015_fancytimer")
- [exams/review2015\_fsmonehot](../references/markdown/e5dcdd479a3b395a.md "exams/review2015_fsmonehot")
- [bugs\_mux2](../references/markdown/212b3d2b71cd9e8c.md "bugs_mux2")

[exams/2013\_q2afsm](../references/markdown/ac84c7f31ae37198.md "exams/2013_q2afsm")Previous

Next[exams/review2015\_count1k](../references/markdown/482e2500425db122.md "exams/review2015_count1k")

**交付物**：独立 .v/.sv、testbench、期望生成器/向量、编译/运行日志；在线判题记录可选。

**验收条件**（自验）：以原题文字和图表作独立参考；组合逻辑穷举可承受输入，时序电路覆盖复位、所有可达转移、边界/重叠输入和保持条件；断言比较逐拍输出，不能只用目测波形。 原状态图/时序图每条边分别设置到达与触发用例，确认 Moore/Mealy 的输出时点。

归类：基础路径指定题。

接口原样保留：

```verilog
module top_module (
    input clk,
    input resetn,    // active-low synchronous reset
    input x,
    input y,
    output f,
    output g
);
```
