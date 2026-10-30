"""Deterministic instruction-stream fixtures with independent Python integer results."""
from pathlib import Path
import random,json
ROOT=Path(__file__).resolve().parents[2]
MASK=(1<<32)-1
def signed(x):return x-(1<<32) if x>>31 else x
def main():
    seed=0x2607b401;rng=random.Random(seed);regs=[5,6,7,10,11,12,13,14,15];values={i:rng.getrandbits(32) for i in regs};memory=bytearray(2048)
    lines=['.text','.balign 32','.globl main','.type main,@function','main:','addi sp,sp,-16','sw ra,12(sp)','sw s0,8(sp)','sw s1,4(sp)','la s0,scratch']
    # A long load allows younger independent producers to fill E/D, followed by
    # two writes of the same destination and a consumer of the youngest value.
    lines+=['sw zero,0(s0)','lw a0,0(s0)','addi t0,zero,1','addi t0,zero,2','addi a1,t0,0','li t1,2','bne a1,t1,failed']
    lines += [f'li x{i},0x{values[i]:08x}' for i in regs]
    coverage={}
    for index in range(1200):
        kind=rng.randrange(5);rd,rs1,rs2=[rng.choice(regs) for _ in range(3)]
        if kind<=1:
            op=rng.choice(['add','sub','xor','or','and','sll','srl','sra','slt','sltu']);a,b=values[rs1],values[rs2]
            result={'add':lambda:a+b,'sub':lambda:a-b,'xor':lambda:a^b,'or':lambda:a|b,'and':lambda:a&b,'sll':lambda:a<<(b&31),'srl':lambda:a>>(b&31),'sra':lambda:signed(a)>>(b&31),'slt':lambda:int(signed(a)<signed(b)),'sltu':lambda:int(a<b)}[op]()&MASK
            lines.append(f'{op} x{rd},x{rs1},x{rs2}');values[rd]=result
        elif kind==2:
            op=rng.choice(['addi','xori','ori','andi','slti','sltiu']);imm=rng.randrange(-2048,2048);a=values[rs1]
            result={'addi':lambda:a+imm,'xori':lambda:a^(imm&MASK),'ori':lambda:a|(imm&MASK),'andi':lambda:a&(imm&MASK),'slti':lambda:int(signed(a)<imm),'sltiu':lambda:int(a<(imm&MASK))}[op]()&MASK
            lines.append(f'{op} x{rd},x{rs1},{imm}');values[rd]=result
        elif kind==3:
            size=rng.choice([1,2,4]);offset=(rng.randrange(1024)//size)*size;op={1:'sb',2:'sh',4:'sw'}[size]
            lines.append(f'{op} x{rs1},{offset}(s0)');memory[offset:offset+size]=(values[rs1]&((1<<(8*size))-1)).to_bytes(size,'little')
        else:
            op,size,sign=rng.choice([('lb',1,True),('lbu',1,False),('lh',2,True),('lhu',2,False),('lw',4,False)]);offset=(rng.randrange(1024)//size)*size
            lines.append(f'{op} x{rd},{offset}(s0)');values[rd]=int.from_bytes(memory[offset:offset+size],'little',signed=sign)&MASK
        coverage[op]=coverage.get(op,0)+1
        if index%29==0:
            # A taken forward branch must squash a wrong-path store and illegal instruction.
            lines += [f'beq x{rd},x{rd},skip_{index}','sw s0,1024(s0)','.word 0xffffffff',f'skip_{index}:']
    for j,r in enumerate(regs):lines.append(f'sw x{r},{1040+j*4}(s0)')
    lines+=['lw t0,1024(s0)','bne t0,zero,failed']
    for j,r in enumerate(regs):lines += [f'lw t0,{1040+j*4}(s0)',f'li t1,0x{values[r]:08x}','bne t0,t1,failed']
    for offset in range(0,1024,4):lines += [f'lw t0,{offset}(s0)',f'li t1,0x{int.from_bytes(memory[offset:offset+4],"little"):08x}','bne t0,t1,failed']
    lines += ['li a0,0','j done','failed:','li a0,201','done:','lw s1,4(sp)','lw s0,8(sp)','lw ra,12(sp)','addi sp,sp,16','ret','.size main,.-main','.section .bss',' .balign 16','scratch: .space 2048']
    out=ROOT/'B/B4/programs';out.mkdir(parents=True,exist_ok=True);(out/'hazards.S').write_text('\n'.join(lines)+'\n')
    (out/'hazards.json').write_text(json.dumps({'seed':hex(seed),'random_operations':1200,'coverage':coverage,'expected_registers':values,'memory_hex':memory.hex(),'checks':'Final registers and every word of the1024-byte touched range, plus wrong-path store/illegal instruction squash. No DUT-derived expected values.'},indent=2))
if __name__=='__main__':main()
