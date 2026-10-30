from common import *
import csv,re
def main():
    cpp=ROOT/'E/E4/csrc';rtl=ROOT/'E/E4/rtl';data=ROOT/'E/E4/data'
    obj=WORK/'semu.o';semu=WORK/'semu'
    run('cpu/semu_compile',['gcc','-std=c11','-Wall','-Wextra','-Werror','-O2','-g',cpp/'semu.c',cpp/'semu_main.c','-o',semu],inputs=[cpp/'semu.c',cpp/'semu.h',cpp/'semu_main.c'])
    run('cpu/semu_object',['gcc','-std=c11','-Wall','-Wextra','-Werror','-O2','-g','-c',cpp/'semu.c','-o',obj],inputs=[cpp/'semu.c',cpp/'semu.h'])
    sys.path.insert(0,str(ROOT/'F/programs'));from sisa import Machine
    for image,mode in [('f5_sum10',0),('f6_sum10',1),('f6_output',1)]:
        o,e,r=run('cpu/semu_'+image,[semu,data/(image+'.hex'),'200',str(mode)],inputs=[semu,data/(image+'.hex')]);rows=list(csv.reader(o.splitlines()));m=Machine(enhanced=bool(mode));memory=[int(v,16) for v in (data/(image+'.hex')).read_text().split()]
        for row in rows:
            got=list(map(int,row));old=m.pc;ins=memory[old];m.step(ins);assert got[1:]==[old,ins,*m.state()]
        assert m.r[2]==55 and (mode==0 or image!='f6_output' or m.led==m.display==55)
    args=[rtl/'scpu.sv',rtl/'cpu_top.sv'];exe=build('cpu_top',args,cpp/'difftest.cpp','difftest',extra=[obj],trace=False,flags=['-Wno-DECLFILENAME'])
    for label,image,cycles in [('sum',str(data/'f6_output.hex'),200),('random','random',50000)]:
        trace=OUT/'cpu'/('trace_'+label+'.csv')
        o,e,r=run('cpu/diff_'+label,[exe,image,str(cycles),trace],inputs=[exe,obj],timeout=90);assert 'PASS DiffTest' in o
        m=Machine(enhanced=True)
        for line in trace.read_text().splitlines():
            row=list(map(int,line.split(',')));i,old,ins,sw,buttons,rst,*actual=row
            assert m.pc==old;m.step(ins,sw,buttons,reset=bool(rst));assert actual==m.state(),(i,actual,m.state())
        if label=='sum':assert m.led==m.display==55
    for name,macro,needle in [('gpr','FAULT_R0_CONSTANT','pc_before=0x00 instruction=0x86 GPR0 dut=0x00 ref=0x08'),('pc','FAULT_BRANCH_SIGN','pc_before=0x08 instruction=0xf9 PC dut=0x16 ref=0x06')]:
        bad=build('cpu_top',args,cpp/'difftest.cpp','diff_bad_'+name,defines=[macro],extra=[obj],trace=False,flags=['-Wno-DECLFILENAME'])
        o,e,r=run('cpu/negative_'+name,[bad,data/'f6_output.hex','200',OUT/'cpu'/('bad_'+name+'.csv')],inputs=[bad,obj],expected=(1,));assert needle in e,e
        if name=='pc':assert 'GPR' not in e
    result(['E4-M013','E4-M015','E4-M016','E4-M017'],['artifacts/E4/cpu','artifacts/E4/cpu_source.json'],'Real C11 sEMU, native Verilator sCPU, all256 instruction encodings in50000-step deterministic stream and200-step sum; independent prior Python model checks every state; genuine GPR and PC-only RTL mutations rejected at first divergence.')
    print('CPU_DIFFTEST_PASS',flush=True)
if __name__=='__main__':main()
