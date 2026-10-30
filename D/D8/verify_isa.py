from pathlib import Path
import sys,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'D3'))
from common import *
from verify_isa import expected as isa_expected

def main():
    d=ROOT/'D/D8';out=d/'results';out.mkdir(exist_ok=True);build=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(build['executable']);ref=Path(build['reference'])
    code=['.option norvc','.option norelax','.section .text.start,"ax"','.globl _start','_start:'];cases=[]
    def check(steps,register,value,label):
        code.extend([f'li a0,{len(cases)+1}',*steps,f'li t2,0x{value&0xffffffff:08x}',f'bne {register},t2,fail']);cases.append({'description':label,'expected':value&0xffffffff})
    values=[0,1,2,31,32,0x7fffffff,0x80000000,0xfffffffe,0xffffffff];ops=['add','sub','sll','srl','sra','slt','sltu','xor','or','and']
    for op in ops:
        for a in values:
            for b in values:check([f'li t0,0x{a:08x}',f'li t1,0x{b:08x}',f'{op} a5,t0,t1'],'a5',isa_expected(op,a,b),f'{op} {a:#x},{b:#x}')
    rng=random.Random(0x2607d8)
    for _ in range(512):
        op=rng.choice(ops);a=rng.getrandbits(32);b=rng.getrandbits(32)
        check([f'li t0,0x{a:08x}',f'li t1,0x{b:08x}',f'{op} t0,t0,t1'],'t0',isa_expected(op,a,b),'random '+op+' rd=rs1')
    for a in values:
        for imm in [-2048,-1,0,1,2047]:
            for op,refop in [('addi','add'),('slti','slt'),('sltiu','sltu'),('xori','xor'),('ori','or'),('andi','and')]:
                check([f'li t0,0x{a:08x}',f'{op} a5,t0,{imm}'],'a5',isa_expected(refop,a,imm&0xffffffff),op+' immediate')
        for sh in [0,1,15,31]:
            for op,refop in [('slli','sll'),('srli','srl'),('srai','sra')]:check([f'li t0,0x{a:08x}',f'{op} a5,t0,{sh}'],'a5',isa_expected(refop,a,sh),op+' shamt')
    for i in range(1,16):
        if i in (7,10):continue
        check([f'li x{i},{i*73}'],f'x{i}',i*73,'all accessible registers')
    check(['addi zero,zero,127','addi a5,zero,0'],'a5',0,'x0 stays zero')
    check(['lui a5,0xabcde'],'a5',0xabcde000,'LUI')
    code.extend(['here:','auipc t0,0','la t1,here','bne t0,t1,fail'])
    signed=lambda a:a if a<0x80000000 else a-0x100000000
    for op,condition in [('beq',lambda a,b:a==b),('bne',lambda a,b:a!=b),('blt',lambda a,b:signed(a)<signed(b)),('bge',lambda a,b:signed(a)>=signed(b)),('bltu',lambda a,b:a<b),('bgeu',lambda a,b:a>=b)]:
        for a,b in [(0,0),(0,1),(1,0),(0xffffffff,1),(0x80000000,0x7fffffff)]:
            label='taken_'+str(len(cases))
            check([f'li t0,0x{a:08x}',f'li t1,0x{b:08x}','li a5,0',f'{op} t0,t1,{label}','j '+label+'_end',label+':','li a5,1',label+'_end:'],'a5',int(condition(a,b)),op+' direction')
    check(['li t0,9','li a5,0','loop:','addi a5,a5,1','addi t0,t0,-1','bne t0,zero,loop'],'a5',9,'backward loop')
    code.extend(['jal ra,direct','return_from_direct:','j after_jump','direct:','la t0,return_from_direct','bne ra,t0,fail','la t0,indirect','ori t0,t0,1','jalr s0,0(t0)','return_from_indirect:','j fail','indirect:','la t0,return_from_indirect','bne s0,t0,fail','j after_jump','after_jump:'])
    code.extend(['la t0,data','li t1,0x80ff7f01','sw t1,0(t0)'])
    for op,offset,want in [('lb',0,1),('lb',1,127),('lb',2,0xffffffff),('lb',3,0xffffff80),('lbu',2,255),('lh',0,0x7f01),('lh',2,0xffff80ff),('lhu',2,0x80ff),('lw',0,0x80ff7f01)]:check([f'{op} a5,{offset}(t0)'],'a5',want,op+' extension')
    check(['li t1,0x55','sb t1,1(t0)','lw a5,0(t0)'],'a5',0x80ff5501,'SB preserves other lanes')
    check(['li t1,0x1122','sh t1,2(t0)','lw a5,0(t0)'],'a5',0x11225501,'SH preserves other lanes')
    check(['li t0,0x87ffffff','li t1,0x5a','sb t1,0(t0)','lbu a5,0(t0)'],'a5',0x5a,'last RAM byte')
    code.extend(['fence rw,rw','li a0,0','ebreak','fail:','ebreak','.section .data','.balign 4','data: .word 0'])
    source=out/'rv32e-boundaries.S';source.write_text('\n'.join(code)+'\n');elf=out/'rv32e-boundaries.elf';binary=out/'rv32e-boundaries.bin';ld=ROOT/'D/D7/baremetal.ld';report=out/'rv32e-boundaries.json'
    run('D8/isa/compile',['riscv64-linux-gnu-gcc','-march=rv32e','-mabi=ilp32e','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-T',ld,source,'-o',elf],inputs=[source,ld],outputs=[elf])
    run('D8/isa/objcopy',['riscv64-linux-gnu-objcopy','-O','binary',elf,binary],inputs=[elf],outputs=[binary])
    run('D8/isa/boundaries',[exe,'--image',binary,'--ref',ref,'--report',report],inputs=[exe,ref,binary],outputs=[report],timeout=180)
    result=json.loads(report.read_text());assert result['result']=='GOOD_TRAP' and result['diff_checked']==result['instructions'] and result['device_sync_checked']==0
    dump(out/'boundary_expectations.json',{'seed':'0x2607d8','cases':cases})
    dump(ROOT/'reports/D8_isa.json',{'status':'PASS_BOUNDED_TESTS','case_count':len(cases),'seed':'0x2607d8','result':result,'binary_sha256':sha(binary),'elf_sha256':sha(elf),'scope':'Finite independent Python expectations plus NEMU per-commit comparison. Not a proof for every RV32E input or privileged behavior.'})
    print('RV32E_BOUNDARIES_PASS',len(cases),flush=True)

if __name__=='__main__':main()
