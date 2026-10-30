"""Independent structural implementations of the public F2/F3 assignments."""
from logisim_circuits import *
from evidence import *
from itertools import product
import random

PATTERNS=[0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]
def zeros(c,n):return [c.const(0)]*n
def eq(c,a,b):return c.and_(*[c.inv(c.xor(x,y)) for x,y in zip(a,b)])
def eq_const(c,a,n):return c.and_(*[b if n>>i&1 else c.inv(b) for i,b in enumerate(a)])
def fa(c,a,b,cin):
    p=c.xor(a,b);return c.xor(p,cin),c.or_(c.and_(a,b),c.and_(p,cin))
def add(c,a,b,carry=None):
    carry=carry if carry is not None else c.const(0);out=[]
    for x,y in zip(a,b):s,carry=fa(c,x,y,carry);out.append(s)
    return out,carry
def sub(c,a,b):return add(c,a,[c.inv(x) for x in b],c.const(1))
def select(c,s,a,b):return [c.mux(s,x,y) for x,y in zip(a,b)]
def decode(c,bits):return [eq_const(c,bits,n) for n in range(1<<len(bits))]
def lookup(c,inputs,values,outwidth):
    dec=decode(c,inputs);z=c.const(0);return [c.or_(*[dec[n] for n,v in enumerate(values) if v>>bit&1]) if any(v>>bit&1 for v in values) else z for bit in range(outwidth)]
def busout(c,name,bits):return c.io(name,len(bits),True,c.join(bits))
def display(c,bits,label='S7',x=1600,y=180):
    comp(c.el,'I/O','7-Segment Display',x,y,label=label)
    for net,(dx,dy) in zip(bits,[(20,0),(30,0),(20,60),(10,60),(0,60),(10,0),(0,0),(30,60)]):c.tap(x+dx,y+dy,net,'up' if dy==0 else 'down')
def led(c,net,label='LED_OUT',x=1650,y=350):comp(c.el,'I/O','LED',x,y,label=label);c.tap(x,y,net,'left')
def hexdisplay(c,bits,label='HEX',x=1600,y=180):
    comp(c.el,'I/O','Hex Digit Display',x,y,decimalPoint=False,label=label);c.tap(x,y,c.join(bits),'down')
def input_bus(c,name,width):return c.split(c.io(name,width))
def xor_nand(c,a,b):
    t=c.gate('NAND',[a,b]);u=c.gate('NAND',[a,t]);v=c.gate('NAND',[b,t]);return c.gate('NAND',[u,v])
def xor_tutorial(c,a,b):return c.or_(c.and_(a,c.inv(b)),c.and_(c.inv(a),b))
def sr_nor(c,s,r,q=None):
    q=q or c.fresh('Q');qb=c.fresh('QB');c.gate('NOR',[r,qb],q);c.gate('NOR',[s,q],qb);return q,qb
def reg_named(c,bits,clk,rst,en=None,prefix='Q'):
    q=[c.fresh(prefix) for _ in bits]
    for i,d in enumerate(bits):c.ff(c.mux(en,q[i],d) if en is not None else d,clk,rst,q[i])
    return q
def counter(c,n,clk,rst,enable=None,mod=None):
    q=[c.fresh('count') for _ in range(n)];inc,carry=add(c,q,[c.const(1)]+zeros(c,n-1));top=eq_const(c,q,(mod-1) if mod else (1<<n)-1)
    if mod:inc=select(c,top,inc,zeros(c,n))
    for i,d in enumerate(inc):c.ff(c.mux(enable,q[i],d) if enable is not None else d,clk,rst,q[i])
    return q,top

def vecfile(name,header,rows):
    path=ROOT/'F/vectors'/(name+'.txt');path.write_text(' '.join(header)+'\n'+''.join((' '.join(str(x) for x in row)+'\n') if not isinstance(row,str) else row+'\n' for row in rows),encoding='utf8');return path
def build():
    p=Project('tutorial_xor');jobs=[];mapping={}
    def job(name,header,rows,ids=()):
        v=vecfile(name,header,rows);jobs.append({'circuit':name,'vectors':str(v),'tasks':list(ids),'rows':sum(1 for l in v.read_text('utf8').splitlines()[1:] if l and not l.startswith('!'))});mapping[name]=list(ids)
    c=p.circuit('tutorial_xor');a=c.io('X');b=c.io('Y');q=xor_tutorial(c,a,b);c.io('Z',output=True,net=q);led(c,q)
    job(c.name,['X','Y','Z','LED_OUT@0'],[(a,b,a^b,a^b) for a,b in product(range(2),repeat=2)],['F2-M002'])
    c=p.circuit('parity_alarm');bits=input_bus(c,'DATA',4);q=c.xor(c.xor(bits[0],bits[1]),c.xor(bits[2],bits[3]));c.io('ODD',output=True,net=q);led(c,q)
    job(c.name,['DATA','ODD','LED_OUT@0'],[(a,a.bit_count()%2,a.bit_count()%2) for a in range(16)],['F2-M005'])
    c=p.circuit('xor_nand4');a=c.io('A');b=c.io('B');c.io('Y',output=True,net=xor_nand(c,a,b));job(c.name,['A','B','Y'],[(a,b,a^b) for a,b in product(range(2),repeat=2)],['F3-M003'])
    c=p.circuit('xnor');a=c.io('A');b=c.io('B');c.io('Y',output=True,net=c.inv(xor_nand(c,a,b)));job(c.name,['A','B','Y'],[(a,b,int(a==b)) for a,b in product(range(2),repeat=2)],['F3-M004'])
    c=p.circuit('decoder2to4');bits=input_bus(c,'A',2);outs=decode(c,bits);busout(c,'Y',outs);job(c.name,['A','Y'],[(a,1<<a) for a in range(4)],['F3-M007','F3-M008'])
    c=p.circuit('decoder3to8');bits=input_bus(c,'A',3);lo=c.join(bits[:2]);d0=c.split(c.sub('decoder2to4',{'A':lo})['Y']);d1=c.split(c.sub('decoder2to4',{'A':lo})['Y']);n=c.inv(bits[2]);out=[c.and_(n,b) for b in d0]+[c.and_(bits[2],b) for b in d1];busout(c,'Y',out);job(c.name,['A','Y'],[(a,1<<a) for a in range(8)],['F3-M009'])
    for mode in ['decimal','hex']:
        c=p.circuit('sevenseg_'+mode);bits=input_bus(c,'A',4);table=PATTERNS if mode=='hex' else PATTERNS[:10]+[0x80]*6;s=lookup(c,bits,table,8);busout(c,'SEG',s);display(c,s)
        job(c.name,['A','SEG']+[f'S7@{i}' for i in range(8)],[(a,v,*[(v>>b)&1 for b in range(8)]) for a,v in enumerate(table)],['F3-M010' if mode=='decimal' else 'F3-M011'])
    c=p.circuit('encoder16to4');bits=input_bus(c,'I',16);out=[c.or_(*[bits[n] for n in range(16) if n>>i&1]) for i in range(4)];busout(c,'Y',out);hexdisplay(c,out)
    job(c.name,['I','Y','HEX@0'],[(1<<i,i,i) for i in range(16)],['F3-M012'])
    c=p.circuit('priority4to2');bits=input_bus(c,'I',4);y1=c.or_(bits[3],bits[2]);y0=c.or_(bits[3],c.and_(c.inv(bits[2]),bits[1]));busout(c,'Y',[y0,y1]);c.io('VALID',output=True,net=c.or_(*bits))
    job(c.name,['I','Y','VALID'],[(a,max(a.bit_length()-1,0),int(a!=0)) for a in range(16)],['F3-M013'])
    c=p.circuit('mux2');a=c.io('A');b=c.io('B');s=c.io('S');c.io('Y',output=True,net=c.mux(s,a,b));job(c.name,['A','B','S','Y'],[(a,b,s,b if s else a) for a,b,s in product(range(2),repeat=3)],['F3-M014'])
    c=p.circuit('mux4x3');data=[input_bus(c,'D'+str(i),3) for i in range(4)];s=input_bus(c,'S',2);out=select(c,s[1],select(c,s[0],data[0],data[1]),select(c,s[0],data[2],data[3]));busout(c,'Y',out)
    job(c.name,['D0','D1','D2','D3','S','Y'],[(a,b,d,e,s,[a,b,d,e][s]) for a,b,d,e,s in product(range(8),range(8),range(8),range(8),range(4))],['F3-M015'])
    c=p.circuit('select_display');a=c.io('A',4);s=c.io('HEXMODE');dec=c.split(c.sub('sevenseg_decimal',{'A':a})['SEG']);hexa=c.split(c.sub('sevenseg_hex',{'A':a})['SEG']);out=select(c,s,dec,hexa);busout(c,'SEG',out);display(c,out)
    job(c.name,['A','HEXMODE','SEG']+[f'S7@{i}' for i in range(8)],[(a,m,(v:=PATTERNS[a] if m or a<10 else 128),*[(v>>b)&1 for b in range(8)]) for a,m in product(range(16),range(2))],['F3-M016'])
    c=p.circuit('equal4');a=input_bus(c,'A',4);b=input_bus(c,'B',4);q=eq(c,a,b);c.io('EQ',output=True,net=q);led(c,q)
    job(c.name,['A','B','EQ','LED_OUT@0'],[(a,b,int(a==b),int(a==b)) for a,b in product(range(16),repeat=2)],['F3-M017'])
    c=p.circuit('full_adder');a=c.io('A');b=c.io('B');ci=c.io('CI');s,co=fa(c,a,b,ci);c.io('S',output=True,net=s);c.io('CO',output=True,net=co)
    job(c.name,['A','B','CI','S','CO'],[(a,b,i,(a+b+i)&1,(a+b+i)>>1) for a,b,i in product(range(2),repeat=3)],['F3-M018'])
    for operation in ['add4','sub4']:
        c=p.circuit(operation);a=input_bus(c,'A',4);b=input_bus(c,'B',4);out,carry=add(c,a,b) if operation=='add4' else sub(c,a,b);flag=carry if operation=='add4' else c.inv(carry);busout(c,'S',out);c.io('C' if operation=='add4' else 'BORROW',output=True,net=flag);hexdisplay(c,a,'AHEX',1600,180);hexdisplay(c,b,'BHEX',1600,300);hexdisplay(c,out,'SHEX',1600,420);led(c,flag,'FLAG',1650,550)
        rows=[]
        for aa,bb in product(range(16),repeat=2):s=(aa+bb if operation=='add4' else aa-bb)&15;f=int(aa+bb>15) if operation=='add4' else int(aa<bb);rows.append((aa,bb,s,f,aa,bb,s,f))
        job(c.name,['A','B','S','C' if operation=='add4' else 'BORROW','AHEX@0','BHEX@0','SHEX@0','FLAG@0'],rows,['F3-M019' if operation=='add4' else 'F3-M020'])
    c=p.circuit('signmag4');a=input_bus(c,'A',4);b=input_bus(c,'B',4);same=c.inv(c.xor(a[3],b[3]));summ,co=add(c,a[:3],b[:3]);ab,nborrow=sub(c,a[:3],b[:3]);ba,_=sub(c,b[:3],a[:3]);diff=select(c,nborrow,ba,ab);mag=select(c,same,diff,summ);sign=c.mux(same,c.mux(nborrow,b[3],a[3]),a[3]);sign=c.and_(sign,c.or_(*mag));busout(c,'S',mag+[sign]);ov=c.and_(same,co);c.io('OV',output=True,net=ov);hexdisplay(c,mag+[c.const(0)],'MAG');minus=[c.const(0)]*6+[sign,c.const(0)];display(c,minus,'SIGN',1650,330)
    rows=[]
    for aa,bb in product(range(16),repeat=2):
        av=-(aa&7) if aa&8 else aa;bv=-(bb&7) if bb&8 else bb;v=av+bv;m=abs(v)&7;s=m|(8 if v<0 and m else 0);rows.append((aa,bb,s,int(abs(v)>7),m,int(v<0 and m!=0)))
    job(c.name,['A','B','S','OV','MAG@0','SIGN@6'],rows,['F3-M021'])
    c=p.circuit('ones4');a=input_bus(c,'A',4);b=input_bus(c,'B',4);ss,co=add(c,a,b);out,_=add(c,ss,zeros(c,4),co);busout(c,'S',out);job(c.name,['A','B','S'],[(a,b,((a+b)&15)+((a+b)>>4)) for a,b in product(range(16),repeat=2)],['F3-M022'])
    c=p.circuit('signed_overflow4');a=input_bus(c,'A',4);b=input_bus(c,'B',4);s,co=add(c,a,b);v=c.and_(c.inv(c.xor(a[3],b[3])),c.xor(a[3],s[3]));busout(c,'S',s);c.io('V',output=True,net=v)
    job(c.name,['A','B','S','V'],[(a,b,(a+b)&15,int(not(-8<=((a-16 if a&8 else a)+(b-16 if b&8 else b))<=7))) for a,b in product(range(16),repeat=2)],['F3-M023'])
    c=p.circuit('sr_latch');s=c.io('S');r=c.io('R');q,qb=sr_nor(c,s,r);c.io('Q',output=True,net=q);c.io('QB',output=True,net=qb)
    job(c.name,['S','R','Q','QB','OSC'],[(0,1,0,1,0),(0,0,0,1,0),(1,0,1,0,0),(0,0,1,0,0),(1,1,0,0,0),(0,0,'-','-',1)],['F3-M024'])
    for variant in ['dlatch_nor','dlatch_nand','dlatch_reset']:
        c=p.circuit(variant);d=c.io('D');we=c.io('WE');rst=c.io('RESET') if variant=='dlatch_reset' else None
        if variant=='dlatch_nor':q,_=sr_nor(c,c.and_(d,we),c.and_(c.inv(d),we))
        elif variant=='dlatch_nand':
            sb=c.gate('NAND',[d,we]);rb=c.gate('NAND',[sb,we]);q=c.fresh('q');qb=c.fresh('qb');c.gate('NAND',[sb,qb],q);c.gate('NAND',[rb,q],qb)
        else:q=c.latch(d,we,rst)
        c.io('Q',output=True,net=q);rows=[]
        if rst is not None:rows+=[(0,0,1,0,0),(1,1,1,0,0),(0,0,0,0,0)]
        base=[(0,1,0,0),(1,1,1,0),(0,0,1,0),(1,0,1,0),(0,1,0,0),(1,0,0,0)]
        rows += [(d,we,0,q,osc) for d,we,q,osc in base] if rst is not None else base
        job(c.name,['D','WE']+(['RESET'] if rst is not None else [])+['Q','OSC'],rows,['F3-M025','F3-M027'] if variant=='dlatch_nor' else ['F3-M026'] if variant=='dlatch_nand' else ['F3-M028'])
    c=p.circuit('latch_oscillator');we=c.io('WE');rst=c.io('RESET');q=c.fresh('q');c.latch(c.inv(q),we,rst,q);c.io('Q',output=True,net=q);job(c.name,['WE','RESET','Q','OSC'],[(0,1,0,0),(1,0,'-',1)],['F3-M029'])
    for variant in ['dff','dff_reset','dff_enable','toggle']:
        c=p.circuit(variant);clk=c.io('CLK');rst=c.io('RESET') if variant!='dff' else None;d=c.io('D') if variant!='toggle' else None;en=c.io('EN') if variant=='dff_enable' else None
        q=c.fresh('q');din=c.inv(q) if variant=='toggle' else c.mux(en,q,d) if en is not None else d;c.ff(din,clk,rst,q);c.io('Q',output=True,net=q)
        if variant=='dff':header=['CLK','D','Q','OSC'];rows=[(0,0,'-',0),(1,0,0,0),(1,1,0,0),(0,1,0,0),(1,1,1,0),(1,0,1,0),(0,0,1,0),(1,0,0,0)]
        elif variant=='toggle':
            header=['CLK','RESET','Q','OSC'];rows=[(0,1,0,0),(0,0,0,0)];v=0
            for i in range(32):v^=1;rows += [(1,0,v,0),(0,0,v,0)]
        else:
            header=['CLK','RESET','D']+(['EN'] if en is not None else [])+['Q','OSC'];rows=[];v=0;rng=random.Random(2607)
            for i in range(60):
                rstval=int(i in (0,21,44));dv=rng.randrange(2);ev=rng.randrange(2) if en is not None else 1
                if rstval:v=0
                args=(rstval,dv,*([ev] if en is not None else []));rows.append((0,*args,v,0));v=0 if rstval else dv if ev else v;rows.append((1,*args,v,0))
        ids={'dff':['F3-M030'],'dff_reset':['F3-M031'],'toggle':['F3-M032'],'dff_enable':['F3-M033']}[variant];job(c.name,header,rows,ids)
    c=p.circuit('reg4');d=input_bus(c,'D',4);clk=c.io('CLK');rst=c.io('RESET');q=reg_named(c,d,clk,rst);busout(c,'Q',q);hexdisplay(c,q)
    rows=[(0,0,1,0,0),(0,1,1,0,0)]
    old=0
    for d in range(16):rows.append((d,0,0,old,old));rows.append((d,1,0,d,d));old=d
    rows += [(7,0,1,0,0),(7,1,1,0,0)];job(c.name,['D','CLK','RESET','Q','HEX@0'],rows,['F3-M034'])
    c=p.circuit('counter4');clk=c.io('CLK');rst=c.io('RESET');q,_=counter(c,4,clk,rst);busout(c,'Q',q);hexdisplay(c,q)
    rows=[(0,1,0,0),(0,0,0,0)]
    for n in range(1,34):rows.extend([(1,0,n%16,n%16),(0,0,n%16,n%16)])
    job(c.name,['CLK','RESET','Q','HEX@0'],rows,['F3-M035'])
    c=p.circuit('sum10');clk=c.io('CLK');rst=c.io('RESET');count=[c.fresh('i') for _ in range(8)];acc=[c.fresh('acc') for _ in range(8)];done=eq_const(c,count,10);en=c.inv(done);inc,_=add(c,count,[c.const(1)]+zeros(c,7));nacc,_=add(c,acc,inc)
    for old,new in zip(count,inc):c.ff(c.mux(en,old,new),clk,rst,old)
    for old,new in zip(acc,nacc):c.ff(c.mux(en,old,new),clk,rst,old)
    busout(c,'I',count);busout(c,'SUM',acc);c.io('DONE',output=True,net=done);hexdisplay(c,acc[:4],'LO');hexdisplay(c,acc[4:],'HI',1650,180)
    rows=[(0,1,0,0,0),(0,0,0,0,0)]
    for n in range(1,15):i=min(n,10);s=i*(i+1)//2;rows.extend([(1,0,i,s,int(i==10)),(0,0,i,s,int(i==10))])
    job(c.name,['CLK','RESET','I','SUM','DONE'],rows,['F3-M036'])
    c=p.circuit('clock_mmss');clk=c.io('CLK');rst=c.io('RESET');s1,cs1=counter(c,4,clk,rst,mod=10);s10,cs10=counter(c,3,clk,rst,enable=cs1,mod=6);m1,cm1=counter(c,4,clk,rst,enable=c.and_(cs1,cs10),mod=10);m10,_=counter(c,3,clk,rst,enable=c.and_(cs1,cs10,cm1),mod=6)
    for label,bits in [('S1',s1),('S10',s10),('M1',m1),('M10',m10)]:busout(c,label,bits)
    hexdisplay(c,m10+[c.const(0)],'M10HEX',1500,180);hexdisplay(c,m1,'M1HEX',1560,180);hexdisplay(c,s10+[c.const(0)],'S10HEX',1660,180);hexdisplay(c,s1,'S1HEX',1720,180)
    rows=[(0,1,0,0,0,0),(0,0,0,0,0,0)]
    for n in range(1,3602):t=n%3600;m,s=divmod(t,60);v=(s%10,s//10,m%10,m//10);rows.extend([(1,0,*v),(0,0,*v)])
    job(c.name,['CLK','RESET','S1','S10','M1','M10'],rows,['F3-M037'])
    path=ROOT/'F/circuits/fundamentals.circ';p.write(path);dump(ROOT/'config/F_circuit_jobs.json',{'circuit_file':str(path),'jobs':jobs,'seed':2607,'implementation':'Independently authored structural Logisim gates, wires, own latch/FF and hierarchical decoder; native displays also probed'})
    print('BUILT_F_CIRCUITS',len(p.circuits),'jobs',len(jobs),'vectors',sum(j['rows'] for j in jobs),flush=True)
    return p
if __name__=='__main__':build()
