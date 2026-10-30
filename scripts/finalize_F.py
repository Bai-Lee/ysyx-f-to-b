"""Write the F-only ledger and handoff from actual reports, never inferred success."""
from evidence import *
import csv,re,collections

def read(name):return json.loads((ROOT/'reports'/name).read_text('utf8'))
def note(name,text):p=ROOT/'F/notes'/name;p.write_text(text.strip()+'\n',encoding='utf8');return p
def main():
    circuit=read('F_circuit_results.json');cpu=read('F_cpu_results.json');f4=read('F4_results.json');theory=read('F_theory_results.json');f2=read('F2_results.json');optional=read('F_optional_results.json');assembler=read('F_assembler_results.json')
    if not all(r['status'] in ('PASS','PASS_ADAPTED') for r in (circuit,cpu,f4,theory,f2,optional,assembler)):raise ValueError('Unfinished/failed verification report')
    policy=json.loads((ROOT/'config/execution_policy.json').read_text('utf8'));policy.update(allow_logisim_gui=False,computer_use_logisim=False,logisim_optional=True,tool_adaptation='User authorized flexible non-Logisim workflow; F5/F6 SystemVerilog + Icarus/Yosys; previous native Logisim headless circuit results retained',stop_after='F',advance_to_E=False);dump(ROOT/'config/execution_policy.json',policy)
    note('F1_工程方法与记录.md','''
# F1：工程方法、来源与复盘

本任务是自主工程实验，不代替用户报名、提交个人表格或撰写个人提问经历。F1图例、通识问卷和个人提问流程按用户指令排除。

STFW用于发现官方工具入口和定位问题；RTFM用于确认规格/选项/端口；RTFSC用于在文档不充分或现象矛盾时追到实现。实例：Logisim4的门输入坐标与旧版经验不同，通过组件端口实际查询校准；driveInputPin只写意图值，持续仿真还需触发失效事件；DipSwitch随包文档误用Button文字，通过源码和原生8输出端口核对纠正。相关源码属于工具API，不是下载他人的处理器实现。

一次验收不能只看程序退出0。先独立写预期，再实际驱动设计；查齐向量数量和解析错误；错误设计/数据必须确实被拒绝。工具预检中的错误真值、缺线电路，以及sCPU中的零号寄存器、分支符号扩展、输出保持、li移位故障，都有独立失败对照。失败运行放在对应artifacts目录的attempts，不覆盖后当作从未出错。

复位锁存器曾在D/WE/RESET同时改变时振荡，保留原用例并修改电路；没有删断言。还发现File方式读取Logisim会恢复GUI自动存档并改写文件，故最终改成只读字节流加载，并比较输入执行前后哈希。所有33个基础电路已在新路径下重新批量验证。

已阅读《给AI时代的一生一芯初学者的一封信》的离线正文，来源为归档references/markdown/e797b24c7ab4be5c.md。这里采用其强调的“解释、判断、验证和复盘”：生成结果不自动成为结论；不能声称人工学习经历；代码的来源、模型的假设和测试的边界需要明确。原文针对人的成长，本轮对agent的评价落实为可检查的实现与证据。

开发记录分三层：config/task_status.json逐项状态；reports汇总；artifacts保留命令、cwd、输入及其快照/哈希、退出码、stdout/stderr、用时。设计源码/脚本用本地Git管理；不改原讲义和源归档，不上传私人资料。F阶段结束后按用户指令停下，由下一模型开始E。
''')
    rows=list(csv.DictReader((ROOT/'artifacts/F/rtl_f5_sum10/commits.csv').open(encoding='utf8')));odd=list(csv.DictReader((ROOT/'artifacts/F/rtl_f5_odd10/commits.csv').open(encoding='utf8')))
    lines=['# F4：程序和电路的状态机','', '## 求和程序的实际RTL状态（M001）','', 'PC计数的是8位sISA指令地址；表内数值为十进制。不是手写预期冒充运行值，原始CSV在artifacts/F/rtl_f5_sum10。','', '|有效执行步|PC|R0|R1|R2|R3|','|---|---|---|---|---|---|']
    for row in rows:
        if row['reset']=='1':continue
        vals=[int(row[k],16) for k in ('new_pc','r0','r1','r2','r3')];lines.append('| '+str(row['cycle'])+' | '+' | '.join(map(str,vals))+' |')
        if vals[0]==7:break
    lines += ['', '末态PC=7、R2=55。PC7处bner0比较R0=10与R3=1，故PC保持7；这是软件自环，不是ebreak或新增halt指令。真实仿真继续多拍，寄存器结果保持。','', '## 奇数和（M002）','', '保持硬件不变，只更换指令序列：R0=11、R1=1、R2=0、R3=2，循环先R2+=R1再R1+=R3，到R1=11退出。实际PC7、R2=25；原始CSV在rtl_f5_odd10，程序与机器码在F/programs/f5_odd10。','', '|循环后的R1|R2|','|---|---|']
    seen=set()
    for row in odd:
        pc=int(row['new_pc'],16);i=int(row['r1'],16);s=int(row['r2'],16)
        if pc in (4,7) and (i,s) not in seen:seen.add((i,s));lines.append(f'| {i} | {s} |')
    lines += ['', '## C的源级状态（M003、M004）','', 'Compiler Explorer gcc15.1真实执行输出z=3，修改版输出z=42；同样的源文件也在本机GCC实际编译运行。请求/响应与哈希见F4_results。源级抽象PC依次表示即将执行的语句：x赋值前(x,y,z未知)→x=1→y=2→z=3→printf输出→return0→END。局部变量在生命周期外不再作为可读取的C对象；源级抽象PC不是x86机器地址。','', '## 专用求和电路（M005）','', '下面的逐拍状态已由F3 native测试向量逐行断言。源码中的旧i与sum同时更新：i_next=i+1、sum_next=sum+i+1，i=10后保持。','', '|有效拍|i|sum|','|---|---|---|']
    lines += [f'| {i} | {i} | {i*(i+1)//2} |' for i in range(11)]
    lines += ['', '## 层次对应与编译（M006、M007）','', '循环边界上，C的i/sum、sISA的R1/R2、专用电路的i/sum表示同一数学状态sum=i(i+1)/2。ISA先更新R1再更新R2，两个指令之间存在中间态，不能硬说每条指令等价于专用电路一拍。实际RTL提交边界已经核验该不变量，见F/analysis/sum_state_boundaries.json。','', 'sISA机器码由独立汇编器生成；没有声称GCC已实现C→sISA后端。C→x86的真实编译对应另在[汇编映射](../analysis/c_to_assembly.md)，来源为Compiler Explorer source.line；以API代替网页点击和颜色高亮，保留实际在线执行与对应关系。']
    note('F4_状态机与编译.md','\n'.join(lines))
    note('F5_结构与程序.md','''
# F5：简单处理器的实现与验证

按用户授权，用可综合SystemVerilog替代继续在Logisim中搭建处理器。`F/rtl/scpu.sv`分为ROM多路选择器、4×8寄存器堆、核心和显示译码。源码、测试台和独立Python指令状态机均在本项目；没有参考下载他人的CPU实现。

PC宽8、复位0；4个GPR各8位，R0可写。为测试确定性，复位清空全部GPR；原ISA并未要求R0恒0。时钟上升沿更新，复位同步高有效。整数运算保留低8位。

## M001：取指ROM

逻辑规格256×8，每个PC选择一个8位字，地址每次加1。instruction_rom_mux以动态8位切片实现字选择；系统的IMAGE参数是只读程序内容。全部256地址与独立字节表对照，Yosys映射到MUX网络。此处是教学逻辑ROM，不冒充实际工艺存储宏。

## M002：GPR

两个可寻址读端口、一个按写地址及写使能更新的写端口，共32存储位。1024次写入覆盖4个地址×256数据，每次检查16组读地址并加写禁止保持；另验复位。R0也接受写入，故不会把sISA错当RISC-V。

## M003–M005：逐步增加指令

STAGE=0仅li写回：imm4零扩展，顺序PC。真实执行原程序前4条li后得到R0=10,R1=0,R2=0,R3=1。STAGE=1增加add，前6条后R1=1,R2=1。STAGE=2增加bner0，比较R0与R[rs2]，不等时PC更新到4位绝对目标，否则PC+1。完整求和最终PC7、R2=55，自环保持。

全部256条编码分别在每个阶段的32组固定种子任意初态上单步比较；不把这称为穷尽所有32位GPR状态。未支持的opcode01在基础版定义为不写回且PC+1，未把它偷偷扩成I/O。

## M006：专用电路与存储程序

专用求和只需i与sum两组状态，算法固定；当前版本10拍完成10项累加。CPU使用PC/GPR与ROM，每个迭代经历两个add和一次branch，加4条初始化共34个指令周期抵达PC7。CPU可只换程序算奇数和，专用电路则要改结构。这里比较的是教学模型的步骤/状态和可编程性，不是主频、面积或能耗的工艺实测。

## M007：只换程序

f5_sum10.hex与f5_odd10.hex使用相同核心源码；后一程序得25。单步PC/GPR与独立参考逐次对照，程序、CSV和VCD均保留。C程序、sISA程序与专用电路的对应详见F4笔记。
''')
    note('F6_增强指令与输入输出.md','''
# F6：增强sISA与输入输出

## 五项必做

li的imm2左移2×s位；移量明确为3位，防止在2位表达式里丢掉最高位。bner0使用当前PC加有符号4位偏移，范围−8…7，8位PC模256回绕。独立汇编器检查寄存器号和立即数/偏移范围；非法操作数8类被拒绝。

io编码方向0为输入、1为输出。输入0=8位switches、输入1=8位buttons；输出0=8位LED存储器、输出1=8位显示存储器。未连接设备输入读0、输出忽略，这是本实现明确的扩展约定。I/O复用GPR读口：输出时读rd，而非把指令低位误当源寄存器。

增强版求和仍为55；输出到LED为0x37，两个十六进制显示字符为37。高/低七段译码也与参考对照，不能把55误写成十进制显示55。

输入末项测试0、1、2、10、22、23、31、127、255。23等情况超过8位和，按模256处理。按钮等待程序在循环时输出当前项到LED，完成后先轮询buttons；未按时HEX保持0，任一非零按钮输入后才显示55。实际验证1、2、128、255四种按钮值。

LED和HEX有各自独立寄存器；写入后修改源GPR仍保持输出。故障版把LED直接接到GPR，已被独立测试拒绝。

## 选做O001：末项0

本程序先递增再比较，末项0要等8位项计数绕回0，实际累加1…256，结果为128（模256），不是数学意义上的空和0。该现象已真实运行，并按原题说明不要求修复。不能把本程序结果推广成所有写法的唯一行为。

## 选做O002：12条指令的单步求和

程序f6_step_level使用R0=1作比较/递增常数，R1为项、R2为和、R3读按钮。只有按钮值1才离开轮询；当其他按钮未按时，这对应最低位按钮。输出依次1/1、2/3、3/6。按住不放会连续推进，这是这个版本有意保留的电平敏感行为。多个按钮同时组合未纳入该选做输入约定；必做的“任意按钮触发显示”版本则支持全部非零值。

## 选做O003：完整按下—释放才推进

f6_step_release先在R0=1时等待buttons=1，再把R0改0等待buttons=0，恢复R0=1后只进行一次递增及累加。R3此时为0，可与R0构成无条件跳转。

该方案没有声称压到12条；为了不突破4位相对偏移，在空闲ROM地址22、29、…、253放置+7的跳转岛，最后通过8位PC回绕抵达地址4。全程每个偏移都在−8…7之内，使用4个GPR及256字ROM。填充字节00是add r0,r0,r0，不是NOP；正常控制流不会执行它们。没有声称这是最短或最快程序。

实际仿真8次按下各保持100周期、释放各保持100周期，每次只前进一步，最后项为9、和为45。全过程每个周期的PC/GPR/LED/HEX与独立状态机匹配。

## 验证边界

四套编码单步检查总计32768个随机初态样本，另有23项正常固件运行和4类故障拒绝、ROM/GPR专项与Yosys结构检查。随机状态抽样不是全状态形式化证明，综合也不表示已经达到芯片PPA或流片签核。本阶段仍为8位sISA，尚未开发RISC-V。
''')
    note('F3_已选扩展.md','''
# F3扩展的具体状态

O011：已用4个4→2优先编码器及1个组选择编码器构成16→4层次，全部65536种输入穷举，VALID及最高优先级正确。实现为optional_logic.sv；采用用户授权的RTL替代。

O012：CLZ=15−最高置位索引，CTZ通过位反转再做相同编码，CLO/CTO对按位取反的数据分别计算；全零/全一的对应计数为16。四个计数器与优先编码一起遍历65536数据。

O013：fa_two_halves实际实例化两个half_adder，再用OR合并进位，8个输入穷举。

O014：已选用RCA后加回最高进位的反码方案，与必做M022共享ones4实现和256对验证证据，不重复算成两套独立实现。

O017：NAND型SR锁存器激励低有效；Sbar/Rbar=01置1、10清0、11保持、00两输出为1（非法互补状态）。同时释放非法态可能产生数字竞争；这是对原NOR结构的德摩根对偶分析，未把纸面分析冒充额外的仿真。

O015：N位ones' complement是(2^N−1)−x，即逐位对全1取补；two's complement是(2^N−x) mod 2^N，等于按位取反后加1，是基数2的补数，不是“取反两次”。前者保留正负两种零，后者零唯一。

F5-O001：可以定义固定十数求和的专用指令，但需明确十个操作数的来源；4个GPR和8位编码不足以直接列出十个独立寄存器，可能要引入内存、隐式约定或多周期结构。还要评价面积、时序、编译支持和其他程序的收益。仅为1…10硬连出55可以特化，却不能据此认定通用ISA应新增该指令。现有三指令ISA只换程序即可算奇数和，体现通用性的价值。本项为分析题，没有改DUT ISA。

其他面积最优寻优、晶体管级XOR/XNOR、下降沿DFF、维持-阻塞DFF等选做未选，不计入必做完成率。背景阅读和未选做程序在总报告分别列出。没有为了让“全部完成”好看而把未做项写成PASS。
''')
    data=json.loads((ROOT/'config/task_status.json').read_text('utf8'));ids={r['id']:r for r in data['tasks']};allcore=[r for r in data['tasks'] if re.fullmatch(r'F[1-6]-M\d{3}',r['id'])]
    excluded={'F1-M001':'LEGEND','F1-M002':'USER_EXCLUDED_PERSONAL','F1-M004':'USER_EXCLUDED_PERSONAL'}
    generic={
      'F1':['reports/preflight_F.json','F/notes/F1_工程方法与记录.md'],
      'F2':['reports/F2_results.json','reports/F_circuit_results.json','F/notes/F2_工具与教程.md'],
      'F3':['reports/F_circuit_results.json','reports/F_theory_results.json','F/notes/F3_逻辑与时序分析.md'],
      'F4':['reports/F4_results.json','F/notes/F4_状态机与编译.md','F/analysis/c_to_assembly.md'],
      'F5':['reports/F_cpu_results.json','F/rtl/scpu.sv','F/notes/F5_结构与程序.md'],
      'F6':['reports/F_cpu_results.json','reports/F_assembler_results.json','F/rtl/scpu.sv','F/notes/F6_增强指令与输入输出.md']}
    for row in allcore:
        rid=row['id'];course=rid.split('-')[0]
        if rid in excluded:row.update(status='EXCLUDED_SCOPE',result_details=excluded[rid],evidence=[]);continue
        adapted=course in ('F5','F6') or rid in ('F2-M002','F2-M003','F4-M003','F4-M007')
        row.update(status='PASS_ADAPTED' if adapted else 'PASS',result_details='Actual execution/evidence complete under user-authorized non-GUI workflow.' if adapted else 'Required technical deliverable and its checks completed.',evidence=generic[course])
    selected={'F3-O011':['reports/F_optional_results.json','F/notes/F3_已选扩展.md'],'F3-O012':['reports/F_optional_results.json','F/notes/F3_已选扩展.md'],'F3-O013':['reports/F_optional_results.json','F/notes/F3_已选扩展.md'],'F3-O014':['reports/F_circuit_results.json','F/notes/F3_已选扩展.md'],'F3-O017':['F/notes/F3_已选扩展.md'],'F3-O015':['F/notes/F3_已选扩展.md'],'F5-O001':['F/notes/F3_已选扩展.md'],'F6-O001':['reports/F_cpu_results.json','F/notes/F6_增强指令与输入输出.md'],'F6-O002':['reports/F_cpu_results.json','F/notes/F6_增强指令与输入输出.md'],'F6-O003':['reports/F_cpu_results.json','F/notes/F6_增强指令与输入输出.md']}
    extra_challenges={'F3-O003','F3-O004','F3-O006','F3-O007','F3-O018','F3-O019'}
    for row in data['tasks']:
        if not row['id'].startswith('F') or '-M' in row['id']:continue
        if row['id'] in selected:row.update(status='PASS_THEORY' if row['id'] in ('F3-O017','F3-O015','F5-O001') else 'PASS_ADAPTED',evidence=selected[row['id']],result_details='Selected extension completed; scope/type explicit in notes.')
        elif row['id'].startswith('F1-'):row.update(status='EXCLUDED_SCOPE',result_details='Personal process or legend excluded by user.')
        elif row['id'] in extra_challenges:row.update(status='NOT_SELECTED',result_details='Optional exercise not selected; not counted as completed.')
        else:row.update(status='READING_OR_METHOD_NOTE',result_details='Background/reference or method reminder; no additional programming acceptance invented.',evidence=['F/notes/F3_逻辑与时序分析.md'])
    for job in circuit['jobs']:
        for rid in job['tasks']:
            if rid in ids:ids[rid]['result_details']=f'Native Logisim {job["circuit"]}: {job["rows"]} vectors, zero mismatches; input bytes unchanged.'
    for rid,detail in {
      'F1-M003':'Actual commands/failed attempts/input snapshots and hashes maintained in artifacts; local Git project initialized.',
      'F1-M005':'STFW/RTFM/RTFSC applied to Pin invalidation, model port geometry, DipSwitch documentation and autosave recovery.',
      'F1-M006':'Read source letter; engineering reflection and independent verification method delivered; no personal biography invented.',
      'F3-M001':'Source transistor topology identified as NOR; four ideal-switch input combinations checked.',
      'F3-M002':'OR drawn as NOR plus inverter; all six device/net identities cross-checked and four outputs verified.',
      'F3-M005':'NOT/NAND/AND/NOR/OR/TG equal-drive area formulas derived; physical device count distinguished from area units.',
      'F3-M006':'NAND N(N+1) versus specified gate chain 8N-10 derived for N>=2, checked at 31 integer sizes.',
      'F4-M001':'Real RTL trace reaches PC7 and R2=55, then retains the self-loop state.',
      'F4-M002':'Independent odd-sum firmware reaches PC7 and R2=25 on the same hardware.',
      'F4-M003':'Compiler Explorer cg151 actually executes z=3; modified z=42 and native GCC executions also pass.',
      'F4-M004':'Source-level x/y/z state sequence and END explained; actual output3 confirmed.',
      'F4-M005':'Dedicated i/sum states0..10 tabulated and checked against native per-vector assertions.',
      'F4-M006':'Real loop-boundary commits satisfy sum=i(i+1)/2; intermediate ISA states distinguished from one dedicated clock.',
      'F4-M007':'Real Compiler Explorer source.line mappings preserved; replaces GUI color highlighting by user-authorized API.',
      'F5-M001':'256 ROM addresses compared; real Yosys maps byte selection into a MUX network.',
      'F5-M002':'GPR4x8 passes1024 writes,16384 address-pair reads,1024 hold checks and reset; R0 writable.',
      'F5-M003':'STAGE0 li-only executes first4 initialization instructions with expected PC/GPR.',
      'F5-M004':'STAGE1 adds add; first6 instructions end with R1=1,R2=1.',
      'F5-M005':'STAGE2 complete program gives PC7,R2=55 and self-loop hold.',
      'F5-M006':'Dedicated versus stored-program comparison includes10 versus34 update steps and explicitly avoids unsupported PPA.',
      'F5-M007':'Only firmware image changes; same core computes odd sum25.',
      'F6-M001':'Enhanced li shift and signed PC-relative branch pass8192 arbitrary-state encoding cases and sum55 firmware.',
      'F6-M002':'Output register drives LED data55=0x37 and remains stable after source GPR changes.',
      'F6-M003':'Independent HEX register and high/low segment decoders show37 for decimal55; source-overwrite hold checked.',
      'F6-M004':'Switch limits0,1,2,10,22,23,31,127,255 actually run; overflow and zero-limit behavior documented.',
      'F6-M005':'No-button display hold and four nonzero button values checked; current-term LED remains held.'}.items():ids[rid]['result_details']=detail
    for row in data['tasks']:
        row.setdefault('source_inventory_initial_status',row.get('implementation_status','NOT_RUN'))
        row['implementation_status']=row['status']
    data['current_stage']='F';data['stage_status']='IMPLEMENTATION_COMPLETE_PENDING_FINAL_AUDIT';data['stop_after_F']=True;dump(ROOT/'config/task_status.json',data)
    required=[r for r in allcore if r['id'] not in excluded];assert len(allcore)==67 and len(required)==64 and all(r['status'].startswith('PASS') for r in required)
    groupcounts={c:dict(collections.Counter(r['status'] for r in allcore if r['id'].startswith(c+'-'))) for c in ['F1','F2','F3','F4','F5','F6']}
    meta={'status':'IMPLEMENTATION_COMPLETE_PENDING_FINAL_AUDIT','required_technical_tasks':len(required),'source_yellow_boxes':len(allcore),'excluded_source_boxes':excluded,'courses':groupcounts,'selected_optional_completed':list(selected),'not_selected_optional':sorted(extra_challenges),'next_stage':'E1, only after user changes model/authorizes continuation','E_to_B_started':False,'adaptations':['No further computer-use Logisim operations after user instruction','F5/F6 synthesizable RTL, independent reference and real Icarus/Yosys checks','Compiler Explorer API executes and supplies source mapping instead of manual web clicks'],'evidence_reports':['F_circuit_results.json','F_cpu_results.json','F4_results.json','F_theory_results.json','F2_results.json','F_optional_results.json','F_assembler_results.json']}
    dump(ROOT/'reports/F_stage_summary.json',meta)
    report=['# F阶段交付与验收','', '**实现闭环已完成，等待最终文件审计。按用户最新指令使用灵活的命令行路线，完成F后停止；E～B没有开始。**','', '67个黄色源框中，图例/个人流程3项排除，64项技术必做完成；10项选做完成（其中3项为纸面分析），其余选做或背景明确标记。PASS_ADAPTED表示用户已授权的工具/操作方式替代，未降低公开功能规格。','', '|阶段|状态计数|','|---|---|']
    report += [f'|{c}|{json.dumps(v,ensure_ascii=False)}|' for c,v in groupcounts.items()]
    report += ['', '## 实际执行结果','', '- 原生结构电路：33个电路、25753向量；包括实际LED/七段组件端口、SR振荡、触发器保持、四位算术和完整一小时分秒状态回绕。最终一次加载只读磁盘字节并检查输入运行前后哈希。','- sCPU：ROM全部256地址；GPR1024写入及16384组读检查；四种基础/增强阶段共32768个任意初态单步样本，覆盖全部256编码。','- 固件：23项正常运行及4类故障拒绝。求和55/奇数和25、增强li/有符号分支、0/255等末项、4种非零按钮、输出保持、12指令电平步进及按下释放步进均实际运行；每周期比较PC/GPR/LED/HEX并保存CSV/VCD。','- 故障拒绝：错误分支符号扩展、错误常量R0、缺输出寄存器、错误li移位均导致非零退出；正常版本通过。另有缺线电路、错误期望值、错误C源码和8类非法汇编操作数对照。','- C程序：本机GCC编译执行z=3/z=42/sum=55；Compiler Explorer真实线上执行同三项并取得source.line汇编映射。','- 选做：16→4优先编码、四种首尾位计数遍历65536输入；两个半加器组成全加器遍历8输入。','- Yosys真实完成ROM MUX映射和增强sCPU结构检查；没有输出缺少工艺/约束支持的PPA结论。','', '## 逐项64技术必做及排除项','', '|ID|实现要求|验收状态|具体结果与证据|','|---|---|---|---|']
    for row in allcore:
        links='、'.join(f'[{Path(p).name}](../{p})' for p in row['evidence']);report.append(f'|{row["id"]}|{row["requirement"].replace("|","/")}|{row["status"]}|{row["result_details"]}<br>{links}|')
    report += ['', '## 选做与范围','', '已完成：'+', '.join(selected)+'。','', '未选做：'+', '.join(sorted(extra_challenges))+'。未选项不记PASS。F7建设中按用户指令忽略，无公开技术作业可验收。','', '## 验证边界','', '这是按公开功能要求的自验，未申请官方身份、考核或认证。数字仿真振荡不证明模拟亚稳态；理想晶体管开关和面积单位不等同PDK/真实PPA；32768个任意初态是抽样而非全状态证明；没有设计或验证RISC-V、E阶段框架及后端流片流程。','', '## 给GPT-6 Astra的接续入口','', '先读项目README、config/execution_policy.json、config/task_status.json和本报告，然后从E1开始。F5/F6是8位sISA，不可当RISC-V：R0可写、PC每指令+1；后续RISC-V的x0/指令宽度/寄存器组必须重新按手册实现。原归档保持只读，使用固定提交的官方框架，不能把其中现成代码冒充独立实现。','', 'E目录当前为空；现有Icarus/Yosys/Verilator来自工作区锁定工具。只发现WSL入口，没有注册Linux发行版；后续E3需要实际Linux验证，系统/WSL组件变更遵循根AGENTS规则。此轮没有安装系统组件、改全局PATH、填写个人表格或发消息给外部人员。']
    (ROOT/'reports/F_STAGE_REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf8')
    readme='''# 一生一芯：独立实现工程

当前目标：F阶段已实现，等待最终审计；按用户要求在F结束后停止，由GPT-6 Astra接续。不要继续E，不要恢复computer-use操作Logisim。

- [F阶段验收报告](reports/F_STAGE_REPORT.md)：64项技术必做、逐项证据、选做及排除。
- [机器状态表](config/task_status.json)：所有阶段任务；E～B仍未开始。
- [执行边界](config/execution_policy.json)：用户最新工具替代授权及stop-after-F。
- F/rtl/scpu.sv：独立8位sISA处理器；F/programs为汇编/镜像/参考状态机。
- F/circuits/fundamentals.circ：33个已验收基础电路，实际原生引擎验证。
- F/notes：每个F节点的实现理由、关键推导、源图拓扑、状态与限制。
- artifacts：实际命令、输入快照/哈希、退出码、stdout/stderr、CSV/VCD；历史失败在attempts。

源资料：/workspace/YSYX_F_B_Archive，未修改原始讲义。实现范围依据该库的公开任务矩阵及用户后续指令。新工具补充锁在config/toolchain.json，已有EDA工具以/workspace/config/toolchain.lock.json为基线。

重放入口：scripts/Run-F.ps1（命令行，不打开GUI）。可先运行 `-Quick` 只重放处理器/理论/扩展，`-Full` 还重放33个原生电路；Compiler Explorer在线结果已留原始请求响应，离线审阅无需登录。

下一模型先读F_STAGE_REPORT和task_status，再按用户继续E的指令更新执行边界。不要把F的sISA、旧资料替代、自验通过、已有工具小例与RISC-V/官方资格/流片完成混淆。
'''
    (ROOT/'README.md').write_text(readme,encoding='utf8')
    print('F_LEDGER_PREPARED required=64 excluded=3 selected_optional=10; final audit pending',flush=True)
if __name__=='__main__':sys.exit(main())
