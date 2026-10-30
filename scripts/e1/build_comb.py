from common import *

def make(slug,body,oracle,widths=None,case_list=None,procedural=(),submodules='',support='',compile_support=None,extra_inputs=None,checks='',explanation=''):
    p=Problem(slug,body,procedural,submodules,support,compile_support,extra_inputs,checks,explanation)
    widths=widths or {x['name']:x['width'] for x in p.ins+p.extra}
    cases=case_list if case_list is not None else exhaustive(widths) if sum(widths.values())<=16 else random_cases(widths)
    p.comb(oracle,cases);return p

def main():
    ps=[]
    ps += [make('step_one',"assign one = 1'b1;",lambda v:{'one':1},case_list=[{},{}],explanation='常量1，连续驱动输出。'),make('zero',"assign zero = 1'b0;",lambda v:{'zero':0},case_list=[{},{}]),make('wire','assign out = in;',lambda v:{'out':v['in']}),make('wire4','assign w=a;assign x=b;assign y=b;assign z=c;',lambda v:dict(w=v['a'],x=v['b'],y=v['b'],z=v['c']))]
    for slug,body,oracle in [('notgate','~in',lambda v:1-v['in']),('andgate','a & b',lambda v:int(v['a']==v['b']==1)),('norgate','~(a | b)',lambda v:int(not(v['a'] or v['b']))),('xnorgate','~(a ^ b)',lambda v:int(v['a']==v['b']))]:ps.append(make(slug,'assign out = '+body+';',lambda v,f=oracle:{'out':f(v)}))
    ps.append(make('wire_decl','wire ab,cd;assign ab=a&b;assign cd=c&d;assign out=ab|cd;assign out_n=~out;',lambda v:{'out':int((v['a'] and v['b']) or (v['c'] and v['d'])),'out_n':int(not((v['a'] and v['b']) or (v['c'] and v['d'])))},explanation='原图两组AND汇入OR，out再取反；中间导线显式声明。'))
    ps.append(make('7458','wire aa,ab,ba,bb;assign aa=p1a&p1b&p1c;assign ab=p1d&p1e&p1f;assign ba=p2a&p2b;assign bb=p2c&p2d;assign p1y=aa|ab;assign p2y=ba|bb;',lambda v:{'p1y':int(all(v[k] for k in ('p1a','p1b','p1c')) or all(v[k] for k in ('p1d','p1e','p1f'))),'p2y':int((v['p2a'] and v['p2b']) or (v['p2c'] and v['p2d']))},explanation='逐引脚核对7458原图：两个三输入AND和两个二输入AND分别汇入两个OR。'))
    ps.append(make('vector0','assign outv=vec;assign {o2,o1,o0}=vec;',lambda v:dict(outv=v['vec'],o2=(v['vec']>>2)&1,o1=(v['vec']>>1)&1,o0=v['vec']&1)))
    ps.append(make('vector1','assign out_hi=in[15:8];assign out_lo=in[7:0];',lambda v:{'out_hi':v['in']//256,'out_lo':v['in']%256}))
    ps.append(make('vector2','assign out={in[7:0],in[15:8],in[23:16],in[31:24]};',lambda v:{'out':int.from_bytes(v['in'].to_bytes(4,'little'),'big')}))
    ps.append(make('vectorgates','assign out_or_bitwise=a|b;assign out_or_logical=a||b;assign out_not={~b,~a};',lambda v:{'out_or_bitwise':v['a']|v['b'],'out_or_logical':int(bool(v['a'] or v['b'])),'out_not':(7-v['b'])*8+(7-v['a'])}))
    ps.append(make('gates4','assign out_and=&in;assign out_or=|in;assign out_xor=^in;',lambda v:{'out_and':int(v['in']==15),'out_or':int(v['in']!=0),'out_xor':v['in'].bit_count()%2}))
    def concat(v):
        bitstring=''.join(format(v[k],'05b') for k in 'abcdef')+'11';chunks=[int(bitstring[i:i+8],2) for i in range(0,32,8)];return dict(zip('wxyz',chunks))
    ps.append(make('vector3',"assign {w,x,y,z}={a,b,c,d,e,f,2'b11};",concat,explanation='30输入位按a到f顺序拼接，再附两个1；独立按字符串分组检验。'))
    ps.append(make('vectorr','genvar i;generate for(i=0;i<8;i=i+1)begin assign out[i]=in[7-i];end endgenerate',lambda v:{'out':int(format(v['in'],'08b')[::-1],2)}))
    ps.append(make('vector4','assign out={{24{in[7]}},in};',lambda v:{'out':(v['in'] if v['in']<128 else v['in']-256)&0xffffffff}))
    def pairwise(v):
        values=[v[k] for k in 'abcde'];s=''.join('1' if a==b else '0' for a in values for b in values);return {'out':int(s,2)}
    ps.append(make('vector5','assign out=~({{5{a}},{5{b}},{5{c}},{5{d}},{5{e}}}^{5{a,b,c,d,e}});',pairwise))
    for slug in ['module','module_pos','module_name']:
        if slug=='module':
            body='mod_a u(.in1(a),.in2(b),.out(out));';support='module mod_a(input in1,in2,output out);assign out=tb.v_stub0;endmodule';syntax='module mod_a(input in1,in2,output out);assign out=1\'b0;endmodule';oracle=lambda v:{'out':v['stub0']};extras={'stub0':1};checks='if(dut.u.in1!==v_a||dut.u.in2!==v_b)$fatal(1,"MISMATCH module input mapping");'
        else:
            body='mod_a u(out1,out2,a,b,c,d);' if slug=='module_pos' else 'mod_a u(.in4(d),.out2(out2),.in1(a),.in3(c),.out1(out1),.in2(b));'
            decl='output out1,out2,input in1,in2,in3,in4' if slug=='module_pos' else 'input in3,output out2,input in2,output out1,input in4,in1'
            support='module mod_a('+decl+');assign out1=tb.v_stub0;assign out2=tb.v_stub1;endmodule';syntax='module mod_a('+decl+');assign out1=0;assign out2=0;endmodule';oracle=lambda v:{'out1':v['stub0'],'out2':v['stub1']};extras={'stub0':1,'stub1':1};checks='if(dut.u.in1!==v_a||dut.u.in2!==v_b||dut.u.in3!==v_c||dut.u.in4!==v_d)$fatal(1,"MISMATCH module input mapping");'
        ps.append(make(slug,body,oracle,support=support,compile_support=syntax,extra_inputs=extras,checks=checks,explanation='题面未给黑盒内部逻辑，测试独立驱动其输出并直接核验每个输入连接；不假造黑盒功能。按名称题还置换fixture端口顺序。'))
    add16='module add16(input[15:0]a,b,input cin,output[15:0]sum,output cout);assign {cout,sum}={1\'b0,a}+{1\'b0,b}+cin;endmodule'
    base='wire carry;add16 lo(.a(a[15:0]),.b(b[15:0]),.cin(1\'b0),.sum(sum[15:0]),.cout(carry));add16 hi(.a(a[31:16]),.b(b[31:16]),.cin(carry),.sum(sum[31:16]),.cout());'
    submodule='module add1(input a,b,cin,output sum,cout);assign sum=a^b^cin;assign cout=(a&b)|(a&cin)|(b&cin);endmodule'
    adder_support='module add16(input[15:0]a,b,input cin,output[15:0]sum,output cout);wire[16:0]c;assign c[0]=cin;assign cout=c[16];genvar n;generate for(n=0;n<16;n=n+1)begin add1 f(a[n],b[n],c[n],sum[n],c[n+1]);end endgenerate endmodule'
    vals=[{'a':a,'b':b} for a,b in [(0xffffffff,1),(0x0000ffff,1),(0xffff0000,0x10000),(0x7fffffff,1),(0,0)]]+list(random_cases({'a':32,'b':32},600))
    ps.append(make('module_add',base,lambda v:{'sum':(v['a']+v['b'])&0xffffffff},case_list=vals,support=add16,explanation='两个16位加法器低半部向高半部传递进位；公开add16契约由离线fixture补齐。'))
    ps.append(make('module_fadd',base,lambda v:{'sum':(v['a']+v['b'])&0xffffffff},case_list=vals,support=adder_support,submodules=submodule,explanation='top实例化两个add16；测试提供的add16分别实例化16个本题自写add1，完整两级层次。'))
    body="wire carry;wire[15:0]s0,s1;add16 lo(a[15:0],b[15:0],1'b0,sum[15:0],carry);add16 hi0(a[31:16],b[31:16],1'b0,s0,);add16 hi1(a[31:16],b[31:16],1'b1,s1,);assign sum[31:16]=carry?s1:s0;"
    ps.append(make('module_cseladd',body,lambda v:{'sum':(v['a']+v['b'])&0xffffffff},case_list=vals,support=add16,explanation='三个add16，上半部预先计算cin0/1并用低半部进位选择。'))
    body='wire[31:0]modified_b;wire carry;assign modified_b=b^{32{sub}};add16 lo(a[15:0],modified_b[15:0],sub,sum[15:0],carry);add16 hi(a[31:16],modified_b[31:16],carry,sum[31:16],);'
    ps.append(make('module_addsub',body,lambda v:{'sum':(v['a']-v['b'] if v['sub'] else v['a']+v['b'])&0xffffffff},support=add16))
    ps.append(make('alwaysblock1','assign out_assign=a&b;always @* out_alwaysblock=a&b;',lambda v:dict(out_assign=v['a']*v['b'],out_alwaysblock=v['a']*v['b']),procedural=['out_alwaysblock']))
    ps.append(make('always_if','assign out_assign=(sel_b1&&sel_b2)?b:a;always @* begin if(sel_b1&&sel_b2)out_always=b;else out_always=a;end',lambda v:{n:v['b'] if v['sel_b1'] and v['sel_b2'] else v['a'] for n in ('out_assign','out_always')},procedural=['out_always']))
    ps.append(make('always_if2','always @* begin if(cpu_overheated)shut_off_computer=1;else shut_off_computer=0;if(!arrived && !gas_tank_empty)keep_driving=1;else keep_driving=0;end',lambda v:dict(shut_off_computer=v['cpu_overheated'],keep_driving=int(not v['arrived'] and not v['gas_tank_empty'])),procedural=['shut_off_computer','keep_driving']))
    body="always @* begin case(sel)3'd0:out=data0;3'd1:out=data1;3'd2:out=data2;3'd3:out=data3;3'd4:out=data4;3'd5:out=data5;default:out=4'd0;endcase end"
    cases=[];rng=random.Random(260703)
    for n in range(120):
        data={f'data{i}':rng.randrange(16) for i in range(6)}
        for sel in range(8):cases.append({**data,'sel':sel})
    ps.append(make('always_case',body,lambda v:{'out':v.get('data'+str(v['sel']),0)},case_list=cases,procedural=['out']))
    body="always @* begin case(in)4'b0001,4'b0011,4'b0101,4'b0111,4'b1001,4'b1011,4'b1101,4'b1111:pos=0;4'b0010,4'b0110,4'b1010,4'b1110:pos=1;4'b0100,4'b1100:pos=2;4'b1000:pos=3;default:pos=0;endcase end"
    low=lambda x:next((i for i in range(8) if x&(1<<i)),0)
    ps.append(make('always_case2',body,lambda v:{'pos':low(v['in'])},procedural=['pos'],explanation='与F阶段高位优先不同：本题最低有效位优先。'))
    body='always @* begin casez(in)'+''.join(f"8'b{'?'*(7-i)}1{'0'*i}:pos=3'd{i};" for i in range(8))+"default:pos=3'd0;endcase end"
    ps.append(make('always_casez',body,lambda v:{'pos':low(v['in'])},procedural=['pos']))
    body="always @* begin {left,down,right,up}=4'b0;case(scancode)16'he06b:left=1;16'he072:down=1;16'he074:right=1;16'he075:up=1;default:begin end endcase end"
    ps.append(make('always_nolatches',body,lambda v:{k:int(v['scancode']==n) for k,n in [('left',0xe06b),('down',0xe072),('right',0xe074),('up',0xe075)]},procedural=['left','down','right','up'],explanation='穷举全部16位扫描码，四个输出在每次输入下都有确定赋值。'))
    ps.append(make('conditional','wire[7:0]m0,m1;assign m0=a<b?a:b;assign m1=c<d?c:d;assign min=m0<m1?m0:m1;',lambda v:{'min':min(v.values())}))
    ps.append(make('reduction','assign parity=^in;',lambda v:{'parity':v['in'].bit_count()%2}))
    ps.append(make('gates100','assign out_and=&in;assign out_or=|in;assign out_xor=^in;',lambda v:{'out_and':int(v['in']==(1<<100)-1),'out_or':int(v['in']!=0),'out_xor':v['in'].bit_count()%2}))
    ps.append(make('vector100r','genvar n;generate for(n=0;n<100;n=n+1)begin assign out[n]=in[99-n];end endgenerate',lambda v:{'out':int(format(v['in'],'0100b')[::-1],2)}))
    ps.append(make('popcount255',"integer n;always @* begin out=8'd0;for(n=0;n<255;n=n+1)out=out+in[n];end",lambda v:{'out':v['in'].bit_count()},procedural=['out'],case_list=[{'in':(1<<i)-1} for i in range(256)]+list(random_cases({'in':255}))))
    sub='module bit_adder(input a,b,cin,output s,cout);assign s=a^b^cin;assign cout=(a&b)|(a&cin)|(b&cin);endmodule'
    body='wire[100:0]c;assign c[0]=cin;assign cout=c[100:1];genvar n;generate for(n=0;n<100;n=n+1)begin bit_adder f(a[n],b[n],c[n],sum[n],c[n+1]);end endgenerate'
    def prefix_carries(v):
        carries=sum((((v['a']&((1<<(i+1))-1))+(v['b']&((1<<(i+1))-1))+v['cin'])>>(i+1))<<i for i in range(100));return {'sum':(v['a']+v['b']+v['cin'])&((1<<100)-1),'cout':carries}
    ps.append(make('adder100i',body,prefix_carries,submodules=sub,explanation='100个全加器真实层次；每一级carry与独立前缀整数加法核对。'))
    support="module bcd_fadd(input[3:0]a,b,input cin,output cout,output[3:0]sum);wire[4:0]t;assign t={1'b0,a}+{1'b0,b}+cin;assign cout=t>5'd9;assign sum=cout?t-5'd10:t;endmodule"
    body='wire[100:0]c;assign c[0]=cin;assign cout=c[100];genvar n;generate for(n=0;n<100;n=n+1)begin bcd_fadd f(a[4*n+:4],b[4*n+:4],c[n],c[n+1],sum[4*n+:4]);end endgenerate'
    def packed(n):return int(str(n).zfill(100),16)
    def decimal(v):return int(format(v,'0100x'),10)
    def bcd_ref(v):
        total=decimal(v['a'])+decimal(v['b'])+v['cin'];return {'cout':int(total>=10**100),'sum':packed(total%(10**100))}
    cases=[{'a':packed(10**100-1),'b':0,'cin':1},{'a':0,'b':0,'cin':0}];rng=random.Random(260704)
    for n in range(1,101):cases.append({'a':packed(10**n-1),'b':packed(1),'cin':0})
    for _ in range(400):cases.append({'a':packed(rng.randrange(10**100)),'b':packed(rng.randrange(10**100)),'cin':rng.randrange(2)})
    ps.append(make('bcdadd100',body,bcd_ref,case_list=cases,support=support,explanation='100个题面BCD单元串接；参考在Python中解码为大十进制整数后整体验算。只给合法BCD数字。'))
    ps.append(make('gates','assign out_and=a&b;assign out_or=a|b;assign out_xor=a^b;assign out_nand=~(a&b);assign out_nor=~(a|b);assign out_xnor=~(a^b);assign out_anotb=a&~b;',lambda v:dict(zip(['out_and','out_or','out_xor','out_nand','out_nor','out_xnor','out_anotb'],[int(v['a'] and v['b']),int(v['a'] or v['b']),int(v['a']!=v['b']),int(not(v['a'] and v['b'])),int(not(v['a'] or v['b'])),int(v['a']==v['b']),int(v['a'] and not v['b'])]))))
    ps.append(make('truthtable1','assign f=(~x3 & x2) | (x3 & x1);',lambda v:{'f':[0,0,1,1,0,1,0,1][v['x3']*4+v['x2']*2+v['x1']]},explanation='按原真值表逐行核对，RTL采用化简式。'))
    ps.append(make('mt2015_q4a','assign z=(x^y)&x;',lambda v:{'z':int(v['x']==1 and v['y']==0)}))
    ps.append(make('mt2015_q4b','assign z=~(x^y);',lambda v:{'z':{(0,0):1,(1,0):0,(0,1):0,(1,1):1}[(v['x'],v['y'])]},explanation='原波形四个稳定区间依次对应00→1、10→0、01→0、11→1。'))
    ps.append(make('thermostat','assign heater=mode&too_cold;assign aircon=~mode&too_hot;assign fan=heater|aircon|fan_on;',lambda v:{'heater':int(v['mode']==1 and v['too_cold']==1),'aircon':int(v['mode']==0 and v['too_hot']==1),'fan':int(v['fan_on'] or (v['too_cold'] if v['mode'] else v['too_hot']))}))
    ps.append(make('popcount3',"assign out={1'b0,in[0]}+{1'b0,in[1]}+{1'b0,in[2]};",lambda v:{'out':v['in'].bit_count()}))
    def neighbors(v):
        a=v['in'];both=anys=diff=0
        for i in range(100):
            me=(a>>i)&1;left=(a>>((i+1)%100))&1
            if i<99:both|=(me&left)<<i
            if i>0:anys|=(me|((a>>(i-1))&1))<<(i-1)
            diff|=(me!=left)<<i
        return {'out_both':both,'out_any':anys,'out_different':diff}
    ps.append(make('gatesv100','assign out_both=in[98:0]&in[99:1];assign out_any=in[99:1]|in[98:0];assign out_different=in^{in[0],in[99:1]};',neighbors))
    ps.append(make('mux2to1','assign out=sel?b:a;',lambda v:{'out':v['b'] if v['sel'] else v['a']}))
    body="always @* begin case(sel)"+''.join(f"4'd{i}:out={n};" for i,n in enumerate('abcdefghi'))+"default:out=16'hffff;endcase end"
    rng=random.Random(260705);cases=[]
    for _ in range(100):
        v={n:rng.randrange(65536) for n in 'abcdefghi'}
        for sel in range(16):cases.append({**v,'sel':sel})
    ps.append(make('mux9to1v',body,lambda v:{'out':v['abcdefghi'[v['sel']]] if v['sel']<9 else 65535},case_list=cases,procedural=['out'],explanation='未使用sel9…15按原题返回全1，不能沿用另一题mux的默认0。'))
    rng=random.Random(260706);cases=[]
    for pat in range(6):
        digits=[(i+pat)%16 if pat<2 else rng.randrange(16) for i in range(256)];data=sum(v<<(4*i) for i,v in enumerate(digits))
        cases.extend({'in':data,'sel':i} for i in range(256))
    ps.append(make('mux256to1v','assign out=in[4*sel+:4];',lambda v:{'out':(v['in']//(16**v['sel']))%16},case_list=cases))
    def overflow(v):
        a=v['a'] if v['a']<128 else v['a']-256;b=v['b'] if v['b']<128 else v['b']-256;return {'s':(a+b)%256,'overflow':int(not(-128<=a+b<=127))}
    ps.append(make('ece241_2014_q1c','assign s=a+b;assign overflow=(~(a[7]^b[7]))&(a[7]^s[7]);',overflow))
    ps.append(make('adder100',"assign {cout,sum}={1'b0,a}+{1'b0,b}+cin;",lambda v:{'sum':(v['a']+v['b']+v['cin'])%2**100,'cout':(v['a']+v['b']+v['cin'])//2**100}))
    write_jobs(ps)
if __name__=='__main__':main()
