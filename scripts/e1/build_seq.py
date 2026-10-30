from common import *
from collections import Counter

class RegisterModel(Model):
    def __init__(self,nextfn,out='q',reset=None,active=1,value=0,asynchronous=False):self.q=None;self.nextfn=nextfn;self.out=out;self.reset=reset;self.active=active;self.value=value;self.async_reset=asynchronous
    def asynchronous(self,v):
        if self.async_reset and v[self.reset]==self.active:self.q=self.value
    def tick(self,v):self.q=self.value if self.reset and v[self.reset]==self.active else self.nextfn(self.q,v)
    def output(self,v):return {self.out:self.q}

def cycles_random(widths,n=500,seed=260710,first=None,reset=None,active=1):
    rng=random.Random(seed);out=[]
    if first:out.extend(first)
    for k in range(n):
        v={name:rng.getrandbits(w) for name,w in widths.items()}
        if reset:v[reset]=active if k%73==0 else 1-active
        out.append(v)
    return out

def main():
    ps=[]
    class Delay(Model):
        def __init__(self,vector=False):self.pipe=[None]*3;self.vector=vector
        def tick(self,v):self.pipe=[v['d']]+self.pipe[:2]
        def output(self,v):return {'q':([v['d']]+self.pipe)[v['sel']] if self.vector else self.pipe[-1]}
    p=Problem('module_shift','wire q1,q2;my_dff u0(clk,d,q1);my_dff u1(clk,q1,q2);my_dff u2(clk,q2,q);',support='module my_dff(input clk,d,output reg q);always @(posedge clk)q<=d;endmodule',mask_reasons={'q':'No reset; pipeline positions are undefined until three samples arrive.'},explanation='三个题面DFF串接；独立队列参考验证三拍历史，无新增复位。')
    p.clocked(Delay(),cycles_random({'d':1},250));ps.append(p)
    p=Problem('module_shift8','wire[7:0]q1,q2,q3;my_dff8 u0(clk,d,q1);my_dff8 u1(clk,q1,q2);my_dff8 u2(clk,q2,q3);assign q=sel==0?d:sel==1?q1:sel==2?q2:q3;',support='module my_dff8(input clk,input[7:0]d,output reg[7:0]q);always @(posedge clk)q<=d;endmodule',mask_reasons={'q':'Unfilled pipeline tap undefined; direct input and filled taps still checked.'})
    p.clocked(Delay(True),cycles_random({'d':8,'sel':2},800));ps.append(p)
    class ClockXor(Model):
        def __init__(self):self.q=None
        def tick(self,v):self.q=int(v['a']!=v['b'])
        def output(self,v):x=int(v['a']!=v['b']);return {'out_assign':x,'out_always_comb':x,'out_always_ff':self.q}
    p=Problem('alwaysblock2','assign out_assign=a^b;always @* out_always_comb=a^b;always @(posedge clk)out_always_ff<=a^b;',procedural=['out_always_comb','out_always_ff'],mask_reasons={'out_always_ff':'Unreset flop before its first sample only.'})
    p.clocked(ClockXor(),list(exhaustive({'a':1,'b':1}))*30);ps.append(p)
    p=Problem('dff','always @(posedge clk)q<=d;',procedural=['q'],mask_reasons={'q':'Unreset flop before first positive edge.'});p.clocked(RegisterModel(lambda q,v:v['d']),cycles_random({'d':1},300));ps.append(p)
    p=Problem('dff8p',"reg[7:0]value;assign q=value;always @(negedge clk)if(reset)value<=8'h34;else value<=d;",mask_reasons={'q':'Before first synchronous reset/clock sample.'},explanation='原文指定下降沿和同步复位0x34；时钟正沿阶段的保持也单独检查。')
    p.clocked(RegisterModel(lambda q,v:v['d'],reset='reset',value=0x34),cycles_random({'d':8,'reset':1},600,reset='reset'),falling=True);ps.append(p)
    p=Problem('dff8ar',"reg[7:0]value;assign q=value;always @(posedge clk or posedge areset)if(areset)value<=8'h00;else value<=d;",explanation='异步复位在无正沿的输入阶段立即验证，不能被同步复位代替。')
    p.clocked(RegisterModel(lambda q,v:v['d'],reset='areset',asynchronous=True),cycles_random({'d':8,'areset':1},600,reset='areset'));ps.append(p)
    p=Problem('dff16e',"reg[15:0]value;assign q=value;always @(posedge clk)begin if(!resetn)value<=16'h0;else begin if(byteena[0])value[7:0]<=d[7:0];if(byteena[1])value[15:8]<=d[15:8];end end",mask_reasons={'q':'Before the initial active-low synchronous reset.'})
    def bytes_next(q,v):
        return ((v['d']&255) if v['byteena']&1 else (q&255))|((v['d']&65280) if v['byteena']&2 else (q&65280))
    p.clocked(RegisterModel(bytes_next,reset='resetn',active=0),cycles_random({'d':16,'byteena':2,'resetn':1},1000,reset='resetn',active=0));ps.append(p)
    p=Problem('mt2015_muxdff','always @(posedge clk)Q<=L?r_in:q_in;',procedural=['Q'],mask_reasons={'Q':'Unreset stage until first edge.'},explanation='只实现图中一个MUX+DFF子级；q_in是外部端口，不是本级反馈Q。')
    p.clocked(RegisterModel(lambda q,v:v['r_in'] if v['L'] else v['q_in'],out='Q'),list(exhaustive({'L':1,'r_in':1,'q_in':1}))*20);ps.append(p)
    muxdff='reg value;assign Q=value;always @(posedge clk)if(L)value<=R;else if(E)value<=w;'
    p=Problem('2014_q4a',muxdff,mask_reasons={'Q':'Unreset until a load/enable samples a value.'},explanation='按原图：L优先于E；L0/E0反馈保持，L0/E1选择w。')
    p.clocked(RegisterModel(lambda q,v:v['R'] if v['L'] else v['w'] if v['E'] else q,out='Q'),[{'w':0,'R':1,'E':0,'L':1}]+list(exhaustive({'w':1,'R':1,'E':1,'L':1}))*20);ps.append(p)
    body="reg stored,next_d;assign Q=stored;always @* begin case({j,k})2'b00:next_d=stored;2'b01:next_d=0;2'b10:next_d=1;2'b11:next_d=~stored;default:next_d=1'bx;endcase end always @(posedge clk)stored<=next_d;"
    p=Problem('ece241_2013_q7',body,mask_reasons={'Q':'No initial state specified; first clear/set establishes it.'})
    def jk(q,v):return q if not(v['j'] or v['k']) else 0 if not v['j'] else 1 if not v['k'] else None if q is None else 1-q
    p.clocked(RegisterModel(jk,out='Q'),[{'j':1,'k':0}]+list(exhaustive({'j':1,'k':1}))*30);ps.append(p)
    class Edges(Model):
        def __init__(self,kind):self.prev=None;self.result=None;self.kind=kind
        def tick(self,v):
            old=self.prev;self.prev=v['in']
            if self.kind=='capture':
                if v['reset']:self.result=0
                elif old is not None:self.result=(self.result or 0)|(old&~v['in']&0xffffffff)
            else:self.result=None if old is None else ((v['in']&~old)&255 if self.kind=='rise' else v['in']^old)
        def output(self,v):return { {'rise':'pedge','both':'anyedge','capture':'out'}[self.kind]:self.result}
    for slug,kind,name in [('edgedetect','rise','pedge'),('edgedetect2','both','anyedge')]:
        body='reg[7:0]previous,result;assign '+name+'=result;always @(posedge clk)begin previous<=in;result<='+('in&~previous' if kind=='rise' else 'in^previous')+';end'
        p=Problem(slug,body,mask_reasons={name:'First comparison lacks a previous sample; later outputs always checked.'})
        p.clocked(Edges(kind),[{'in':v} for v in [0,255,255,0,0,1,0,128,0]]+cycles_random({'in':8},1000));ps.append(p)
    body="reg[31:0]previous,captured;assign out=captured;always @(posedge clk)begin previous<=in;if(reset)captured<=32'b0;else captured<=captured|(previous&~in);end"
    p=Problem('edgecapture',body,mask_reasons={'out':'Before initial synchronous reset only.'},explanation='previous每拍都采样，包括复位拍；复位优先于本拍捕获。专测复位拍in=1、下一拍in=0的捕获。')
    cases=[{'reset':1,'in':0},{'reset':0,'in':0xffffffff},{'reset':1,'in':0xffffffff},{'reset':0,'in':0}]+cycles_random({'reset':1,'in':32},1500,reset='reset')
    p.clocked(Edges('capture'),cases);ps.append(p)
    body='reg rising,falling;always @(posedge clk)rising<=d;always @(negedge clk)falling<=d;assign q=clk?rising:falling;'
    p=Problem('dualedge',body,explanation='两个单沿触发器加时钟选择MUX；符合题目允许忽略组合毛刺的功能模型，不能原封不动带入后续禁止下降沿的NPC。')
    rng=random.Random(260711);clk=None;q=None
    for _ in range(1000):
        newclk=rng.randrange(2);d=rng.randrange(2)
        if clk is None or newclk!=clk:q=d
        p.add({'clk':newclk,'d':d},{'q':q});clk=newclk
    ps.append(p)
    for slug,start,enable in [('count1to10',1,None),('countslow',0,'slowena')]:
        maximum=10 if start else 9;body=f'reg[3:0]count;assign q=count;always @(posedge clk)if(reset)count<=4\'d{start};else '+('if(slowena)' if enable else '')+f' count <= (count == 4\'d{maximum}) ? 4\'d{start} : count + 4\'d1;'
        p=Problem(slug,body,mask_reasons={'q':'Before initial synchronous reset.'})
        model=RegisterModel(lambda q,v,s=start,e=enable,m=maximum:q if e and not v[e] else s if q==m else q+1,reset='reset',value=start)
        widths={'reset':1};widths.update({enable:1} if enable else {});p.clocked(model,cycles_random(widths,800,reset='reset'));ps.append(p)
    body="wire[3:0]u,t,h;assign c_enable[0]=1'b1;assign c_enable[1]=(u==9);assign c_enable[2]=(u==9)&&(t==9);assign OneHertz=(u==9)&&(t==9)&&(h==9);bcdcount low(clk,reset,c_enable[0],u);bcdcount middle(clk,reset,c_enable[1],t);bcdcount high(clk,reset,c_enable[2],h);"
    support="module bcdcount(input clk,reset,enable,output reg[3:0]Q);always @(posedge clk)if(reset)Q<=0;else if(enable)Q<=Q==9?0:Q+1'b1;endmodule"
    class Divider(Model):
        def __init__(self):self.n=None
        def tick(self,v):self.n=0 if v['reset'] else (self.n+1)%1000
        def output(self,v):return {'OneHertz':None if self.n is None else int(self.n==999),'c_enable':None if self.n is None else 1|(int(self.n%10==9)<<1)|(int(self.n%100==99)<<2)}
    p=Problem('ece241_2014_q7b',body,support=support,mask_reasons={'OneHertz':'Before first reset.','c_enable':'Before first reset.'},explanation='三个BCD计数器直接共用clk；进位用enable，OneHertz每1000周期只高一拍。')
    p.clocked(Divider(),[{'reset':int(n in (0,1000,2501))} for n in range(4505)]);ps.append(p)
    body="""reg pm_value;reg[7:0]hours,minutes,seconds;
assign pm=pm_value;assign hh=hours;assign mm=minutes;assign ss=seconds;
function[7:0] inc_bcd;input[7:0]v;begin inc_bcd=(v[3:0]==9)?v+8'd7:v+8'd1;end endfunction
always @(posedge clk)begin
if(reset)begin pm_value<=0;hours<=8'h12;minutes<=0;seconds<=0;end
else if(ena)begin
if(seconds==8'h59)begin seconds<=0;
if(minutes==8'h59)begin minutes<=0;
if(hours==8'h11)begin hours<=8'h12;pm_value<=~pm_value;end
else if(hours==8'h12)hours<=8'h01;else hours<=inc_bcd(hours);
end else minutes<=inc_bcd(minutes);
end else seconds<=inc_bcd(seconds);
end end"""
    class Clock(Model):
        def __init__(self):self.seconds=None
        def tick(self,v):
            if v['reset']:self.seconds=0
            elif v['ena']:self.seconds=(self.seconds+1)%86400
        def output(self,v):
            if self.seconds is None:return dict.fromkeys(('pm','hh','mm','ss'),None)
            h,rest=divmod(self.seconds,3600);m,s=divmod(rest,60);hour=h%12 or 12
            bcd=lambda n:16*(n//10)+n%10
            return {'pm':int(h>=12),'hh':bcd(hour),'mm':bcd(m),'ss':bcd(s)}
    p=Problem('count_clock',body,mask_reasons={n:'Before initial synchronous reset.' for n in ('pm','hh','mm','ss')},explanation='完整24小时状态循环，加使能暂停及未使能时复位；参考使用累计秒数，RTL使用独立BCD进位。')
    cases=[{'reset':1,'ena':0}]+[{'reset':0,'ena':1} for _ in range(86401)]+[{'reset':0,'ena':0} for _ in range(7)]+[{'reset':1,'ena':0},{'reset':0,'ena':1}]
    p.clocked(Clock(),cases);ps.append(p)
    body="always @(posedge clk)begin if(load)q<=data;else case(ena)2'b01:q<={q[0],q[99:1]};2'b10:q<={q[98:0],q[99]};default:q<=q;endcase end"
    def rotation(q,v):
        if v['load']:return v['data']
        if v['ena']==1:return q//2+(q%2)*(1<<99)
        if v['ena']==2:return (q*2)%(1<<100)+q//(1<<99)
        return q
    p=Problem('rotate100',body,procedural=['q'],mask_reasons={'q':'Before first synchronous load.'})
    cases=[{'load':1,'ena':3,'data':1}]+[{'load':0,'ena':1,'data':0} for _ in range(102)]+[{'load':0,'ena':2,'data':0} for _ in range(102)]+cycles_random({'load':1,'ena':2,'data':100},1000)
    p.clocked(RegisterModel(rotation),cases);ps.append(p)
    body="always @(posedge clk)begin if(load)q<=data;else if(ena)case(amount)2'b00:q<=q<<1;2'b01:q<=q<<8;2'b10:q<=$signed(q)>>>1;2'b11:q<=$signed(q)>>>8;endcase end"
    def shifting(q,v):
        if v['load']:return v['data']
        if not v['ena']:return q
        n=8 if v['amount']&1 else 1
        if v['amount']<2:return (q*(2**n))%(1<<64)
        signed=q if q<(1<<63) else q-(1<<64);return (signed//(2**n))%(1<<64)
    p=Problem('shift18',body,procedural=['q'],mask_reasons={'q':'Before first load.'},explanation='负数算术右移按有符号除2的幂向下取整参考；专测符号位、全1、1和移8。')
    cases=[]
    for value in [1,1<<63,(1<<64)-1,0x123456789abcdef0]:
        for amount in range(4):cases += [{'load':1,'ena':1,'amount':amount,'data':value}]+[{'load':0,'ena':1,'amount':amount,'data':0} for _ in range(66)]
    p.clocked(RegisterModel(shifting),cases+cycles_random({'load':1,'ena':1,'amount':2,'data':64},1000));ps.append(p)
    body="reg[4:0]value;assign q=value;always @(posedge clk)if(reset)value<=5'b00001;else value<={value[0],value[4],value[3]^value[0],value[2:1]};"
    p=Problem('lfsr5',body,mask_reasons={'q':'Before initial reset.'},explanation='核对原图Galois抽头5、3：旧bit0反馈到新bit4和新bit2；非Fibonacci式总异或。')
    p.clocked(RegisterModel(lambda q,v:(q>>1)^(0x14 if q&1 else 0),reset='reset',value=1),[{'reset':int(i in (0,95,146))} for i in range(210)]);ps.append(p)
    body="reg[3:0]stages;assign out=stages[3];always @(posedge clk)if(!resetn)stages<=4'b0;else stages<={stages[2:0],in};"
    p=Problem('m2014_q4k',body,mask_reasons={'out':'Before first synchronous reset.'},explanation='图中四个DFF，resetn以题面明确的同步低有效为准。')
    class Shift4(Model):
        def __init__(self):self.values=[None]*4
        def tick(self,v):self.values=[0]*4 if not v['resetn'] else [v['in']]+self.values[:3]
        def output(self,v):return {'out':self.values[-1]}
    p.clocked(Shift4(),cycles_random({'resetn':1,'in':1},600,reset='resetn',active=0));ps.append(p)
    sub='module MUXDFF(input clk,w,R,E,L,output reg Q);always @(posedge clk)if(L)Q<=R;else if(E)Q<=w;endmodule'
    body='MUXDFF u3(KEY[0],KEY[3],SW[3],KEY[1],KEY[2],LEDR[3]);MUXDFF u2(KEY[0],LEDR[3],SW[2],KEY[1],KEY[2],LEDR[2]);MUXDFF u1(KEY[0],LEDR[2],SW[1],KEY[1],KEY[2],LEDR[1]);MUXDFF u0(KEY[0],LEDR[1],SW[0],KEY[1],KEY[2],LEDR[0]);'
    p=Problem('2014_q4b',body,submodules=sub,mask_reasons={'LEDR':'No reset; initial parallel load establishes all four bits.'},explanation='按原图w进入Q[n-1]，向Q0移动；不能误用另一移位题的S→Q0方向。KEY0时钟、KEY1使能、KEY2装载、KEY3串入。')
    def shifted(q,v):return v['SW'] if v['KEY']&4 else (q//2+8*((v['KEY']>>3)&1)) if v['KEY']&2 else q
    cases=[{'SW':10,'KEY':4}]+cycles_random({'SW':4,'KEY':4},1000)
    p.clocked(RegisterModel(shifted,out='LEDR'),cases,clock='KEY',clock_bit=0);ps.append(p)
    body='reg[7:0]storage;always @(posedge clk)if(enable)storage<={storage[6:0],S};assign Z=storage[{A,B,C}];'
    class Lookup(Model):
        def __init__(self):self.bits=[None]*8
        def tick(self,v):
            if v['enable']:self.bits=[v['S']]+self.bits[:7]
        def output(self,v):return {'Z':self.bits[4*v['A']+2*v['B']+v['C']]}
    p=Problem('ece241_2013_q12',body,mask_reasons={'Z':'Unread initial bit until shifted data reaches that position.'},explanation='S进入Q0；MSB先写8拍后得到完整LUT。枚举全部256配置和8个地址，并测试enable保持。')
    cases=[]
    for word in range(256):
        for i in range(7,-1,-1):cases.append({'enable':1,'S':(word>>i)&1,'A':0,'B':0,'C':0})
        for address in range(8):cases.append({'enable':0,'S':1,'A':address>>2,'B':(address>>1)&1,'C':address&1})
    p.clocked(Lookup(),cases);ps.append(p)
    class Automaton(Model):
        def __init__(self,rule):self.word=None;self.rule=rule
        def tick(self,v):
            if v['load']:self.word=v['data'];return
            old='0'+format(self.word,'0512b')+'0';self.word=int(''.join(str((self.rule>>int(old[i:i+3],2))&1) for i in range(512)),2)
        def output(self,v):return {'q':self.word}
    for slug,rule in [('rule90',90),('rule110',110)]:
        if rule==90:body="reg[511:0]cells;assign q=cells;always @(posedge clk)if(load)cells<=data;else cells<={1'b0,cells[511:1]}^{cells[510:0],1'b0};"
        else:body="""reg[511:0]cells;wire[511:0]next_cells;assign q=cells;
function next_bit;input l,c,r;begin case({l,c,r})3'b001,3'b010,3'b011,3'b101,3'b110:next_bit=1;default:next_bit=0;endcase end endfunction
genvar n;generate for(n=0;n<512;n=n+1)begin
if(n==0)assign next_cells[n]=next_bit(cells[n+1],cells[n],1'b0);
else if(n==511)assign next_cells[n]=next_bit(1'b0,cells[n],cells[n-1]);
else assign next_cells[n]=next_bit(cells[n+1],cells[n],cells[n-1]);end endgenerate
always @(posedge clk)if(load)cells<=data;else cells<=next_cells;"""
        p=Problem(slug,body,mask_reasons={'q':'Before initial load.'},explanation='512格、两端固定0；参考按MSB到LSB字符串查规则表，避免复制RTL位移方向。')
        rng=random.Random(260712);words=[0,(1<<512)-1,1,1<<511,1<<255,int('01'*256,2)]+[rng.getrandbits(512) for _ in range(8)];cases=[]
        for word in words:cases += [{'load':1,'data':word}]+[{'load':0,'data':rng.getrandbits(512)} for _ in range(35)]
        p.clocked(Automaton(rule),cases);ps.append(p)
    body="""reg[255:0]cells;wire[255:0]next_cells;assign q=cells;
genvar r,c;generate for(r=0;r<16;r=r+1)begin:rows for(c=0;c<16;c=c+1)begin:cols
wire[3:0]neighbors;
assign neighbors={3'b0,cells[((r+15)%16)*16+(c+15)%16]}+{3'b0,cells[((r+15)%16)*16+c]}+{3'b0,cells[((r+15)%16)*16+(c+1)%16]}+
{3'b0,cells[r*16+(c+15)%16]}+{3'b0,cells[r*16+(c+1)%16]}+
{3'b0,cells[((r+1)%16)*16+(c+15)%16]}+{3'b0,cells[((r+1)%16)*16+c]}+{3'b0,cells[((r+1)%16)*16+(c+1)%16]};
assign next_cells[r*16+c]=(neighbors==3)||((neighbors==2)&&cells[r*16+c]);end end endgenerate
always @(posedge clk)if(load)cells<=data;else cells<=next_cells;"""
    class Life(Model):
        def __init__(self):self.live=None
        def tick(self,v):
            if v['load']:self.live={(i//16,i%16) for i in range(256) if v['data']>>i&1};return
            counts=Counter()
            for r,c in self.live:
                for dr,dc in itertools.product((-1,0,1),repeat=2):
                    if dr or dc:counts[((r+dr)%16,(c+dc)%16)]+=1
            self.live={pos for pos,n in counts.items() if n==3 or (n==2 and pos in self.live)}
        def output(self,v):return {'q':None if self.live is None else sum(1<<(16*r+c) for r,c in self.live)}
    p=Problem('conwaylife',body,mask_reasons={'q':'Before initial load.'},explanation='16×16环面，边界不是固定0；参考采用活细胞坐标集合及邻居贡献计数，与RTL逐格求和不同。')
    pattern=lambda cells:sum(1<<(16*r+c) for r,c in cells)
    rng=random.Random(260713);words=[0,(1<<256)-1,1,pattern([(0,0),(0,15),(15,0),(15,15)]),pattern([(0,15),(0,0),(0,1)]),pattern([(1,2),(2,3),(3,1),(3,2),(3,3)])]+[rng.getrandbits(256) for _ in range(10)];cases=[]
    for word in words:cases += [{'load':1,'data':word}]+[{'load':0,'data':rng.getrandbits(256)} for _ in range(35)]
    p.clocked(Life(),cases);ps.append(p)
    write_jobs(ps)
if __name__=='__main__':main()
