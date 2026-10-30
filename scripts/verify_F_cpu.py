"""Compile and run sCPU RTL against an independently written instruction model."""
from evidence import *
import random
sys.path.insert(0,str(ROOT/'F/programs'))
from sisa import Machine,programs,li,io,add,branch

PAT=[0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]
RTL=ROOT/'F/rtl/scpu.sv'
IVER=Path(r'C:\YSYX_WORKSPACE\tools\oss-cad-suite-20261022\oss-cad-suite\bin\iverilog.exe')
VVP=IVER.with_name('vvp.exe')
YOSYS=IVER.with_name('yosys.exe')

def compile_and_run(name,source,defines=(),expected=0,timeout=90):
    folder=ROOT/'F/testbenches';folder.mkdir(exist_ok=True);tb=folder/(name+'.sv');tb.write_text(source,encoding='utf8');exe=ROOT/'temp'/(name+'.vvp')
    compile_cmd=[IVER,'-g2012','-Wall','-s','tb','-o',exe,*['-D'+x for x in defines],RTL,tb]
    c=run('F/rtl_'+name+'_compile',compile_cmd,[RTL,tb],timeout=40)
    if c['status']!='PASS':return {'status':'FAIL','compile':c}
    r=run('F/rtl_'+name,[VVP,exe],[RTL,tb,exe],timeout=timeout,expected=expected)
    return {'status':r['status'],'compile':c,'simulation':r}

def check_expected(text,token):
    if token not in text:raise ValueError('Missing simulator result: '+token)

def semantic_result(name,result,token):
    log=ROOT/'artifacts/F'/('rtl_'+name)/'stdout.log'
    if result['status']=='PASS' and (not log.exists() or token not in log.read_text('utf8')):
        result.update(status='FAIL',reason='Expected semantic result/case count missing: '+token)
    return result

def rom_test():
    rng=random.Random(260701);image=[rng.randrange(256) for _ in range(256)];packed=int.from_bytes(bytes(image),'little')
    refs='\n'.join(f'ref_data[{i}]=8\'h{v:02x};' for i,v in enumerate(image))
    src=f'''module tb;reg[7:0]addr;wire[7:0]data;integer i;reg[7:0]ref_data[0:255];
instruction_rom_mux dut(addr,2048'h{packed:0512x},data);
initial begin {refs}
for(i=0;i<256;i=i+1)begin addr=i;#1;if(data!==ref_data[i])$fatal(1,"ROM address %0d",i);end
$display("PASS ROM addresses=256 width=8");$finish;end endmodule'''
    return semantic_result('rom256x8',compile_and_run('rom256x8',src),'PASS ROM addresses=256 width=8')

def regfile_test():
    src='''module tb;
reg clk=0,reset=1,wen=0;reg[1:0]wa=0,ra=0,rb=0;reg[7:0]wd=0;wire[7:0]a,b;wire[31:0]state;
reg[7:0]model[0:3];integer x,y,z,k,checks=0;
gpr4x8 dut(clk,reset,wen,wa,ra,rb,wd,a,b,state);
initial begin #1;clk=1;#1;clk=0;reset=0;for(k=0;k<4;k=k+1)model[k]=0;
for(x=0;x<4;x=x+1)for(y=0;y<256;y=y+1)begin
wa=x;wd=y;wen=1;#1;clk=1;#1;clk=0;model[x]=y;
for(z=0;z<16;z=z+1)begin ra=z/4;rb=z%4;#1;if(a!==model[ra]||b!==model[rb])$fatal(1,"GPR data");checks=checks+1;end
wen=0;wd=~y;#1;clk=1;#1;clk=0;
if(state!=={model[3],model[2],model[1],model[0]})$fatal(1,"GPR hold");
end
reset=1;#1;clk=1;#1;if(state!==0)$fatal(1,"GPR reset");
$display("PASS GPR read_checks=%0d writes=1024 hold_checks=1024",checks);$finish;end endmodule'''
    return semantic_result('gpr4x8',compile_and_run('gpr4x8',src),'PASS GPR read_checks=16384 writes=1024 hold_checks=1024')

def hex_test():
    refs=''.join(f'ref_data[{i}]=7\'h{v:02x};' for i,v in enumerate(PAT))
    src=f'''module tb;reg[3:0]d;wire[6:0]s;reg[6:0]ref_data[0:15];integer i;hex7 dut(d,s);initial begin {refs}
for(i=0;i<16;i=i+1)begin d=i;#1;if(s!==ref_data[i])$fatal(1,"hex mismatch");end
$display("PASS HEX values=16");$finish;end endmodule'''
    return semantic_result('hex_decode16',compile_and_run('hex_decode16',src),'PASS HEX values=16')

def unit_test(enhanced,stage,samples=32,defines=()):
    name=f'isa_e{int(enhanced)}_s{stage}'+('_'+defines[0].lower() if defines else '')
    path=ROOT/'F/vectors'/(name+'.txt');rng=random.Random(260700+stage+100*int(enhanced));rows=[]
    for ins in range(256):
        for sample in range(samples):
            m=Machine(enhanced,stage,rng.randrange(256),[rng.randrange(256) for _ in range(4)],rng.randrange(256),rng.randrange(256));pre=m.state();sw=rng.randrange(256);bt=rng.randrange(256);m.step(ins,sw,bt);rows.append(pre+[ins,sw,bt]+m.state())
    path.write_text(''.join(' '.join(map(str,row))+'\n' for row in rows),encoding='ascii')
    src=f'''module tb;
reg clk=0,reset=0;reg[7:0]ins=0,sw=0,btn=0;wire[7:0]pc,led,hx;wire[31:0]gpr;wire[6:0]hh,hl;wire iw;wire[2:0]idx;
integer f,rc,n=0,p,r0,r1,r2,r3,l,h,iv,sv,bv,ep,e0,e1,e2,e3,el,eh;
scpu_core #(.ENHANCED({int(enhanced)}),.STAGE({stage})) dut(clk,reset,ins,sw,btn,pc,gpr,led,hx,hh,hl,iw,idx);
initial begin
f=$fopen("{path.as_posix()}","r");if(!f)$fatal(1,"vectors missing");
while(!$feof(f))begin
rc=$fscanf(f,"%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\\n",p,r0,r1,r2,r3,l,h,iv,sv,bv,ep,e0,e1,e2,e3,el,eh);
if(rc!=17)$fatal(1,"vector parse rc=%0d",rc);
clk=0;dut.pc=p;dut.rf.regs[0]=r0;dut.rf.regs[1]=r1;dut.rf.regs[2]=r2;dut.rf.regs[3]=r3;dut.led_storage=l;dut.hex_storage=h;ins=iv;sw=sv;btn=bv;
#2;clk=1;#2;
if(pc!==ep[7:0]||gpr!=={{e3[7:0],e2[7:0],e1[7:0],e0[7:0]}}||led!==el[7:0]||hx!==eh[7:0])begin
$display("MISMATCH unit=%0d prePC=%02x ins=%02x PC got=%02x expected=%02x GPR=%08x expected=%02x%02x%02x%02x",n,p,iv,pc,ep,gpr,e3,e2,e1,e0);$fatal(1,"ISA mismatch");end
n=n+1;
end
$fclose(f);$display("PASS ISA cases=%0d",n);$finish;end endmodule'''
    result=compile_and_run(name,src,defines,expected=1 if defines else 0)
    semantic_result(name,result,'MISMATCH' if defines else f'PASS ISA cases={len(rows)}')
    result.update(cases=len(rows),enhanced=enhanced,stage=stage,vector_sha256=sha(path))
    return result

def firmware_test(name,enhanced,program,stimulus,stage=2,defines=(),expect_final=None):
    fullname=name+('_'+defines[0].lower() if defines else '');image=program+[0]*(256-len(program));packed=int.from_bytes(bytes(image),'little');m=Machine(enhanced,stage);rows=[];trace=[]
    for reset,sw,buttons in stimulus:
        old=m.state();ins=image[m.pc];m.step(ins,sw,buttons,bool(reset));rows.append([reset,sw,buttons]+m.state()+[PAT[m.display>>4],PAT[m.display&15]]);trace.append({'before':old,'instruction':ins,'reset':reset,'switches':sw,'buttons':buttons,'after':m.state()})
    if expect_final:
        for key,value in expect_final.items():
            actual=m.r[int(key[1:])] if key.startswith('r') else getattr(m,key)
            if actual!=value:raise ValueError((name,key,actual,value))
    path=ROOT/'F/vectors'/(fullname+'.txt');path.write_text(''.join(' '.join(map(str,row))+'\n' for row in rows),encoding='ascii');dump(ROOT/'artifacts/F'/(fullname+'_reference.json'),trace)
    art=ROOT/'artifacts/F'/('rtl_'+fullname);art.mkdir(exist_ok=True);vcd=art/'trace.vcd';csv=art/'commits.csv'
    src=f'''module tb;
reg clk=0,reset=1;reg[7:0]sw=0,btn=0;wire[7:0]pc,ins,led,hx;wire[31:0]gpr;wire[6:0]hh,hl;reg[7:0]old_pc,committed_instruction;
integer f,log,rc,n=0,rv,sv,bv,ep,e0,e1,e2,e3,el,eh,ehh,ehl;
scpu_system #(.ENHANCED({int(enhanced)}),.STAGE({stage}),.IMAGE(2048'h{packed:0512x})) dut(clk,reset,sw,btn,pc,ins,gpr,led,hx,hh,hl);
initial begin
$dumpfile("{vcd.as_posix()}");$dumpvars(0,dut);
f=$fopen("{path.as_posix()}","r");log=$fopen("{csv.as_posix()}","w");if(!f||!log)$fatal(1,"file open");
$fwrite(log,"cycle,reset,old_pc,instruction,new_pc,r0,r1,r2,r3,led,hex\\n");
while(!$feof(f))begin
rc=$fscanf(f,"%d %d %d %d %d %d %d %d %d %d %d %d\\n",rv,sv,bv,ep,e0,e1,e2,e3,el,eh,ehh,ehl);if(rc!=12)$fatal(1,"bad vector %0d",rc);
clk=0;reset=rv;sw=sv;btn=bv;#5;old_pc=pc;committed_instruction=ins;clk=1;#1;
if(pc!==ep[7:0]||gpr!=={{e3[7:0],e2[7:0],e1[7:0],e0[7:0]}}||led!==el[7:0]||hx!==eh[7:0]||hh!==ehh[6:0]||hl!==ehl[6:0])begin
$display("MISMATCH cycle=%0d PC=%02x expected=%02x GPR=%08x expected=%02x%02x%02x%02x LED=%02x/%02x HEX=%02x/%02x",n,pc,ep,gpr,e3,e2,e1,e0,led,el,hx,eh);$fatal(1,"firmware mismatch");end
$fwrite(log,"%0d,%0d,%02x,%02x,%02x,%02x,%02x,%02x,%02x,%02x,%02x\\n",n,rv,old_pc,committed_instruction,pc,gpr[7:0],gpr[15:8],gpr[23:16],gpr[31:24],led,hx);
#4;n=n+1;end
$fclose(f);$fclose(log);$display("PASS FIRMWARE {fullname} cycles=%0d pc=%02x r0=%02x r1=%02x r2=%02x r3=%02x led=%02x hex=%02x",n,pc,gpr[7:0],gpr[15:8],gpr[23:16],gpr[31:24],led,hx);$finish;end endmodule'''
    result=compile_and_run(fullname,src,defines,1 if defines else 0)
    semantic_result(fullname,result,'MISMATCH' if defines else f'PASS FIRMWARE {fullname} cycles={len(rows)}')
    result.update(cycles=len(rows),reference_final=m.state(),image_sha256=hashlib.sha256(bytes(image)).hexdigest(),vector_sha256=sha(path),waveform=str(vcd),commits=str(csv),fault=list(defines))
    return result

def main():
    lock=json.loads((ROOT.parents[1]/'config/toolchain.lock.json').read_text('utf8'));fingerprints={}
    for name,path in [('iverilog',IVER),('vvp',VVP),('yosys',YOSYS)]:
        got=sha(path);expected=lock['tools'][name]['sha256'];fingerprints[name]={'path':str(path),'sha256':got,'matches_locked':got==expected}
        if got!=expected:raise ValueError('Tool fingerprint changed: '+name)
    dump(ROOT/'config/F_rtl_tool_fingerprints.json',fingerprints)
    results={};results['rom']=rom_test();results['gpr']=regfile_test();results['hex']=hex_test()
    if any(v['status']!='PASS' for v in results.values()):dump(ROOT/'reports/F_cpu_results.json',results);return 1
    for enh,stage in [(False,0),(False,1),(False,2),(True,2)]:results[f'isa_{int(enh)}_{stage}']=unit_test(enh,stage)
    progs=programs()
    for name,(enh,program) in progs.items():
        (ROOT/'F/programs'/(name+'.hex')).write_text(''.join(f'{v:02x}\n' for v in program+[0]*(256-len(program))),encoding='ascii')
    def stim(n,sw=0,button=0):return [(1,sw,0)]+[(0,sw,button)]*n
    for name,n,stage,final in [('f5_sum10',4,0,{'r0':10,'r1':0,'r2':0,'r3':1}),('f5_sum10',6,1,{'r1':1,'r2':1}),('f5_sum10',80,2,{'r2':55,'pc':7}),('f5_odd10',80,2,{'r2':25,'pc':7}),('f6_sum10',100,2,{'r2':55}),('f6_output',100,2,{'led':55,'display':55})]:
        enh,program=progs[name];case=name+('_li' if stage==0 else '_add' if stage==1 else '');results[case]=firmware_test(case,enh,program,stim(n),stage,expect_final=final)
    for n in [0,1,2,10,22,23,31,127,255]:
        steps=3*(n or 256)+30;v=((n or 256)*((n or 256)+1)//2)&255
        results['switch_'+str(n)]=firmware_test('switch_'+str(n),True,progs['f6_switch_sum'][1],stim(steps,n),expect_final={'led':v,'display':v})
    for bt in [1,2,128,255]:
        pattern=[(1,10,0)]+[(0,10,0)]*100+[(0,10,bt)]*20
        # A separate no-button run proves the display is held at zero first.
        results['wait_'+str(bt)]=firmware_test('wait_'+str(bt),True,progs['f6_button_wait'][1],pattern,expect_final={'led':10,'display':55})
    results['wait_no_button']=firmware_test('wait_no_button',True,progs['f6_button_wait'][1],stim(150,10),expect_final={'led':10,'display':0})
    results['hold_outputs']=firmware_test('hold_outputs',True,progs['f6_output_hold'][1],stim(50),expect_final={'led':3,'display':3,'r2':0})
    results['step_level']=firmware_test('step_level',True,progs['f6_step_level'][1],[(1,0,0)]+[(0,0,0)]*30+[(0,0,1)]*80+[(0,0,0)]*30)
    release_pattern=[(1,0,0)]+[(0,0,0)]*50
    for _ in range(8):release_pattern += [(0,0,1)]*100+[(0,0,0)]*100
    results['step_release']=firmware_test('step_release',True,progs['f6_step_release'][1],release_pattern,expect_final={'led':9,'display':45})
    import csv
    actual=list(csv.DictReader((ROOT/'artifacts/F/rtl_step_release/commits.csv').open(encoding='utf8')))
    for press in range(8):
        start=51+200*press
        if any(int(x['r1'],16)!=press+1 for x in actual[start:start+100]):raise ValueError('Held button advanced before release')
        last=actual[start+199];term=press+2
        if int(last['led'],16)!=term or int(last['hex'],16)!=term*(term+1)//2:raise ValueError('One full release did not advance exactly once')
    results['step_release']['independent_behavior_check']='PASS: each held interval leaves term unchanged; each of eight releases advances exactly one term'
    for fault,program in [('FAULT_BRANCH_SIGN','f6_sum10'),('FAULT_R0_CONSTANT','f5_sum10'),('FAULT_LED_LIVE','f6_output_hold'),('FAULT_LI_SHIFT','f6_sum10')]:
        enh,words=progs[program];results['reject_'+fault]=firmware_test('reject_'+fault,enh,words,stim(100),defines=[fault])
    src='read_verilog -sv '+RTL.as_posix()+'; hierarchy -top instruction_rom_mux; proc; opt; techmap; opt; stat; write_json '+(ROOT/'artifacts/F/rom_mux_netlist.json').as_posix()
    results['synthesis_rom']=run('F/rom_yosys',[YOSYS,'-Q','-p',src],[RTL],timeout=60)
    src='read_verilog -sv '+RTL.as_posix()+'; chparam -set ENHANCED 1 scpu_core; hierarchy -top scpu_core; proc; memory; opt; check -assert; stat; write_json '+(ROOT/'artifacts/F/scpu_enhanced_netlist.json').as_posix()
    results['synthesis_cpu']=run('F/scpu_yosys',[YOSYS,'-Q','-p',src],[RTL],timeout=60)
    result={'status':'PASS' if all(x['status']=='PASS' for x in results.values()) else 'FAIL','seed':2607,'tool_fingerprints':fingerprints,'results':results,'scope':'Functional F-stage sISA implementation, not RISC-V/physical silicon; sequential firmware plus all 256 instruction encodings over seeded arbitrary states; four fault rejection controls'}
    dump(ROOT/'reports/F_cpu_results.json',result);print('F_CPU_RESULT',result['status'],'checks',len(results),flush=True)
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
