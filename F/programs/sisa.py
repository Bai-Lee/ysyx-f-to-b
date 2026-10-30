"""Independent sISA assembler/reference state machine. Not a processor RTL model."""
from dataclasses import dataclass,field
import json
from pathlib import Path

def regcheck(*indices):
    if any(not isinstance(x,int) or not 0<=x<4 for x in indices):raise ValueError('GPR index must be 0..3')
def li(rd,value,enhanced=False):
    regcheck(rd)
    if not enhanced:
        if not 0<=value<=15:raise ValueError('li imm4 out of range')
        return 0x80|(rd<<4)|value
    for shift in range(4):
        for imm in range(4):
            if imm<<(shift*2)==value:return 0x80|(rd<<4)|(shift<<2)|imm
    raise ValueError('value is not one enhanced li immediate')
def add(rd,rs1,rs2):
    regcheck(rd,rs1,rs2);return (rd<<4)|(rs1<<2)|rs2
def branch(rs2,target,relative=False):
    regcheck(rs2)
    if not ((-8<=target<=7) if relative else (0<=target<=15)):raise ValueError('branch field out of range')
    return 0xc0|((target&15)<<2)|rs2
def io(rd,direction,index):
    regcheck(rd)
    if direction not in (0,1):raise ValueError('IO direction must be 0 or 1')
    if not 0<=index<8:raise ValueError(index)
    return 0x40|(rd<<4)|(direction<<3)|index

@dataclass
class Machine:
    enhanced:bool=False
    stage:int=2
    pc:int=0
    r:list=field(default_factory=lambda:[0]*4)
    led:int=0
    display:int=0
    def reset(self):self.pc=0;self.r=[0]*4;self.led=self.display=0
    def step(self,insn,switches=0,buttons=0,reset=False):
        if reset:self.reset();return
        op=insn//64;rd=(insn//16)%4;old=self.r.copy();nxt=(self.pc+1)%256
        if op==2:
            self.r[rd]=(insn%16) if not self.enhanced else (insn%4)*4**((insn//4)%4)
        elif op==0 and self.stage>=1:self.r[rd]=(old[(insn//4)%4]+old[insn%4])%256
        elif op==3 and self.stage>=2 and old[0]!=old[insn%4]:
            field=(insn//4)%16
            nxt=(self.pc+(field if field<8 else field-16))%256 if self.enhanced else field
        elif op==1 and self.enhanced:
            index=insn%8
            if (insn//8)%2==0:self.r[rd]=(switches if index==0 else buttons if index==1 else 0)%256
            elif index==0:self.led=old[rd]
            elif index==1:self.display=old[rd]
        self.pc=nxt
    def state(self):return [self.pc,*self.r,self.led,self.display]

def programs():
    f5=[li(0,10),li(1,0),li(2,0),li(3,1),add(1,1,3),add(2,2,1),branch(1,4),branch(3,7)]
    odd=[li(0,11),li(1,1),li(2,0),li(3,2),add(2,2,1),add(1,1,3),branch(1,4),branch(3,7)]
    e=lambda rd,val:li(rd,val,True)
    b=lambda rs,offset:branch(rs,offset,True)
    setup=[e(0,8),e(3,2),add(0,0,3),e(1,0),e(2,0),e(3,1)]
    f6=setup+[add(1,1,3),add(2,2,1),b(1,-2),b(3,0)]
    f6out=setup+[add(1,1,3),add(2,2,1),b(1,-2),io(2,1,0),io(2,1,1),b(3,0)]
    switch=[io(0,0,0),e(1,0),e(2,0),e(3,1),add(1,1,3),add(2,2,1),b(1,-2),io(2,1,0),io(2,1,1),b(3,0)]
    wait=[io(0,0,0),e(1,0),e(2,0),e(3,1),add(1,1,3),add(2,2,1),io(1,1,0),b(1,-3),e(0,0),io(1,0,1),b(1,2),b(3,-2),io(2,1,1),b(3,0)]
    hold=[e(0,0),e(2,3),io(2,1,0),io(2,1,1),e(2,0),e(1,1),b(1,0)]
    step=[e(0,1),e(1,1),e(2,1),e(3,0),io(1,1,0),io(2,1,1),io(3,0,1),b(3,-1),add(1,1,0),add(2,2,1),e(3,0),b(3,-7)]
    release=[e(0,1),e(1,1),e(2,1),io(1,1,0),io(2,1,1),io(3,0,1),b(3,-1),e(0,0),io(3,0,1),b(3,-1),e(0,1),add(1,1,0),add(2,2,1),io(1,1,0),io(2,1,1),b(3,7)]
    release += [0]*(256-len(release))
    for at in range(22,254,7):release[at]=b(3,7)
    assert list(range(22,254,7))[-1]==253 # final +7 wraps to address 4
    return {'f5_sum10':(False,f5),'f5_odd10':(False,odd),'f6_sum10':(True,f6),'f6_output':(True,f6out),'f6_switch_sum':(True,switch),'f6_button_wait':(True,wait),'f6_output_hold':(True,hold),'f6_step_level':(True,step),'f6_step_release':(True,release)}

def disassemble(insn,enhanced=False):
    op=insn>>6;rd=(insn>>4)&3
    if op==0:return f'add r{rd},r{(insn>>2)&3},r{insn&3}'
    if op==2:
        value=insn&15 if not enhanced else (insn&3)<<(2*((insn>>2)&3))
        return f'li r{rd},{value}'
    if op==3:
        v=(insn>>2)&15
        if enhanced and v&8:v-=16
        return f'bner0 r{insn&3},{v:+}' if enhanced else f'bner0 r{insn&3},{v}'
    return f'io r{rd},{"out" if insn&8 else "in"},{insn&7}'

if __name__=='__main__':
    folder=Path(__file__).resolve().parent
    for name,(enh,program) in programs().items():
        image=program+[0]*(256-len(program));(folder/(name+'.hex')).write_text(''.join(f'{v:02x}\n' for v in image),encoding='ascii')
        (folder/(name+'.asm')).write_text('\n'.join(f'{i:02x}: {v:02x}  {disassemble(v,enh)}' for i,v in enumerate(program))+'\n',encoding='utf8')
