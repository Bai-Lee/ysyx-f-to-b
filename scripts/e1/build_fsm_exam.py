"""Exam FSMs: diagram-transcribed RTL vs history, arithmetic and event oracles."""
from common import *
from build_fsm_core import Graph,graph_cycles,random_cycles,onehot_next

TABLE5={0:(0,1),1:(1,4),2:(2,1),3:(1,2),4:(3,4)}
# Tables independently transcribed from the two source images (labels differ).
GRAPH2014={0:(1,0),1:(2,3),2:(4,3),3:(5,0),4:(4,3),5:(2,3)}
GRAPH2012={0:(0,1),1:(3,2),2:(3,4),3:(0,5),4:(3,4),5:(3,2)}


def sequences(width=8,reset='areset',active=1,name='x'):
    for bits in itertools.product((0,1),repeat=width):
        yield {reset:active,name:0}
        for bit in bits:yield {reset:1-active,name:bit}


def main():
    ps=[]
    class Detector(Model):
        def __init__(self):self.history=[]
        def asynchronous(self,v):
            if not v['aresetn']:self.history=[]
        def tick(self,v):
            if not v['aresetn']:self.history=[]
            else:self.history=(self.history+[v['x']])[-2:]
        def output(self,v):return {'z':int(self.history+[v['x']]==[1,0,1])}
    body="""localparam EMPTY=0,ONE=1,ONE_ZERO=2;reg[1:0]state,next_state;
always @* begin case(state)EMPTY:next_state=x?ONE:EMPTY;ONE:next_state=x?ONE:ONE_ZERO;
ONE_ZERO:next_state=x?ONE:EMPTY;default:next_state=EMPTY;endcase end
always @(posedge clk or negedge aresetn)if(!aresetn)state<=EMPTY;else state<=next_state;
assign z=(state==ONE_ZERO)&&x;"""
    p=Problem('ece241_2013_q8',body,explanation='恰好三个Mealy状态，异步低有效复位；独立历史串检测101，覆盖重叠10101及输入改变到时钟沿之间的组合输出。')
    p.clocked(Detector(),list(sequences(reset='aresetn',active=0))+random_cycles({'x':1},'aresetn',0));ps.append(p)

    class Complement(Model):
        def __init__(self,mealy):self.prefix=0;self.length=0;self.last=0;self.mealy=mealy
        def asynchronous(self,v):
            if v['areset']:self.prefix=0;self.length=0;self.last=0
        def tick(self,v):
            if v['areset']:self.asynchronous(v);return
            self.prefix+=v['x']<<self.length
            self.last=((-self.prefix)%(1<<(self.length+1)))>>self.length
            self.length+=1
        def output(self,v):
            value=((- (self.prefix+(v['x']<<self.length)))%(1<<(self.length+1)))>>self.length if self.mealy else self.last
            return {'z':value}
    body="""localparam BEFORE_ONE=0,OUT_ONE=1,OUT_ZERO=2;reg[1:0]state,next_state;
always @* begin case(state)BEFORE_ONE:next_state=x?OUT_ONE:BEFORE_ONE;
OUT_ONE,OUT_ZERO:next_state=x?OUT_ZERO:OUT_ONE;default:next_state=BEFORE_ONE;endcase end
always @(posedge clk or posedge areset)if(areset)state<=BEFORE_ONE;else state<=next_state;
assign z=(state==OUT_ONE);"""
    p=Problem('ece241_2014_q5a',body,explanation='Moore两补数转换，LSB先到；参考直接计算任意精度负整数的当前位，不复制RTL状态转移。')
    seq=list(sequences())+[{'areset':1,'x':0}]+[{'areset':0,'x':0}]*64+[{'areset':0,'x':1}]+[{'areset':0,'x':i%2} for i in range(512)]
    p.clocked(Complement(False),seq);ps.append(p)
    body="""localparam A=2'b01,B=2'b10;reg[1:0]state,next_state;
always @* begin next_state[0]=state[0]&~x;next_state[1]=state[1]|(state[0]&x);end
always @(posedge clk or posedge areset)if(areset)state<=A;else state<=next_state;
assign z=(state[0]&x)|(state[1]&~x);"""
    p=Problem('ece241_2014_q5b',body,explanation='按原图两状态one-hot Mealy实现；整数取负参考计算当前输入对应的组合输出，复位只改变状态，不额外屏蔽x。')
    p.clocked(Complement(True),seq);ps.append(p)

    class Groups(Model):
        def __init__(self):self.active=False;self.samples=[];self.z=None
        def tick(self,v):
            if v['reset']:self.active=False;self.samples=[];self.z=0;return
            self.z=0
            if not self.active:
                if v['s']:self.active=True
            else:
                self.samples.append(v['w'])
                if len(self.samples)==3:self.z=int(sum(self.samples)==2);self.samples=[]
        def output(self,v):return {'z':self.z}
    body="""localparam A=0,B=1,C=2,D=3,E=4,F=5,G=6,H=7;reg[2:0]state,next_state;
always @* begin case(state)
A:next_state=s?B:A;B,H:next_state=w?D:C;C:next_state=w?F:E;D:next_state=w?G:F;
E:next_state=B;F:next_state=w?H:B;G:next_state=w?B:H;default:next_state=A;endcase end
always @(posedge clk)if(reset)state<=A;else state<=next_state;
assign z=(state==H);"""
    p=Problem('2014_q3fsm',body,mask_reasons={'z':'Before initial synchronous reset.'},explanation='八个Moore状态；s仅启动，启动拍不消费w。随后每三个不重叠采样恰好两个1时输出一拍。独立列表计数参考并核对原WaveDrom。')
    seq=[]
    for bits in itertools.product((0,1),repeat=9):seq += [{'reset':1,'s':0,'w':1},{'reset':0,'s':0,'w':1},{'reset':0,'s':1,'w':1}]+[{'reset':0,'s':i%2,'w':bit} for i,bit in enumerate(bits)]
    seq += random_cycles({'s':1,'w':1})
    p.clocked(Groups(),seq);ps.append(p)

    case5="case(state)0:next_state=x?1:0;1:next_state=x?4:1;2:next_state=x?1:2;3:next_state=x?2:1;4:next_state=x?4:3;default:next_state=0;endcase"
    p=Problem('2014_q3bfsm',"reg[2:0]state,next_state;always @* begin "+case5+" end always @(posedge clk)if(reset)state<=0;else state<=next_state;assign z=(state==3)||(state==4);",mask_reasons={'z':'Before initial synchronous reset.'})
    p.clocked(Graph(TABLE5,0,{i:{'z':int(i in (3,4))} for i in TABLE5},lambda v:v['x']),graph_cycles(TABLE5,0,lambda i:{'x':i})+random_cycles({'x':1}));ps.append(p)
    p=Problem('2014_q3c','wire[2:0]state=y;reg[2:0]next_state;always @* begin '+case5+' end assign Y0=next_state[0];assign z=(y==3)||(y==4);',mask_reasons={'Y0':'Source table assigns no behavior to y=5,6,7.','z':'Source table assigns no behavior to y=5,6,7.'},explanation='只实现表中的组合Y0与z；clk是题面保留端口，没有触发器。未定义编码不擅自成为验收规格。')
    p.comb(lambda v:{'Y0':TABLE5[v['y']][v['x']]&1,'z':int(v['y'] in (3,4))} if v['y'] in TABLE5 else {'Y0':None,'z':None},exhaustive({'clk':1,'y':3,'x':1}));ps.append(p)

    # Binary and one-hot equations are authored separately from source-table oracles.
    body="reg[2:0]next_state;always @* begin case(y)0:next_state=w?0:1;1:next_state=w?3:2;2:next_state=w?3:4;3:next_state=w?0:5;4:next_state=w?3:4;5:next_state=w?3:2;default:next_state=0;endcase end assign Y2=next_state[1];"
    p=Problem('m2014_q6b',body,mask_reasons={'Y2':'Unused binary encodings6/7 are unspecified.'},explanation='y[3:1]和Y2：输出中间位，等于紧凑编码的bit1，不能误当bit2。')
    p.comb(lambda v:{'Y2':(GRAPH2014[v['y']][v['w']]>>1)&1 if v['y'] in GRAPH2014 else None},exhaustive({'y':3,'w':1}));ps.append(p)
    p=Problem('m2014_q6c','assign Y2=~w&y[1];assign Y4=w&(y[2]|y[3]|y[5]|y[6]);',explanation='one-hot端口下标从1开始：Y2为B、Y4为D；所有64种零/多热组合也按入边OR验证。')
    p.comb(lambda v:{'Y2':(onehot_next(v['y'],v['w'],GRAPH2014)>>1)&1,'Y4':(onehot_next(v['y'],v['w'],GRAPH2014)>>3)&1},exhaustive({'y':6,'w':1}));ps.append(p)
    for slug,table,case in [
        ('m2014_q6',GRAPH2014,'A:next_state=w?A:B;B:next_state=w?D:C;C:next_state=w?D:E;D:next_state=w?A:F;E:next_state=w?D:E;F:next_state=w?D:C;'),
        ('2012_q2fsm',GRAPH2012,'A:next_state=w?B:A;B:next_state=w?C:D;C:next_state=w?E:D;D:next_state=w?F:A;E:next_state=w?E:D;F:next_state=w?C:D;')]:
        body="localparam A=0,B=1,C=2,D=3,E=4,F=5;reg[2:0]state,next_state;always @* begin case(state)"+case+'default:next_state=A;endcase end always @(posedge clk)if(reset)state<=A;else state<=next_state;assign z=(state==E)||(state==F);'
        p=Problem(slug,body,mask_reasons={'z':'Before initial synchronous reset.'},explanation='按各自原图逐边转录，六状态Moore；组合转移与时序寄存器分开always。覆盖全部状态/入边、同步复位与随机长序列。')
        p.clocked(Graph(table,0,{i:{'z':int(i in (4,5))} for i in table},lambda v:v['w']),graph_cycles(table,0,lambda i:{'w':i})+random_cycles({'w':1}));ps.append(p)
    p=Problem('2012_q2b','assign Y1=w&y[0];assign Y3=~w&(y[1]|y[2]|y[4]|y[5]);',explanation='另一张图的输入标签与2014题不同；这里端口从0起，下标1为B、3为D。所有64种state均按OR入边。')
    p.comb(lambda v:{'Y1':(onehot_next(v['y'],v['w'],GRAPH2012)>>1)&1,'Y3':(onehot_next(v['y'],v['w'],GRAPH2012)>>3)&1},exhaustive({'y':6,'w':1}));ps.append(p)

    class Arbiter(Model):
        def __init__(self):self.owner=None
        def tick(self,v):
            if not v['resetn']:self.owner=0
            elif self.owner:
                if not v['r']&(1<<(self.owner-1)):self.owner=0
            else:
                requests=[i+1 for i in range(3) if v['r']&(1<<i)]
                self.owner=min(requests) if requests else 0
        def output(self,v):return {'g':None if self.owner is None else (1<<(self.owner-1) if self.owner else 0)}
    body="""localparam IDLE=0,G1=1,G2=2,G3=3;reg[1:0]state,next_state;
always @* begin next_state=state;case(state)
IDLE:if(r[1])next_state=G1;else if(r[2])next_state=G2;else if(r[3])next_state=G3;
G1:if(!r[1])next_state=IDLE;G2:if(!r[2])next_state=IDLE;G3:if(!r[3])next_state=IDLE;endcase end
always @(posedge clk)if(!resetn)state<=IDLE;else state<=next_state;
assign g[1]=(state==G1);assign g[2]=(state==G2);assign g[3]=(state==G3);"""
    p=Problem('2013_q2afsm',body,mask_reasons={'g':'Before initial active-low synchronous reset.'},explanation='设备1优先；已有授权不可抢占；释放请求先回A空闲一拍，再重新仲裁，按原图保留这个空拍。')
    seq=[]
    for reqs in itertools.product(range(8),repeat=4):seq += [{'resetn':0,'r':7}]+[{'resetn':1,'r':r} for r in reqs]
    p.clocked(Arbiter(),seq+random_cycles({'r':3},'resetn',0));ps.append(p)

    class Motor(Model):
        def __init__(self):self.phase=None;self.samples=[];self.waited=0
        def tick(self,v):
            if not v['resetn']:self.phase='start';self.samples=[];self.waited=0;return
            if self.phase=='start':self.phase='pulse'
            elif self.phase=='pulse':self.phase='search'
            elif self.phase=='search':
                self.samples=(self.samples+[v['x']])[-3:]
                if self.samples==[1,0,1]:self.phase='wait';self.waited=0
            elif self.phase=='wait':
                self.waited+=1
                if v['y']:self.phase='success'
                elif self.waited==2:self.phase='failed'
        def output(self,v):return {'f':None if self.phase is None else int(self.phase=='pulse'),'g':None if self.phase is None else int(self.phase in ('wait','success'))}
    body="""localparam A=0,B=1,C=2,D=3,E=4,F=5,G=6,H=7,I=8;reg[3:0]state,next_state;
always @* begin case(state)
A:next_state=B;B:next_state=C;C:next_state=x?D:C;D:next_state=x?D:E;E:next_state=x?F:C;
F:next_state=y?H:G;G:next_state=y?H:I;H:next_state=H;I:next_state=I;default:next_state=A;endcase end
always @(posedge clk)if(!resetn)state<=A;else state<=next_state;
assign f=(state==B);assign g=(state==F)||(state==G)||(state==H);"""
    p=Problem('2013_q2bfsm',body,mask_reasons={'f':'Before first synchronous reset.','g':'Before first synchronous reset.'},explanation='f脉冲结束后才采x；检测101后g高时才开始两拍y窗口。分别验早到/首拍/第二拍/迟到y、永久成功/失败、所有阶段复位。参考历史串和截止时限，不复制RTL状态图。')
    seq=[]
    for xbits in itertools.product((0,1),repeat=6):
        for ybits in itertools.product((0,1),repeat=5):
            seq += [{'resetn':0,'x':1,'y':1},{'resetn':1,'x':1,'y':1},{'resetn':1,'x':1,'y':1}]
            seq += [{'resetn':1,'x':x,'y':1} for x in xbits]
            seq += [{'resetn':1,'x':i%2,'y':y} for i,y in enumerate(ybits)]
            seq += [{'resetn':1,'x':1,'y':0}]*3
    for success in (0,1):
        sample=[{'resetn':0,'x':0,'y':0}]+[{'resetn':1,'x':x,'y':success if i>=5 else 0} for i,x in enumerate([0,0,1,0,1,0,0,1,0,1,0,0])]
        for cut in range(1,len(sample)+1):seq += sample[:cut]+[{'resetn':0,'x':1,'y':1}]+sample[1:]
    seq += random_cycles({'x':1,'y':1},'resetn',0,n=3000)
    p.clocked(Motor(),seq);ps.append(p)
    write_jobs(ps)


if __name__=='__main__':main()
