"""Evidence-backed paper exercises and bounded ideal-switch topology checks."""
from evidence import *
from itertools import product
import xml.etree.ElementTree as ET

NETWORK=[
 {'id':'P_A','type':'p','gate':'A','a':'VDD','b':'MID'},
 {'id':'P_B','type':'p','gate':'B','a':'MID','b':'Ybar'},
 {'id':'N_A','type':'n','gate':'A','a':'Ybar','b':'GND'},
 {'id':'N_B','type':'n','gate':'B','a':'Ybar','b':'GND'},
 {'id':'P_INV','type':'p','gate':'Ybar','a':'VDD','b':'Y'},
 {'id':'N_INV','type':'n','gate':'Ybar','a':'Y','b':'GND'}]

def switch_sim(devices,a,b):
    known={'VDD':1,'GND':0,'A':a,'B':b};nets={d[k] for d in devices for k in ('a','b')}
    for iteration in range(12):
        parent={n:n for n in nets}
        def find(n):
            while parent[n]!=n:n=parent[n]
            return n
        for d in devices:
            value=known.get(d['gate'])
            if value is not None and value==(1 if d['type']=='n' else 0):parent[find(d['a'])]=find(d['b'])
        if find('VDD')==find('GND'):raise ValueError('Supply short in ideal topology')
        updated={**known}
        for n in nets:
            updated[n]=1 if find(n)==find('VDD') else 0 if find(n)==find('GND') else None
        if updated==known:return updated
        known=updated
    raise ValueError('Switch model did not settle')

def write_or_svg():
    # All device/net identities are also machine readable for topology audit.
    svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','viewBox':'0 0 760 430','width':'1064','height':'602'})
    ET.SubElement(svg,'rect',{'width':'760','height':'430','fill':'white'})
    def line(x1,y1,x2,y2):ET.SubElement(svg,'line',{'x1':str(x1),'y1':str(y1),'x2':str(x2),'y2':str(y2),'stroke':'#111','stroke-width':'2'})
    def text(x,y,t):ET.SubElement(svg,'text',{'x':str(x),'y':str(y),'font-family':'sans-serif','font-size':'16'}).text=t
    text(25,25,'F3-M002: NOR + inverter = OR (independent drawing)');line(180,50,600,50);text(340,43,'VDD');line(130,350,650,350);text(340,375,'GND')
    positions={'P_A':(230,90),'P_B':(230,160),'N_A':(160,280),'N_B':(300,280),'P_INV':(560,110),'N_INV':(560,280)}
    for d in NETWORK:
        x,y=positions[d['id']];g=ET.SubElement(svg,'g',{'id':d['id'],'data-type':d['type'],'data-gate':d['gate'],'data-net-a':d['a'],'data-net-b':d['b']})
        ET.SubElement(g,'line',{'x1':str(x),'y1':str(y-20),'x2':str(x),'y2':str(y+20),'stroke':'black','stroke-width':'4'})
        ET.SubElement(g,'line',{'x1':str(x-18),'y1':str(y-15),'x2':str(x-18),'y2':str(y+15),'stroke':'black','stroke-width':'2'})
        ET.SubElement(g,'line',{'x1':str(x-75),'y1':str(y),'x2':str(x-18),'y2':str(y),'stroke':'black','stroke-width':'2'})
        if d['type']=='p':ET.SubElement(g,'circle',{'cx':str(x-24),'cy':str(y),'r':'5','fill':'white','stroke':'black','stroke-width':'2'})
        text(x+12,y,d['id']);text(x-80,y-9,d['gate'])
    line(230,50,230,70);line(230,110,230,140);text(255,130,'MID');line(230,180,230,220)
    line(160,220,300,220);line(160,220,160,260);line(300,220,300,260);line(160,300,160,350);line(300,300,300,350)
    line(230,220,430,220);text(340,212,'Ybar');line(430,110,430,280);line(430,110,485,110);line(430,280,485,280)
    line(560,50,560,90);line(560,130,560,260);line(560,300,560,350);line(560,220,700,220);text(650,212,'Y = A OR B')
    text(25,410,'Ideal ON/OFF connectivity only; no PDK, voltage gain, speed or power assertion.')
    p=ROOT/'F/analysis/OR_CMOS.svg';ET.indent(svg);ET.ElementTree(svg).write(p,encoding='utf8',xml_declaration=True)
    read=ET.parse(p).getroot();items={e.attrib['id']:e for e in read if e.tag.endswith('g')}
    for d in NETWORK:
        e=items[d['id']]
        assert all(e.attrib['data-'+k]==d[v] for k,v in [('type','type'),('gate','gate'),('net-a','a'),('net-b','b')])
    return p

def main():
    rows=[]
    for a,b in product(range(2),repeat=2):
        n=switch_sim(NETWORK,a,b)
        assert n['Ybar']==int(not(a or b)) and n['Y']==int(a or b)
        rows.append({'A':a,'B':b,'NOR':n['Ybar'],'OR':n['Y'],'internal_mid':n['MID']})
    negative=[(a,b) for a,b in product(range(2),repeat=2) if switch_sim(NETWORK,a,b)['Ybar']!=int(a or b)]
    assert negative # a NOR output cannot be mislabeled as OR
    graph=ROOT/'F/analysis/transistor_networks.json';dump(graph,{'source_image':'/workspace/YSYX_F_B_Archive/assets/offline/ysyx.oscc.cc/slides/2306/resources/img/tikz-images/27009d95075bd53667312a60e43c65d288ac0557.png','observed_source_topology':'Two pMOS in series, two nMOS in parallel: NOR. OR adds an inverter.','devices':NETWORK,'checks':rows,'negative_or_without_inverter_counterexamples':negative,'model':'Boolean ideal switches. Gate input threshold, charge retention, body effect, parasitics and metastability not modeled.'})
    svg=write_or_svg()
    areas={'not':2,'nand2':6,'and2':8,'nor2':6,'or2':8,'transmission_gate':2,'xor_4nand_implementation':24,'xor_cell_assumed_in_lesson':6,'half_adder_cell_model':14,'full_adder_cell_model':36,'ordinary_encoder4to2_two_outputs':16,'priority_encoder4to2_two_outputs':26}
    assert areas['full_adder_cell_model']==2*areas['half_adder_cell_model']+areas['or2']
    proof=[{'N':n,'transistor_level_area':n*n+n,'specified_gate_chain_area':8*n-10} for n in range(2,33)]
    dump(ROOT/'F/analysis/area_models.json',{'unit':'equivalent minimum transistor area units under the lesson equal-drive model; not square micrometres','values':areas,'nand_N_formulas':proof,'physical_OR_MOS_devices':6,'OR_equal_drive_area_units':8,'full_adder_logic':'Two XOR macros, two AND gates and one OR: 2*6+2*8+8=36. F3-M003 is a different four-NAND XOR implementation costing24; do not substitute its cost while claiming36.','encoder_scope':'VALID optional output excluded from both area comparisons; native priority circuit has additional validity logic.'})
    note='''# F3：逻辑、拓扑与时序分析

## 原图与晶体管结构（M001、M002）

已逐节点查看原图：P1、P2 串联构成上拉，N1、N2 并联构成下拉，两对栅分别接 A/B，Y 是公共输出。只有 A=B=0 时上拉通、下拉断，原图是 NOR。真值表及理想开关连通性检查在 `../analysis/transistor_networks.json`。自绘 OR 图为 [OR_CMOS.svg](../analysis/OR_CMOS.svg)：NOR 后接 CMOS 反相器，附每个器件的端网标识。SVG 元数据与分析网表逐项核对；绘图本身不替代连通性验证。

|A|B|原图 NOR|新增反相器后的 OR|
|---|---|---|---|
|0|0|1|0|
|0|1|0|1|
|1|0|0|1|
|1|1|0|1|

理想开关模型仅判断导通网络，不含工艺模型和真实电压、增益、功耗、延迟。NOR 冒充 OR 的负对照已被真值表拒绝。

## 面积模型（M003、M005、M006、M013、M018）

按讲义的对等驱动近似，以最小晶体管面积为1：NOT=2；二输入 NAND 的两个串联 nMOS 各计2、并联 pMOS 各计1，因此 NAND=6；NOR 对偶地把串联 pMOS 加宽，仍为6。AND=NAND+NOT=8；OR=NOR+NOT=8；传输门 TG=2。OR 实际器件个数为6，等效面积单位为8，不能混用。

N输入 NAND 的直接晶体管方案为 N 个并联 pMOS（共N）及 N 个串联、各宽N的 nMOS（共N²），面积 N²+N。用 N−2 个二输入 AND 加最后一个 NAND 的特定门级方案为 8(N−2)+6=8N−10（N≥2）；N=1 是 NOT=2。N=2时均6，N=3时12/14，N=5时均30。该比较限定这两种方案，不声称全局最优或具体纳秒延迟。

独立搭建的 XOR 用4个 NAND，成本24；XNOR 在其后加 NOT。全加器采用讲义允许的优化 XOR 单元模型（每个6）、两个 AND 和一个 OR，面积2×6+2×8+8=36；两组 XOR/AND 分别构成半加器。不能把四 NAND 版本的成本24代入后仍声称全加器36。

普通4→2编码器在单热输入域内：Y1=I3∨I2，Y0=I3∨I1，面积16。高位优先编码：Y1=I3∨I2，Y0=I3∨(¬I2∧I1)，面积26。比较不含两者可选的 VALID；实现文件里的额外 VALID 逻辑不偷算成零面积。全加器的8项真值表由 native Logisim `full_adder` 穷举校验；进位为 AB∨Cin(A⊕B)，和为 A⊕B⊕Cin。

## 编码、显示与多路选择（M007–M017）

2→4译码器由 NOT/AND 构造；3→8实例化两个自建2→4子电路，并用高位选择屏蔽。16→4普通编码器只在单热域验收，未把全零/多热任意结果伪装成优先编码。4→2优先编码器穷举全部16输入并另给VALID。3位4选1由三级2选1结构组成，全部16384组合通过。每个输入都是3位数据，选择信号是2位。

七段位序 bit0…7=a,b,c,d,e,f,g,dp，均高有效。十进制10–15仅dp亮；十六进制10–15为A,b,C,d,E,F。native 7-Segment Display 的真实端口逐位读取，与SEG总线一起验收，避免总线值正确而显示引脚接错。相等比较器256对输入与LED实际端口同时核对。

## 加法器、减法器和数制（M019–M023）

四位无符号加法输出低4位与carry；减法采用 A+(¬B)+1，BORROW=¬carry。所有256对分别穷举，并核对三组十六进制显示与标志LED。

原码四位含1符号+3数值位。异号先比较绝对值再相减，同号数值相加。超出±7时置OV，数值低3位及符号按文档约定输出；数学结果不可表示时不宣称四位数仍是真值。零统一为+0，额外七段只在有效负结果显示负号。

反码加法先四位相加，再把最高进位加回低位，保留反码双零的原始编码。补码加法的V=(a符号=b符号)∧(结果符号≠a符号)，与无符号carry分开；同号超出[-8,7]才溢出。对应256对输入全部通过。

## 锁存器、触发器与竞争（M024–M033）

NOR型 SR：S=1/R=0置1，S=0/R=1清0，S=R=0保持；S=R=1令两输出均0，随后同时释放在本Logisim模型中确实触发OSC。该现象只是数字事件模型的振荡，不是硅器件模拟亚稳态证据。

第一种 D 锁存器用 S=D∧WE、R=¬D∧WE 消除正常输入下的非法SR激励。WE=1时Q=D，WE=0时Q保持，与D无关。原图第二种 NAND 方案 Sbar=¬(D∧WE)、Rbar=¬(Sbar∧WE)，在WE=0时二者均1保持，在WE=1时输出D。两套结构都跑过顺序输入/保持测试。

复位锁存器采用 S=D∧WE∧¬RESET、R=(¬D∧WE)∨RESET，RESET高优先。初版独立门控低有效激励在D/WE/RESET同时变化时产生竞争，实际测试发现OSC；已改为在高有效SR激励中统一处理复位。原失败用例保留，不通过删除断言规避。最终全套回归通过。

把Q取反反馈给透明锁存器，在WE打开后形成无稳定点的奇数反相环，确实触发OSC。主从D触发器的主锁存器在CLK低时透明、从锁存器在CLK高时透明，稳定输入下只在上升沿传递状态；高电平保持期间改变D不会跟随。反馈Q取反到D后，每个有效沿翻转一次。使能版本用 Dnext=EN?D:Q 反馈保持，复位优先。

## 寄存器、计数器、求和与时钟（M034–M037）

四位寄存器由自建触发器组成，遍历16写入值、保持及复位。四位计数器逐沿加一，15→0回绕。专用求和电路使用8位i和sum，每拍若i≠10则 i←i+1、sum←sum+(i+1)，旧状态同时更新；第10次有效沿得到i=10,sum=55并保持。

分秒时钟用四个BCD位：秒个位模10、秒十位模6、分个位模10、分十位模6，各级进位使能。数字显示的是十进制00:00…59:59。实际native仿真遍历一整小时及回绕，未用十六进制3B冒充59。测试中的一个有效沿定义为一秒，不是宿主墙钟校时或真实晶振验收。

## 证据入口

`../../reports/F_circuit_results.json` 包含33电路、25753向量的实际Logisim结果；`../../artifacts/F/circuit_*/` 是逐电路命令、输入快照和日志。所有电路在 `../circuits/fundamentals.circ`。GUI流程已按用户最新指令停止；这些是命令行原生引擎结果。
'''
    (ROOT/'F/notes/F3_逻辑与时序分析.md').write_text(note,encoding='utf8')
    dump(ROOT/'reports/F_theory_results.json',{'status':'PASS','ideal_switch_cases':4,'negative_counterexamples':negative,'area_identities_checked':True,'nand_formula_samples':len(proof),'graph_sha256':sha(graph),'svg_sha256':sha(svg),'notes_sha256':sha(ROOT/'F/notes/F3_逻辑与时序分析.md'),'scope':'Declared Boolean switch/area models plus source-image topology and native functional simulation evidence. No real PDK or physical PPA.'})
    print('F_THEORY_RESULT PASS',flush=True)
if __name__=='__main__':main()
