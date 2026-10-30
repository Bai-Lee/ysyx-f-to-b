"""Source-derived state graphs, independent protocol/sequence oracles (HDL119-138)."""
from common import *
from collections import deque


def random_cycles(widths, reset='reset', active=1, n=1000, seed=260720):
    rng=random.Random(seed)
    return [dict({k:rng.getrandbits(w) for k,w in widths.items()}, **{reset:active if i%97==0 else 1-active}) for i in range(n)]


class Graph(Model):
    def __init__(self, table, initial, outputs, encode, reset='reset', active=1, asynchronous=False):
        self.table=table;self.initial=initial;self.outputs=outputs;self.encode=encode
        self.reset=reset;self.active=active;self.is_async=asynchronous;self.state=None
    def asynchronous(self,v):
        if self.is_async and v[self.reset]==self.active:self.state=self.initial
    def tick(self,v):
        self.state=self.initial if v[self.reset]==self.active else self.table[self.state][self.encode(v)]
    def output(self,v):
        return dict.fromkeys(next(iter(self.outputs.values())),None) if self.state is None else self.outputs[self.state]


def graph_cycles(table, initial, decode, reset='reset', active=1):
    """Shortest path to each state, then every outgoing edge and reset from it."""
    paths={initial:[]};queue=deque([initial])
    while queue:
        s=queue.popleft()
        for x,t in enumerate(table[s]):
            if t not in paths:paths[t]=paths[s]+[x];queue.append(t)
    assert len(paths)==len(table), ('unreachable source states',paths,table)
    seq=[]
    for s,path in paths.items():
        for x in range(len(table[s])):
            seq.append(dict(decode(0),**{reset:active}))
            seq += [dict(decode(a),**{reset:1-active}) for a in path+[x]]
            seq.append(dict(decode(x),**{reset:active}))
    return seq


def onehot_next(value, bit, edges):
    result=0
    for state, targets in edges.items():
        if (value>>state)&1:result |= 1<<targets[bit]
    return result


FOUR={0:(0,1),1:(2,1),2:(0,3),3:(2,1)}
HDLC={0:(0,1),1:(0,2),2:(0,3),3:(0,4),4:(0,5),5:(8,6),6:(9,7),7:(0,7),8:(0,1),9:(0,1)}


def main():
    ps=[]
    for slug,async_ in [('fsm1',True),('fsm1s',False)]:
        reset='areset' if async_ else 'reset'
        body=f"reg state;assign out=state;always @(posedge clk{' or posedge areset' if async_ else ''})if({reset})state<=1'b1;else if(!in)state<=~state;"
        p=Problem(slug,body,mask_reasons={'out':'Before initial synchronous reset only.'} if not async_ else {},explanation='A输出0/B输出1；复位B，in=0切换，in=1保持。遍历所有状态/输入/复位。')
        table={0:(1,0),1:(0,1)}
        p.clocked(Graph(table,1,{i:{'out':i} for i in table},lambda v:v['in'],reset=reset,asynchronous=async_),graph_cycles(table,1,lambda i:{'in':i},reset)+random_cycles({'in':1},reset));ps.append(p)
    for slug,async_ in [('fsm2',True),('fsm2s',False)]:
        reset='areset' if async_ else 'reset'
        body=f"reg on;assign out=on;always @(posedge clk{' or posedge areset' if async_ else ''})if({reset})on<=0;else if(on)begin if(k)on<=0;end else if(j)on<=1;"
        table={0:(0,0,1,1),1:(1,0,1,0)};decode=lambda i:{'j':i//2,'k':i%2}
        p=Problem(slug,body,mask_reasons={'out':'Before initial synchronous reset.'} if not async_ else {})
        p.clocked(Graph(table,0,{i:{'out':i} for i in table},lambda v:2*v['j']+v['k'],reset=reset,asynchronous=async_),graph_cycles(table,0,decode,reset)+random_cycles({'j':1,'k':1},reset));ps.append(p)
    next_case="case(state)A:next_state=in?B:A;B:next_state=in?B:C;C:next_state=in?D:A;D:next_state=in?B:C;default:next_state=A;endcase"
    p=Problem('fsm3comb','localparam A=2\'d0,B=2\'d1,C=2\'d2,D=2\'d3;always @* begin '+next_case+' end assign out=(state==D);',procedural=['next_state'])
    p.comb(lambda v:{'next_state':FOUR[v['state']][v['in']],'out':int(v['state']==3)},exhaustive({'state':2,'in':1}));ps.append(p)
    body="assign next_state[0]=~in&(state[0]|state[2]);assign next_state[1]=in&(state[0]|state[1]|state[3]);assign next_state[2]=~in&(state[1]|state[3]);assign next_state[3]=in&state[2];assign out=state[3];"
    p=Problem('fsm3onehot',body,explanation='OR所有入边；全16种state×2输入，包括零状态和多热状态。')
    p.comb(lambda v:{'next_state':onehot_next(v['state'],v['in'],FOUR),'out':v['state']>>3},exhaustive({'state':4,'in':1}));ps.append(p)
    for slug,async_ in [('fsm3',True),('fsm3s',False)]:
        reset='areset' if async_ else 'reset'
        body="localparam A=2'd0,B=2'd1,C=2'd2,D=2'd3;reg[1:0]state,next_state;assign out=(state==D);always @* begin "+next_case+f" end always @(posedge clk{' or posedge areset' if async_ else ''})if({reset})state<=A;else state<=next_state;"
        p=Problem(slug,body,mask_reasons={'out':'Before initial synchronous reset.'} if not async_ else {})
        p.clocked(Graph(FOUR,0,{i:{'out':int(i==3)} for i in FOUR},lambda v:v['in'],reset=reset,asynchronous=async_),graph_cycles(FOUR,0,lambda i:{'in':i},reset)+random_cycles({'in':1},reset));ps.append(p)

    class Water(Model):
        def __init__(self):self.level=None;self.supp=None
        def tick(self,v):
            if v['reset']:self.level=0;self.supp=1;return
            level={0:0,1:1,3:2,7:3}[v['s']]
            if level==0:self.supp=1
            elif level==3:self.supp=0
            elif level!=self.level:self.supp=int(level<self.level)
            self.level=level
        def output(self,v):
            if self.level is None:return dict.fromkeys(('fr3','fr2','fr1','dfr'),None)
            return {'fr3':int(self.level==0),'fr2':int(self.level<2),'fr1':int(self.level<3),'dfr':self.supp}
    body="""localparam LOW=0,M1UP=1,M1DOWN=2,M2UP=3,M2DOWN=4,HIGH=5;
reg[2:0]state,next_state;
always @* begin next_state=state;case(s)
3'b000:next_state=LOW;3'b111:next_state=HIGH;
3'b001:if(state==LOW)next_state=M1UP;else if(state!=M1UP && state!=M1DOWN)next_state=M1DOWN;
3'b011:if(state==HIGH)next_state=M2DOWN;else if(state!=M2UP && state!=M2DOWN)next_state=M2UP;
default:next_state=state;endcase end
always @(posedge clk)if(reset)state<=LOW;else state<=next_state;
assign fr3=(state==LOW);assign fr2=(state==LOW)||(state==M1UP)||(state==M1DOWN);
assign fr1=(state!=HIGH);assign dfr=(state==LOW)||(state==M1DOWN)||(state==M2DOWN);"""
    p=Problem('ece241_2013_q4',body,mask_reasons={n:'Before first synchronous reset.' for n in ('fr3','fr2','fr1','dfr')},explanation='按原扫描图六个Moore状态；Python以数值水位与最近变化方向建模。只给物理可实现温度计码0/1/3/7赋验收含义；测试跨级、保持、升降及复位。')
    seq=[]
    for levels in itertools.product((0,1,3,7),repeat=4):seq += [{'reset':1,'s':0}]+[{'reset':0,'s':s} for s in levels]
    p.clocked(Water(),seq);ps.append(p)

    class Lemming(Model):
        def __init__(self,version):self.version=version;self.direction=0;self.action='walk';self.duration=0
        def asynchronous(self,v):
            if v['areset']:self.direction=0;self.action='walk';self.duration=0
        def tick(self,v):
            if v['areset']:self.asynchronous(v);return
            if self.action=='dead':return
            ground=v.get('ground',1)
            if self.action=='fall':
                if ground:self.action='dead' if self.version==4 and self.duration>20 else 'walk';self.duration=0
                else:self.duration+=1
            elif not ground:self.action='fall';self.duration=1
            elif self.action=='dig':pass
            elif v.get('dig',0):self.action='dig'
            elif v['bump_right' if self.direction else 'bump_left']:self.direction=1-self.direction
        def output(self,v):
            out={'walk_left':int(self.action=='walk' and self.direction==0),'walk_right':int(self.action=='walk' and self.direction==1)}
            if self.version>=2:out['aaah']=int(self.action=='fall')
            if self.version>=3:out['digging']=int(self.action=='dig')
            return out
    for version in range(1,5):
        slug='lemmings'+str(version)
        if version==1:body="reg right;always @(posedge clk or posedge areset)if(areset)right<=0;else if(right?bump_right:bump_left)right<=~right;assign walk_left=~right;assign walk_right=right;"
        else:
            body="localparam LEFT=0,RIGHT=1,FLEFT=2,FRIGHT=3,DLEFT=4,DRIGHT=5,DEAD=6;reg[2:0]state,next_state;"
            if version==4:body+='reg[4:0]fall_count;'
            body+='always @* begin next_state=state;case(state)\nLEFT:if(!ground)next_state=FLEFT;'
            if version>=3:body+='else if(dig)next_state=DLEFT;'
            body+='else if(bump_left)next_state=RIGHT;\nRIGHT:if(!ground)next_state=FRIGHT;'
            if version>=3:body+='else if(dig)next_state=DRIGHT;'
            body+='else if(bump_right)next_state=LEFT;\n'
            body+='FLEFT:if(ground)next_state='+('(fall_count>20)?DEAD:LEFT;' if version==4 else 'LEFT;')+'\n'
            body+='FRIGHT:if(ground)next_state='+('(fall_count>20)?DEAD:RIGHT;' if version==4 else 'RIGHT;')+'\n'
            if version>=3:body+='DLEFT:if(!ground)next_state=FLEFT;DRIGHT:if(!ground)next_state=FRIGHT;\n'
            body+='default:next_state=state;endcase end\nalways @(posedge clk or posedge areset)if(areset)state<=LEFT;else state<=next_state;\n'
            if version==4:
                body+="always @(posedge clk or posedge areset)if(areset)fall_count<=0;else if(state==FLEFT || state==FRIGHT)begin if(!ground && fall_count<21)fall_count<=fall_count+1'b1;end else if(next_state==FLEFT || next_state==FRIGHT)fall_count<=1;else fall_count<=0;\n"
            body+='assign walk_left=(state==LEFT);assign walk_right=(state==RIGHT);assign aaah=(state==FLEFT)||(state==FRIGHT);'
            if version>=3:body+='assign digging=(state==DLEFT)||(state==DRIGHT);'
        p=Problem(slug,body,explanation='独立行为模型保存方向、动作和无界跌落时长；RTL有限状态加饱和计数。专测20/21周期边界、1025周期长跌落、空中不死亡、落地不处理碰撞、fall>dig>bump优先级。' if version==4 else '独立行为模型：落下和落地拍忽略碰撞；挖掘只在地面行走时开始，跌落优先；异步复位恢复向左。')
        widths={'bump_left':1,'bump_right':1}
        if version>=2:widths['ground']=1
        if version>=3:widths['dig']=1
        base={'areset':0,'bump_left':0,'bump_right':0}
        if version>=2:base['ground']=1
        if version>=3:base['dig']=0
        seq=[]
        # Every short control sequence, with reset between episodes.
        options=list(exhaustive(widths))
        for episode in itertools.product(options,repeat=3):seq += [dict(base,areset=1)]+[dict(v,areset=0) for v in episode]
        if version>=2:
            for direction in (0,1):
                for startdig in ((0,1) if version>=3 else (0,)):
                    for duration in [0,1,2,19,20,21,22,31,32,255,256,1025]:
                        seq += [dict(base,areset=1),dict(base,bump_left=direction)]
                        if startdig:seq.append(dict(base,dig=1))
                        seq += [dict(base,ground=0,bump_left=i%2,bump_right=1-i%2,**({'dig':1} if version>=3 else {})) for i in range(duration)]
                        seq += [dict(base,bump_left=1,bump_right=1)]+[dict(base) for _ in range(4)]
        seq += random_cycles(widths,'areset',n=1500)
        p.clocked(Lemming(version),seq);ps.append(p)

    body="""assign next_state[0]=~in&(state[0]|state[1]|state[2]|state[3]|state[4]|state[7]|state[8]|state[9]);
assign next_state[1]=in&(state[0]|state[8]|state[9]);
assign next_state[2]=in&state[1];assign next_state[3]=in&state[2];assign next_state[4]=in&state[3];
assign next_state[5]=in&state[4];assign next_state[6]=in&state[5];assign next_state[7]=in&(state[6]|state[7]);
assign next_state[8]=~in&state[5];assign next_state[9]=~in&state[6];
assign out1=state[8]|state[9];assign out2=state[7]|state[9];"""
    p=Problem('fsm_onehot',body,explanation='逐条按图转录有向边；全1024种state×2输入，任意多热输入按入边OR，不加非法状态纠错。')
    p.comb(lambda v:{'next_state':onehot_next(v['state'],v['in'],HDLC),'out1':int(bool(v['state']&0x300)),'out2':int(bool(v['state']&0x280))},exhaustive({'state':10,'in':1}));ps.append(p)

    class PS2(Model):
        def __init__(self,data):self.parts=[];self.done=None;self.value=None;self.data=data
        def tick(self,v):
            self.done=0
            if v['reset']:self.parts=[];self.value=None;return
            if self.parts or v['in']&8:self.parts.append(v['in'])
            if len(self.parts)==3:self.value=int.from_bytes(bytes(self.parts),'big');self.parts=[];self.done=1
        def output(self,v):
            out={'done':self.done}
            if self.data:out['out_bytes']=self.value if self.done else None
            return out
    for slug,data in [('fsm_ps2',False),('fsm_ps2data',True)]:
        body="localparam SEEK=0,SECOND=1,THIRD=2;reg[1:0]state;"
        if data:body+='reg[7:0]first,second;'
        body+='always @(posedge clk)begin if(reset)begin state<=SEEK;done<=0;end else begin done<=0;case(state)\nSEEK:if(in[3])begin state<=SECOND;'+('first<=in;' if data else '')+'end\nSECOND:begin state<=THIRD;'+('second<=in;' if data else '')+'end\nTHIRD:begin state<=SEEK;done<=1;'+('out_bytes<={first,second,in};' if data else '')+'end\ndefault:state<=SEEK;endcase end end'
        masks={'done':'Before initial synchronous reset.'}
        if data:masks['out_bytes']='Task explicitly defines out_bytes only when done=1; done always checked after reset.'
        p=Problem(slug,body,procedural=['done']+(['out_bytes'] if data else []),mask_reasons=masks,explanation='独立三字节列表解析；第一字节bit3同步，后两字节不作同步条件；支持连续包，done与第三字节采样对应。')
        seq=[{'reset':1,'in':0}]
        for first in range(256):
            if first&8:
                for second,third in [(0,0),(8,8),(255,255),(first^255,first),(first,first^255)]:seq += [{'reset':0,'in':b} for b in (first,second,third)]
            else:seq.append({'reset':0,'in':first})
        for value in range(256):seq += [{'reset':0,'in':b} for b in (0x98,value,255-value)]
        for n in (0,1,2):seq += [{'reset':1,'in':0}]+[{'reset':0,'in':b} for b in (0x8f,0xa4)[:n]]+[{'reset':1,'in':255}]+[{'reset':0,'in':b} for b in (0x18,0x23,0x45)]
        seq += random_cycles({'in':8},n=2000)
        p.clocked(PS2(data),seq);ps.append(p)

    class Serial(Model):
        def __init__(self,data,parity):self.data=data;self.parity=parity;self.bits=None;self.wait_high=False;self.done=None;self.value=None
        def tick(self,v):
            self.done=0
            if v['reset']:self.bits=None;self.wait_high=False;self.value=None;return
            b=v['in']
            if self.wait_high:
                if b:self.wait_high=False
                return
            if self.bits is None:
                if b==0:self.bits=[]
            elif len(self.bits)<8+int(self.parity):self.bits.append(b)
            else:
                if b and (not self.parity or sum(self.bits)%2==1):self.done=1;self.value=sum(bit<<i for i,bit in enumerate(self.bits[:8]))
                if not b:self.wait_high=True
                self.bits=None
        def output(self,v):
            out={'done':self.done}
            if self.data:out['out_byte']=self.value if self.done else None
            return out
    for slug,data,parity in [('fsm_serial',False,False),('fsm_serialdata',True,False),('fsm_serialdp',True,True)]:
        body="localparam IDLE=0,DATA=1,PARITY=2,STOP=3,RECOVER=4;reg[2:0]state,bit_index;"
        if data:body+='reg[7:0]payload;'
        if parity:body+="wire odd;wire parity_reset=reset || (state!=DATA && state!=PARITY);parity parity_accumulator(clk,parity_reset,in,odd);"
        body+='always @(posedge clk)begin if(reset)begin state<=IDLE;bit_index<=0;done<=0;end else begin done<=0;case(state)\nIDLE:if(!in)begin state<=DATA;bit_index<=0;end\nDATA:begin '+('payload[bit_index]<=in;' if data else '')+"if(bit_index==7)state<="+('PARITY' if parity else 'STOP')+";else bit_index<=bit_index+1'b1;end\n"
        if parity:body+='PARITY:state<=STOP;\n'
        body+='STOP:begin if(in)begin state<=IDLE;'+('if(odd)begin ' if parity else '')+'done<=1;'+('out_byte<=payload;' if data else '')+('end ' if parity else '')+'end else state<=RECOVER;end\nRECOVER:if(in)state<=IDLE;default:state<=IDLE;endcase end end'
        support='module parity(input clk,reset,in,output reg odd);always @(posedge clk)if(reset)odd<=0;else if(in)odd<=~odd;endmodule' if parity else ''
        masks={'done':'Before initial synchronous reset.'}
        if data:masks['out_byte']='Specified only in the valid done cycle; invalid/no-frame bytes are not judged.'
        p=Problem(slug,body,procedural=['done']+(['out_byte'] if data else []),support=support,mask_reasons=masks,explanation='独立帧位列表、奇数个1计数和恢复条件参考；全256数据、连续帧、坏停止位、奇偶错误、逐相位复位。LSB先到；停止位不进入奇偶校验。')
        def frame(byte,goodpar=True,stop=1):
            bits=[0]+[(byte>>i)&1 for i in range(8)]
            if parity:bits.append((1-(byte.bit_count()%2))^int(not goodpar))
            return bits+[stop]
        seq=[{'reset':1,'in':1}]
        def push(bits):seq.extend({'reset':0,'in':b} for b in bits)
        for value in range(256):push(frame(value))
        if parity:
            for value in range(256):push(frame(value,False));push(frame(value^255))
        for value in (0,1,0x80,0x55,0xaa,255):
            push(frame(value,stop=0));push([0]*23+[1]);push(frame(value))
        for cut in range(12 if parity else 11):
            seq.append({'reset':1,'in':1});push(frame(0xa5)[:cut]);seq.append({'reset':1,'in':0});push([1,1]);push(frame(0x96))
        seq += random_cycles({'in':1},n=1800)
        p.clocked(Serial(data,parity),seq);ps.append(p)

    body="""reg[3:0]state,next_state;
always @* begin case(state)
0:next_state=in?1:0;1:next_state=in?2:0;2:next_state=in?3:0;3:next_state=in?4:0;
4:next_state=in?5:0;5:next_state=in?6:8;6:next_state=in?7:9;
7:next_state=in?7:0;8:next_state=in?1:0;9:next_state=in?1:0;default:next_state=0;endcase end
always @(posedge clk)if(reset)state<=0;else state<=next_state;
assign disc=(state==8);assign flag=(state==9);assign err=(state==7);"""
    class Hdlc(Model):
        def __init__(self):self.ones=0;self.events=None
        def tick(self,v):
            if v['reset']:self.ones=0;self.events={'disc':0,'flag':0,'err':0};return
            bit=v['in'];old=self.ones;self.ones=old+1 if bit else 0
            self.events={'disc':int(not bit and old==5),'flag':int(not bit and old==6),'err':int(bit and self.ones>=7)}
        def output(self,v):return self.events if self.events is not None else dict.fromkeys(('disc','flag','err'),None)
    p=Problem('fsm_hdlc',body,mask_reasons={x:'Before initial synchronous reset.' for x in ('disc','flag','err')},explanation='RTL显式十状态；参考无界连续1计数。5个1+0丢弃，6个1+0标记，至少7个1持续错误，0清除。')
    seq=[]
    for bits in itertools.product((0,1),repeat=8):seq += [{'reset':1,'in':0}]+[{'reset':0,'in':x} for x in bits]
    for n in list(range(13))+[31,32,255,1025]:seq += [{'reset':1,'in':0}]+[{'reset':0,'in':1} for _ in range(n)]+[{'reset':0,'in':0}]*2
    seq += graph_cycles(HDLC,0,lambda i:{'in':i})+random_cycles({'in':1},n=2000)
    p.clocked(Hdlc(),seq);ps.append(p)
    write_jobs(ps)


if __name__=='__main__':main()
