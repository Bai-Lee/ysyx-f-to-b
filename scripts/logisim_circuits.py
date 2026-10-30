"""Author structural .circ files. Logic is always executed by Logisim, not this writer."""
from pathlib import Path
import xml.etree.ElementTree as ET
LIBS={'Wiring':'0','Gates':'1','Plexers':'2','Arithmetic':'3','Memory':'4','I/O':'5','Base':'8'}
def attr(el,name,value):ET.SubElement(el,'a',{'name':name,'val':str(value).lower() if isinstance(value,bool) else str(value)})
def point(x,y):return f'({int(x)},{int(y)})'
def comp(parent,lib,name,x,y,**attrs):
    d={'loc':point(x,y),'name':name}
    if lib is not None:d['lib']=LIBS.get(lib,lib)
    e=ET.SubElement(parent,'comp',d)
    for n,v in attrs.items():attr(e,n,v)
    return e
class Project:
    def __init__(self,main):
        self.root=ET.Element('project',{'source':'4.0.0','version':'1.0'})
        for name,i in LIBS.items():ET.SubElement(self.root,'lib',{'name':i,'desc':'#'+name})
        ET.SubElement(self.root,'main',{'name':main})
        options=ET.SubElement(self.root,'options');attr(options,'simlimit',2000)
        self.circuits={}
        toolbar=ET.SubElement(self.root,'toolbar')
        for lib,name in [('Base','Poke Tool'),('Base','Edit Tool'),('Base','Wiring Tool'),('Base','Text Tool'),('Wiring','Pin'),('Gates','NOT Gate'),('Gates','AND Gate'),('Gates','OR Gate')]:ET.SubElement(toolbar,'tool',{'lib':LIBS[lib],'name':name})
    def circuit(self,name,description=''):
        c=Circuit(self,name,description);self.circuits[name]=c;return c
    def write(self,path):
        for c in self.circuits.values():c.appear.find('rect').set('height',str(max(60,50+20*max(len(c.inputs),len(c.outputs)))))
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);ET.indent(self.root,space='  ');ET.ElementTree(self.root).write(path,encoding='UTF-8',xml_declaration=True)

class Circuit:
    def __init__(self,project,name,description):
        self.project=project;self.name=name;self.el=ET.SubElement(project.root,'circuit',{'name':name});attr(self.el,'appearance','custom');self.idx=0;self.serial=0;self.pin_count=0;self.widths={};self.inputs={};self.outputs={};self.pin_locations={};self.description=description
        self.appear=ET.SubElement(self.el,'appear');ET.SubElement(self.appear,'rect',{'x':'50','y':'50','width':'140','height':'60','fill':'none','stroke':'#000000','stroke-width':'2'})
        ET.SubElement(self.appear,'text',{'x':'60','y':'70','font-family':'SansSerif','font-size':'11'}).text=name
        ET.SubElement(self.appear,'circ-anchor',{'facing':'east','height':'6','width':'6','x':'187','y':'77'})
    def fresh(self,prefix='n',width=1):
        self.serial+=1;n=f'{prefix}_{self.serial}';self.widths[n]=width;return n
    def width(self,n):return self.widths[n]
    def wire(self,x1,y1,x2,y2):
        if x1==x2 and y1==y2:return
        if x1!=x2 and y1!=y2:raise ValueError('Only orthogonal wires')
        ET.SubElement(self.el,'wire',{'from':point(x1,y1),'to':point(x2,y2)})
    def tap(self,x,y,net,side='left'):
        dx,dy,face={'left':(-30,0,'east'),'right':(30,0,'west'),'up':(0,-30,'south'),'down':(0,30,'north')}[side]
        comp(self.el,'Wiring','Tunnel',x+dx,y+dy,label=net,width=self.width(net),facing=face)
        self.wire(x,y,x+dx,y+dy)
    def io(self,name,width=1,output=False,net=None):
        net=net or name;self.widths.setdefault(net,width)
        dic=self.outputs if output else self.inputs;idx=len(dic);x=1800 if output else 100;y=120+idx*70
        comp(self.el,'Wiring','Pin',x,y,label=name,width=width,type='output' if output else 'input',facing='west' if output else 'east',radix='16' if width>1 else '2')
        self.tap(x,y,net,'left' if output else 'right');dic[name]=net;self.pin_locations[name]=(x,y)
        # Explicit custom-symbol ports, independent of auto-appearance ordering.
        px=190 if output else 50;py=80+idx*20
        radius=5 if output else 4
        ET.SubElement(self.appear,'circ-port',{'height':str(2*radius),'width':str(2*radius),'pin':f'{x},{y}','x':str(px-radius),'y':str(py-radius)})
        return net
    def pos(self):
        n=self.idx;self.idx+=1;return 450+(n%4)*310,300+(n//4)*240
    def gate(self,kind,args,out=None):
        if len(args)==1 and kind!='NOT':return args[0]
        if len(args)>3:
            if kind not in ('AND','OR'):raise ValueError('Reduction tree only valid for associative AND/OR')
            mids=[self.gate(kind,args[i:i+2]) if len(args[i:i+2])>1 else args[i] for i in range(0,len(args),2)]
            return self.gate(kind,mids,out)
        width=self.width(args[0]);out=out or self.fresh(kind.lower(),width)
        self.widths.setdefault(out,width);x,y=self.pos();comp(self.el,'Gates',kind+' Gate',x,y,width=width,inputs=len(args))
        axis=30 if kind=='NOT' else 50+(10 if kind in ('NAND','NOR','XOR') else 20 if kind=='XNOR' else 0)
        dy=[0] if kind=='NOT' else ([-20,20] if len(args)==2 else [-20,0,20])
        for net,delta in zip(args,dy):self.tap(x-axis,y+delta,net,'left')
        self.tap(x,y,out,'right');return out
    def inv(self,a,out=None):return self.gate('NOT',[a],out)
    def and_(self,*a,out=None):return self.gate('AND',list(a),out)
    def or_(self,*a,out=None):return self.gate('OR',list(a),out)
    def xor(self,a,b,out=None):return self.gate('XOR',[a,b],out)
    def const(self,value,width=1,out=None):
        out=out or self.fresh('k',width);self.widths.setdefault(out,width);x,y=self.pos();comp(self.el,'Wiring','Constant',x,y,width=width,value=hex(value));self.tap(x,y,out,'right');return out
    def split(self,bus):
        n=self.width(bus);x,y=self.pos();attrs={'fanout':n,'incoming':n,'facing':'east','appear':'left'}
        for i in range(n):attrs['bit'+str(i)]=i
        comp(self.el,'Wiring','Splitter',x,y,**attrs);self.tap(x,y,bus,'left');bits=[]
        for i in range(n):
            b=self.fresh('bit',1);self.tap(x+20,y-(n-i)*10,b,'right');bits.append(b)
        return bits
    def join(self,bits,out=None):
        out=out or self.fresh('bus',len(bits));self.widths.setdefault(out,len(bits));x,y=self.pos();attrs={'fanout':len(bits),'incoming':len(bits),'facing':'east','appear':'left'}
        for i in range(len(bits)):attrs['bit'+str(i)]=i
        comp(self.el,'Wiring','Splitter',x,y,**attrs);self.tap(x,y,out,'left')
        for i,b in enumerate(bits):self.tap(x+20,y-(len(bits)-i)*10,b,'right')
        return out
    def sub(self,name,inputs):
        child=self.project.circuits[name];x,y=self.pos();comp(self.el,None,name,x,y)
        if set(inputs)!=set(child.inputs):raise ValueError((name,inputs,child.inputs))
        for i,p in enumerate(child.inputs):self.tap(x-140,y+i*20,inputs[p],'left')
        result={}
        for i,(p,net) in enumerate(child.outputs.items()):
            out=self.fresh(name+'_'+p,child.width(net));self.tap(x,y+i*20,out,'right');result[p]=out
        return result
    def sevenseg(self,bits,x=1600,y=180):
        comp(self.el,'I/O','7-Segment Display',x,y)
        for net,(dx,dy) in zip(bits,[(20,0),(30,0),(20,60),(10,60),(0,60),(10,0),(0,0),(30,60)]):self.tap(x+dx,y+dy,net,'up' if dy==0 else 'down')
    def hexdisplay(self,bits,x=1600,y=180):
        bus=self.join(bits);comp(self.el,'I/O','Hex Digit Display',x,y,decimalPoint=False);self.tap(x,y,bus,'down')
    def mux(self,select,a,b,out=None):
        ns=self.inv(select);return self.or_(self.and_(ns,a),self.and_(select,b),out=out)
    def ff(self,d,clk,reset=None,out=None):
        # Master/slave NAND latches: master transparent low, slave high.
        out=out or self.fresh('q');self.widths.setdefault(out,1)
        nclk=self.inv(clk);m=self.latch(d,nclk,reset);self.latch(m,clk,reset,out=out);return out
    def latch(self,d,we,reset=None,out=None):
        out=out or self.fresh('lq');self.widths.setdefault(out,1);qb=self.fresh('lqb');nd=self.inv(d)
        if reset is not None:
            # Reset is incorporated in the active-high SR excitation. Gating
            # active-low excitations independently can pulse an illegal pair
            # when RESET, D and WE change together (retained regression case).
            s=self.and_(d,we,self.inv(reset));r=self.or_(self.and_(nd,we),reset)
            self.gate('NOR',[r,qb],out);self.gate('NOR',[s,out],qb);return out
        s=self.gate('NAND',[d,we]);r=self.gate('NAND',[nd,we])
        self.gate('NAND',[s,qb],out);self.gate('NAND',[r,out],qb);return out
    def reg(self,data,clk,reset,en=None,outprefix='q'):
        result=[]
        for i,d in enumerate(data):
            q=self.fresh(outprefix);din=self.mux(en,q,d) if en is not None else d;self.ff(din,clk,reset,q);result.append(q)
        return result

def catalog_file(path):
    p=Project('catalog');c=p.circuit('catalog')
    for i,(lib,name,attrs) in enumerate([
        ('Wiring','Splitter',{'fanout':4,'incoming':4,'appear':'left','facing':'east'}),
        ('Wiring','Tunnel',{'width':8,'label':'BUS'}),('Wiring','Constant',{'width':8,'value':'0x55'}),
        ('I/O','LED',{}),('I/O','7-Segment Display',{}),('I/O','Hex Digit Display',{'decimalPoint':False}),
        ('I/O','Dip Switch',{'number':8}),('I/O','Button',{}),('Wiring','Clock',{}),
        ('Plexers','Multiplexer',{'width':8,'select':2}),('Gates','XOR Gate',{}),('Gates','NAND Gate',{}),('Gates','NOT Gate',{})]):
        comp(c.el,lib,name,300+(i%4)*300,150+(i//4)*250,**attrs)
    p.write(path)
if __name__=='__main__':catalog_file(Path(__file__).resolve().parents[1]/'temp/catalog.circ')
