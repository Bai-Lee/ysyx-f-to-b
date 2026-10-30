from pathlib import Path
import sys,random,struct,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def u(x):return x&0xffffffff
def s(x):return x if x<0x80000000 else x-0x100000000
def truncdiv(a,b):return (abs(a)//abs(b))*(-1 if (a<0) != (b<0) else 1)
def expected(op,a,b):
    if op=='add':return u(a+b)
    if op=='sub':return u(a-b)
    if op=='sll':return u(a<<(b&31))
    if op=='srl':return a>>(b&31)
    if op=='sra':return u(s(a)>>(b&31))
    if op=='slt':return int(s(a)<s(b))
    if op=='sltu':return int(a<b)
    if op=='xor':return a^b
    if op=='or':return a|b
    if op=='and':return a&b
    if op=='mul':return u(a*b)
    if op=='mulh':return u((s(a)*s(b))>>32)
    if op=='mulhsu':return u((s(a)*b)>>32)
    if op=='mulhu':return u((a*b)>>32)
    if op=='div':return 0xffffffff if not b else u(truncdiv(s(a),s(b)))
    if op=='divu':return 0xffffffff if not b else a//b
    if op=='rem':return a if not b else u(s(a)-truncdiv(s(a),s(b))*s(b))
    if op=='remu':return a if not b else a%b
    raise ValueError(op)

def main():
    lock=json.loads((ROOT/'reports/D3_build.json').read_text());env=lock['runtime_environment'];n=BENCH/'nemu';exe=Path(lock['nemu']);ref=Path(lock['spike']);scope=ROOT/'D/D3';src=scope/'programs';src.mkdir(exist_ok=True);build=WORK/'D3';build.mkdir(exist_ok=True)
    code=['.option norvc','.option norelax','.section .text','.globl _start','_start:'];cases=[]
    def check(lines,got,want,description):
        idx=len(cases)+1;code.extend([f'li a0, {idx}',*lines,f'li t2, 0x{u(want):08x}',f'bne {got}, t2, fail']);cases.append({'id':idx,'description':description,'expected':u(want)})
    values=[0,1,2,31,32,0x7fffffff,0x80000000,0xfffffffe,0xffffffff]
    ops=['add','sub','sll','srl','sra','slt','sltu','xor','or','and','mul','mulh','mulhsu','mulhu','div','divu','rem','remu']
    for op in ops:
        for a in values:
            for b in values:check([f'li t0, 0x{a:08x}',f'li t1, 0x{b:08x}',f'{op} t6,t0,t1'],'t6',expected(op,a,b),f'{op} a={a:#x} b={b:#x}, rd=x31')
    rng=random.Random(0x2607d3)
    for j in range(512):
        op=rng.choice(ops);a=rng.getrandbits(32);b=rng.getrandbits(32)
        check([f'li t0, 0x{a:08x}',f'li t1, 0x{b:08x}',f'{op} t0,t0,t1'],'t0',expected(op,a,b),f'random {op} rd=rs1')
    for a in values:
        for imm in [-2048,-1,0,1,2047]:
            for op,rop in [('addi','add'),('slti','slt'),('sltiu','sltu'),('xori','xor'),('ori','or'),('andi','and')]:
                check([f'li t0, 0x{a:08x}',f'{op} t1,t0,{imm}'],'t1',expected(rop,a,u(imm)),f'{op} sign extension')
        for sh in [0,1,15,31]:
            for op,rop in [('slli','sll'),('srli','srl'),('srai','sra')]:check([f'li t0, 0x{a:08x}',f'{op} t1,t0,{sh}'],'t1',expected(rop,a,sh),f'{op} shamt={sh}')
    check(['addi zero,zero,37','addi t0,zero,5'],'t0',5,'x0 writes discarded')
    check(['lui t0,0xabcde'],'t0',0xabcde000,'LUI low twelve zero')
    code.extend(['auipc t0,0','la t1,pc_label','pc_label:','addi t0,t0,12','bne t0,t1,fail'])
    for op,condition in [('beq',lambda a,b:a==b),('bne',lambda a,b:a!=b),('blt',lambda a,b:s(a)<s(b)),('bge',lambda a,b:s(a)>=s(b)),('bltu',lambda a,b:a<b),('bgeu',lambda a,b:a>=b)]:
        for a,b in [(0,0),(0,1),(1,0),(0x80000000,1),(0xffffffff,0x80000000)]:
            label=f'branch_{len(cases)}';lines=[f'li t0,0x{a:08x}',f'li t1,0x{b:08x}','li t3,0',f'{op} t0,t1,{label}','j '+label+'_done',label+':','li t3,1',label+'_done:']
            check(lines,'t3',int(condition(a,b)),op+' taken/not taken')
    check(['li t0,7','li t1,0','backward_loop:','addi t1,t1,1','addi t0,t0,-1','bne t0,zero,backward_loop'],'t1',7,'negative branch offset')
    code.extend(['jal ra,jump_target','jump_return:','j after_jump','jump_target:','la t0,jump_return','bne ra,t0,fail','la t0,jump_indirect','ori t0,t0,1','jalr t1,0(t0)','jalr_return:','j fail','jump_indirect:','la t0,jalr_return','bne t1,t0,fail','j after_jump','after_jump:'])
    code.extend(['la t0,data','li t1,0x80ff7f01','sw t1,0(t0)'])
    for op,offset,want in [('lb',0,1),('lb',1,127),('lb',2,0xffffffff),('lb',3,0xffffff80),('lbu',2,255),('lh',0,0x7f01),('lh',2,0xffff80ff),('lhu',2,0x80ff),('lw',0,0x80ff7f01)]:check([f'{op} t1,{offset}(t0)'],'t1',want,op+' sign/zero extension')
    check(['li t1,0x55','sb t1,1(t0)','lw t1,0(t0)'],'t1',0x80ff5501,'SB byte isolation')
    check(['li t1,0x1122','sh t1,2(t0)','lw t1,0(t0)'],'t1',0x11225501,'SH byte isolation')
    code.extend(['fence rw,rw','fence.i','li a0,0','ebreak','fail:','ebreak','.section .data','.balign 4','data:','.word 0'])
    asm=src/'rv32im-boundaries.S';asm.write_text('\n'.join(code)+'\n');elf=build/'boundaries.elf';binary=src/'rv32im-boundaries.bin'
    linker=src/'baremetal.ld';linker.write_text('OUTPUT_ARCH(riscv)\nENTRY(_start)\nSECTIONS { . = 0x80000000; .text : { *(.text*) } .rodata : { *(.rodata*) } . = ALIGN(4); .data : { *(.data*) } .bss : { *(.bss*) *(COMMON) } /DISCARD/ : { *(.note*) *(.comment*) } }\n')
    run('D3/isa/compile',['riscv64-linux-gnu-gcc','-march=rv32im_zifencei','-mabi=ilp32','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-Wl,-T,'+str(linker),asm,'-o',elf],inputs=[asm,linker],outputs=[elf],resume=True)
    run('D3/isa/objcopy',['riscv64-linux-gnu-objcopy','-O','binary',elf,binary],inputs=[elf],outputs=[binary],resume=True)
    assert 0<binary.stat().st_size<1024*1024,'unexpected bare-metal image layout'
    o,_,row=run('D3/isa/boundaries',[exe,'-b','-d',ref,binary],cwd=n,env=env,inputs=[exe,ref,binary],timeout=120,resume=True);assert 'HIT GOOD TRAP' in o and 'DIFF_MISMATCH' not in o
    rejects=[]
    for name,words in [('reserved',[0xffffffff]),('rv64_addiw',[0x0010009b]),('bad_shift',[0xfe101093]),('misaligned_jump',[0x0020006f]),('outside_memory',[0x000000b7,0x0000a103]),('cross_ram_end',[0x880000b7,0xffe08093,0x0000a103])]:
        file=src/(name+'.bin');file.write_bytes(struct.pack('<'+'I'*len(words),*words))
        out,err,r=run('D3/isa/reject_'+name,[exe,'-b','-d',ref,file],cwd=n,env=env,inputs=[exe,ref,file],expected=(255,) if name in ('outside_memory','cross_ram_end') else (1,),timeout=30,resume=True)
        assert ('INSTRUCTION_REJECT' in err) if name not in ('outside_memory','cross_ram_end') else ('out of bound' in out+err)
        rejects.append({'name':name,'exit':r['exit_code'],'log':'artifacts/D3/isa/reject_'+name})
    for name,size in [('empty',0),('too_large',0x08000001)]:
        file=build/(name+'.bin')
        with file.open('wb') as f:f.truncate(size)
        _,err,r=run('D3/isa/image_'+name,[exe,'-b','-d',ref,file],cwd=n,env=env,inputs=[exe,ref,file],expected=(2,),timeout=30,resume=True)
        assert 'IMAGE_REJECT' in err
        rejects.append({'name':'image_'+name,'exit':r['exit_code'],'log':'artifacts/D3/isa/image_'+name})
    dump(scope/'programs/cases.json',{'seed':'0x2607d3','cases':cases,'control_flow_and_memory_extra':True})
    dump(ROOT/'reports/D3_isa.json',{'status':'PASS_BOUNDED_TESTS','checks':len(cases),'seed':'0x2607d3','M_operations':['mul','mulh','mulhsu','mulhu','div','divu','rem','remu'],'golden_values':'Independent Python integer arithmetic; actual assembled instructions and every committed register/PC transition also checked by Spike.','negative_controls':rejects,'image_sha256':sha(binary),'nemu_sha256':sha(exe),'spike_sha256':sha(ref),'evidence':'artifacts/D3/isa','runtime_seconds':row['elapsed_seconds']})
    print('D3_ISA_BOUNDARIES_PASS',len(cases),flush=True)

if __name__=='__main__':main()
