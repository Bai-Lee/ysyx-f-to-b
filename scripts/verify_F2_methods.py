from evidence import *
from verify_F_cpu import compile_and_run
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def main():
    # Command-line event stepping replaces the abandoned manual GUI route.
    waveform=(ROOT/'artifacts/F/rtl_tutorial_events/trace.vcd').as_posix();events=(ROOT/'artifacts/F/rtl_tutorial_events/events.csv').as_posix();(ROOT/'artifacts/F/rtl_tutorial_events').mkdir(exist_ok=True)
    src=f'''`timescale 1ns/1ps
module tb;reg e=0,reset=1;wire inv,pulse;reg q;integer log;
not #(1) inverter(inv,e);and #(1) both(pulse,e,inv);
always @(posedge pulse or posedge reset)if(reset)q<=0;else q<=1;
initial begin $dumpfile("{waveform}");$dumpvars(0,tb);log=$fopen("{events}","w");$fwrite(log,"time,e,not_e,pulse,q\\n");
#4;reset=0;#6;e=1;#5;
if(pulse!==0||q!==1)$fatal(1,"Propagation pulse was not captured");
$display("PASS EVENT_TRACE final_pulse=0 captured_q=1");$fclose(log);$finish;end
always @(e or inv or pulse or q)if(log)$fwrite(log,"%0t,%b,%b,%b,%b\\n",$time,e,inv,pulse,q);
endmodule'''
    result=compile_and_run('tutorial_events',src)
    if result['status']!='PASS':return 1
    rows=(ROOT/'artifacts/F/rtl_tutorial_events/events.csv').read_text('utf8').splitlines()
    if not any(',1,0,1,' in x or ',1,1,1,' in x for x in rows):raise ValueError('No actual transient event logged')
    tool=Path(r'C:\YSYX_WORKSPACE\tools\logisim-evolution-4.0.0');manual=tool/'doc/en/html';review=[]
    for sub in ['guide/tutorial','guide/gui','guide/menu']:
        for p in sorted((manual/sub).glob('*.html')):
            text=BeautifulSoup(p.read_bytes(),'lxml').get_text(' ',strip=True);review.append({'file':str(p),'sha256':sha(p),'text':text})
    for name in ['button','dipswitch','led','7seg','hexdig']:
        p=manual/'libs/io'/(name+'.html')
        if p.exists():review.append({'file':str(p),'sha256':sha(p),'text':BeautifulSoup(p.read_bytes(),'lxml').get_text(' ',strip=True)})
    dump(ROOT/'F/analysis/tool_manual_review.json',review)
    cfg=json.loads((ROOT/'config/toolchain.json').read_text('utf8'));cp=str(ROOT/'temp/java-classes')+';'+cfg['logisim']['jar'];sources=list((ROOT/'scripts/java').glob('*.java'));compiled=run('F2/compile_native_driver',[str(Path(cfg['java']['executable']).with_name('javac.exe')),'-encoding','UTF-8','-cp',cp,'-d',ROOT/'temp/java-classes',*sources],sources,timeout=30)
    if compiled['status']!='PASS':return 1
    prefix=[cfg['java']['executable'],'-Xmx256m','-Djava.awt.headless=true','-Duser.language=en','-Djava.util.prefs.PreferencesFactory=LocalPrefsFactory','-cp',cp,'CircuitRunner'];vec=ROOT/'F/vectors/tutorial_wire_check.txt';vec.write_text('X Y Z\n0 0 0\n0 1 1\n1 0 1\n1 1 0\n',encoding='ascii')
    # Never reopen the mutable GUI work file. Create a fresh, immutable fault
    # fixture from the good circuit, and bypass all autosave recovery in Java.
    tree=ET.parse(ROOT/'F/circuits/tutorial_reference_complete.circ');circuit=tree.getroot().find('circuit');removed=0
    for w in list(circuit.findall('wire')):
        if set(w.attrib.values())=={'(550,200)','(650,200)'}:circuit.remove(w);removed+=1
    if removed!=1:raise ValueError('Missing-output fault injection did not remove exactly one wire')
    tree.write(ROOT/'F/circuits/tutorial_missing_output_fault.circ',encoding='UTF-8',xml_declaration=True)
    native=[]
    for filename,expected in [('tutorial_reference_complete.circ',0),('tutorial_missing_output_fault.circ',1)]:
        p=ROOT/'F/circuits'/filename;q=run('F2/'+p.stem,prefix+[p,'tutorial_gui',vec],[p,vec],timeout=30,expected=expected);native.append(q)
    if not all(x['status']=='PASS' for x in native):return 1
    if 'MISMATCH' not in (ROOT/'artifacts/F2/tutorial_missing_output_fault/stdout.log').read_text('utf8'):raise ValueError('Bad circuit was not actually rejected')
    note='''# F2：工具、教程与输入输出

用户已明确允许灵活采用现有工具，并要求停止 computer-use 操作 Logisim。之后没有继续任何 Logisim GUI 操作；F5/F6 使用可综合 RTL。已有 `.circ` 的原生引擎结果保留。

|六段教程|本轮具体交付与操作方式|
|---|---|
|0 定位界面|实际启动4.0.0窗口；辨认左侧工程/元件树、属性表、画布、菜单和工具栏；后续GUI按用户要求停止|
|1 放置逻辑门|独立生成2个NOT、2个AND和1个OR的XOR结构，保存为可打开的原生circ|
|2 连线|原生电路真实仿真；GUI停止前曾实际补接输出线；最终采用程序生成的完整文件，并以缺线文件作负对照|
|3 文字|原生输入/输出标签；GUI停止前曾实际输入真值表标注，但未把未保存的界面编辑冒充磁盘交付|
|4 测试|四种X/Y组合在真实Logisim引擎校验，LED真实组件端口同步检查；缺输出线的错误文件被拒绝|
|5 逐事件观察|Icarus传播延迟示意模型生成CSV与VCD：e与其延后反相短暂同时为1，静态恒零的 e∧¬e 出现瞬态并让DFF置1|

最后一项的1ns仅用于示意事件排序，不代表任何实际标准单元或工艺延迟。瞬态模型与稳定布尔真值表的边界不同，不能把它当芯片时序签核。

## 图形界面及菜单阅读

官方手册随版本JAR提取，阅读清单/原文哈希在 `../analysis/tool_manual_review.json`。画布编辑负责元件和正交连线；属性表区分工具下一次创建的默认属性与已选中元件属性；工程树管理层次。File用于新建、打开、保存/另存和导出，Edit用于编辑与撤销，Project用于电路/库，Simulate用于仿真、复位、时钟和传播步进，Window/Help用于窗口与帮助。正式工具运行均使用项目内的内存偏好后端，未改用户全局设置。

本轮最终交付可由生成入口与命令行重现；没有宣称在用户停止GUI后继续手点各菜单。GUI程序生成和人工操作的区别在此明确保留。

## I/O元件的引脚和极性

Button有1位输出，按下1、释放0。DipSwitch默认8个独立1位输出，每一位是保持型开关；要接8位总线需要合并，不能把它当瞬时Button。4.0.0随包的 `dipswitch.html` 部分文字误用了Button描述，因此已进一步查阅该版本 `std_io_DipSwitch.java`，并由原生组件检查确认number=8及8个输出端口；没有照抄误文。

LED输入1位，高有效时1亮；7-Segment有a–g和dp共8个输入，实际端口次序已逐位验证。十六进制显示器接受4位数字，可关闭dp。两位Hex显示收到8位数55时呈37，不是十进制55。F5/F6代码保留独立输出寄存器，输入是外部给定状态，不伪造为输出存储。

自行设计的 `parity_alarm` 对四位开关计算奇校验并驱动LED，全部16种输入已在真实引擎验证；这是F2-M005交付。普通二输入AND的正确/错误期望值也已用于工具预检。
'''
    (ROOT/'F/notes/F2_工具与教程.md').write_text(note,encoding='utf8')
    dump(ROOT/'reports/F2_results.json',{'status':'PASS_ADAPTED','authorization':'User explicitly waived Logisim and prohibited further computer-use Logisim operation','event_simulation':result,'native_complete_and_missing_wire_controls':native,'manual_documents':len(review),'gui_claim':'Opened and attempted wiring/text before stop instruction; unsaved GUI edits are not claimed as delivered files','delivered_method':'Programmatic .circ creation plus actual native engine tests; command-line RTL event stepping, source/manual review; no continued GUI automation'})
    print('F2_METHODS_RESULT PASS_ADAPTED',flush=True)
    return 0
if __name__=='__main__':sys.exit(main())
