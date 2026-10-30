from pathlib import Path
import sys,struct,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def addi(rd,rs,i):return ((i&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def add(rd,a,b):return (b<<20)|(a<<15)|(rd<<7)|0x33
def lui(rd,imm):return (imm<<12)|(rd<<7)|0x37
def jalr(rd,rs,imm):return ((imm&4095)<<20)|(rs<<15)|(rd<<7)|0x67
def load(rd,rs,off,byte=False):return ((off&4095)<<20)|(rs<<15)|((4 if byte else 2)<<12)|(rd<<7)|3
def store(rs,base,off,byte=False):return (((off&4095)>>5)<<25)|(rs<<20)|(base<<15)|((0 if byte else 2)<<12)|((off&31)<<7)|0x23
BREAK=0x00100073
def oracle(blob,steps=0):
    mem=bytearray(1024*1024);mem[:len(blob)]=blob;r=[0]*16;pc=0;trace=[];loads=stores=0
    for _ in range(steps or 100000):
        old=pc;inst=int.from_bytes(mem[pc:pc+4],'little');opc=inst%128;rd=(inst//128)%32;a=(inst//32768)%32;b=(inst//1048576)%32;f=(inst//4096)%8
        imm=inst//1048576;imm=imm if imm<2048 else imm-4096;nextpc=(pc+4)%2**32;value=None;halt=False
        if inst==BREAK:halt=True
        elif opc==0x13 and f==0:value=(r[a]+imm)%2**32
        elif opc==0x33 and f==0 and inst//2**25==0:value=(r[a]+r[b])%2**32
        elif opc==0x37:value=inst&0xfffff000
        elif opc==0x67 and f==0:nextpc=(r[a]+imm)%2**32 & ~1;value=(pc+4)%2**32
        elif opc==3 and f in (2,4):
            n=4 if f==2 else 1;address=(r[a]+imm)%2**32;assert address+n<=len(mem) and (n==1 or address%4==0);value=int.from_bytes(mem[address:address+n],'little');loads+=1
        elif opc==0x23 and f in (0,2):
            field=(inst//2**25)*32+(inst//128)%32;off=field if field<2048 else field-4096;n=4 if f==2 else 1;address=(r[a]+off)%2**32;assert address+n<=len(mem) and (n==1 or address%4==0);mem[address:address+n]=(r[b]%(2**(8*n))).to_bytes(n,'little');stores+=1
        else:raise ValueError(hex(inst))
        if value is not None and rd:r[rd]=value
        r[0]=0;pc=nextpc;trace.append([old,inst,pc,*r])
        if halt:break
    else:assert steps
    return {'pc':pc,'gpr':r,'instructions':len(trace),'loads':loads,'stores':stores},trace
def main():
    folder=ROOT/'E/E5/programs';folder.mkdir(exist_ok=True);cases=[]
    def save(name,words,expect=0,steps=0,error=0):
        blob=b''.join(struct.pack('<I',w) for w in words);p=folder/(name+'.bin');p.write_bytes(blob)
        (folder/(name+'.hex')).write_text(''.join(f'{w:08x}\n' for w in words))
        row={'name':name,'path':str(p),'sha256':sha(p),'steps':steps,'expect':expect,'error':error}
        if not error:
            expected,trace=oracle(blob,steps);assert expected['gpr'][10]==expect
            row['expected']=expected;target=folder/(name+'.expected.csv');target.write_text(''.join(','.join(f'{x:08x}' for x in r)+'\n' for r in trace));row['trace']=str(target)
        cases.append(row)
    six=[0x01400513,0x010000e7,0x00c000e7,0x00c00067,0x00a50513,0x00008067]
    save('six_loop',six,30,12);six[3]=BREAK;save('six_ebreak',six,30)
    save('negative_immediates',[addi(1,0,-1),addi(2,0,-2048),addi(3,0,2047),add(4,2,3),addi(5,1,1),addi(0,0,37),addi(10,0,0),BREAK])
    save('jalr_alias_odd',[addi(1,0,17),jalr(1,1,0),addi(10,0,99),BREAK,addi(10,1,22),BREAK],30)
    save('x0_overflow',[lui(0,0xfffff),addi(0,0,-1),addi(1,0,-1),addi(2,0,1),add(3,1,2),lui(4,0x80000),addi(4,4,-2048),addi(10,0,0),BREAK])
    words=[lui(1,0x40),lui(2,0x12345),addi(2,2,0x678),store(2,1,0),store(2,1,4),load(3,1,0)]
    words += [load(4+i,1,i,True) for i in range(4)]
    for offset,value in [(3,0x90),(2,0xab),(1,0xcd),(0,0xef)]:words += [addi(9,0,value),store(9,1,offset,True)]
    words += [load(11,1,0),load(12,1,4)]+[load(4+i,1,i,True) for i in range(4)]+[load(0,1,0),addi(10,0,0),BREAK];save('memory_endian',words)
    save('address_wrap',[addi(1,0,-16),addi(2,0,0x123),store(2,1,16),load(3,0,0),addi(10,0,0),BREAK])
    save('reserved_register',[addi(16,0,1),BREAK],error=3)
    save('invalid_opcode',[0xffffffff,BREAK],error=3)
    save('unaligned_word',[lui(1,0x40),load(2,1,2),BREAK],error=3)
    save('misaligned_jump',[jalr(1,0,2),BREAK],error=3)
    rng=random.Random(260705);regs=[x for x in range(16) if x!=8];words=[lui(8,0x40)]
    for i in range(5000):
        rd=rng.choice(regs);a=rng.randrange(16);b=rng.randrange(16);kind=rng.randrange(8)
        if kind==0:words.append(addi(rd,a,rng.randrange(-2048,2048)))
        elif kind==1:words.append(add(rd,a,b))
        elif kind==2:words.append(lui(rd,rng.randrange(1<<20)))
        elif kind in (3,4):words.append(load(rd,8,rng.randrange(-512,512)*4 if kind==3 else rng.randrange(-2048,2048),kind==4))
        elif kind in (5,6):words.append(store(b,8,rng.randrange(-512,512)*4 if kind==5 else rng.randrange(-2048,2048),kind==6))
        else:
            target=4*(len(words)+4)+1;hi=(target+2048)//4096;lo=target-hi*4096
            words += [lui(1,hi),addi(1,1,lo),jalr(1,1,0),0xffffffff]
    words += [addi(10,0,0),BREAK];save('random_ops',words)
    dump(ROOT/'reports/E5_vectors.json',{'status':'PASS_GENERATION_NOT_EXECUTION','seed':260705,'cases':cases});print('E5_VECTORS',len(cases),flush=True)
if __name__=='__main__':main()
