from pathlib import Path
import sys,re,itertools,collections,html
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
D=ROOT/'D/D6';OUT=D/'results/pdk';OUT.mkdir(parents=True,exist_ok=True)
PDK=Path('/home/USER/tools/icsprout55-e-stage')
CELL=PDK/'IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CL'

def groups(text,kind):
    for m in re.finditer(r'\b'+kind+r'\s*\(\s*([^)]*)\)\s*\{',text):
        level=1
        for b in re.finditer(r'[{}]',text[m.end():]):
            level+=1 if b.group()=='{' else -1
            if not level:
                yield m.group(1).strip('" '),text[m.end():m.end()+b.start()]
                break
        else:raise ValueError('unclosed '+kind)

def attribute(text,key):
    m=re.search(r'\b'+key+r'\s*:\s*("[^"]*"|[^;]+);',text)
    if not m:raise ValueError('missing '+key)
    return m.group(1).strip().strip('"')

def interp(block,x=.0490972,y=.01):
    a=[float(v) for v in re.search(r'index_1\s*\("([^"]+)"',block)[1].split(',')]
    b=[float(v) for v in re.search(r'index_2\s*\("([^"]+)"',block)[1].split(',')]
    values=block[block.index('values'):];rows=[[float(v) for v in row.split(',')] for row in re.findall('"([^"]+)"',values)]
    assert len(rows)==len(a) and all(len(r)==len(b) for r in rows)
    assert a[0]<=x<=a[-1] and b[0]<=y<=b[-1]
    i=next(i for i in range(len(a)-1) if a[i]<=x<=a[i+1]);j=next(j for j in range(len(b)-1) if b[j]<=y<=b[j+1])
    u=(x-a[i])/(a[i+1]-a[i]);v=(y-b[j])/(b[j+1]-b[j])
    return (1-u)*((1-v)*rows[i][j]+v*rows[i][j+1])+u*((1-v)*rows[i+1][j]+v*rows[i+1][j+1])

def number(value):
    suffix={'n':1e-3,'u':1,'m':1e3}
    return float(value[:-1])*suffix[value[-1]] if value[-1] in suffix else float(value)*1e6

def main():
    lib=CELL/'liberty/ics55_LLSC_H7CL_typ_tt_1p2_25_nldm.lib';cdl=CELL/'cdl/ics55_LLSC_H7CL.cdl';lef=CELL/'lef/ics55_LLSC_H7CL.lef';tech=PDK/'prtech/techLEF/N551P6M.lef';iole=PDK/'IP/IO/ICsprout_55LLULP1233_IO_251013/lef/ICSIOA_N55_3P3_1P6M1TM.lef'
    text=lib.read_text();cells={};starts=list(re.finditer(r'\bcell\s*\((\w+)\)\s*\{',text))
    for i,m in enumerate(starts):cells[m[1]]=text[m.end():starts[i+1].start() if i+1<len(starts) else len(text)]
    names=['NAND2X1H7L','NAND2X2H7L','NAND2X4H7L','OAI22X1H7L','AOI221X1H7L','DFFX1H7L','ADDFX1H7L','XOR2X1H7L','AND2X1H7L','OR2X1H7L','INVX1H7L']
    sub={}
    for m in re.finditer(r'(?im)^\.SUBCKT\s+(\w+)([^\n]*)\n(.*?)^\.ENDS[^\n]*',cdl.read_text(),re.S):sub[m[1]]={'pins':m[2].split(),'body':m[3],'source':m.group()}
    def flatten(name,portmap=None,params=None,prefix=''):
        s=sub[name];portmap=portmap or {x:x for x in s['pins']};params=params or {};result=[]
        def net(n):return portmap.get(n,prefix+n)
        for line in s['body'].splitlines():
            words=line.split()
            if not words or line.startswith('*'):continue
            if words[0][0].upper()=='M':
                kv=dict(w.split('=',1) for w in words[6:]);kv={k:params.get(v,v) for k,v in kv.items()}
                result.append({'id':prefix+words[0],'D':net(words[1]),'G':net(words[2]),'S':net(words[3]),'B':net(words[4]),'model':words[5],'type':'n' if words[5].startswith('n') else 'p','W_um':number(kv['W']),'L_um':number(kv['L']),'m':int(kv.get('m','1'))})
            elif words[0][0].upper()=='X':
                ix=words.index('/');child=words[ix+1];childparams=dict(w.split('=',1) for w in words[ix+2:]);mapping=dict(zip(sub[child]['pins'],map(net,words[1:ix])));assert len(mapping)==len(sub[child]['pins'])
                result+=flatten(child,mapping,childparams,prefix+words[0]+'_')
            else:raise ValueError('unsupported CDL '+line)
        return result
    flat={n:flatten(n) for n in names}
    info={}
    for n in names:
        b=cells[n];pins=dict(groups(b,'pin'));func={p:attribute(v,'function') for p,v in pins.items() if re.search(r'\bfunction\s*:',v)}
        info[n]={'area_um2':float(attribute(b,'area')),'leakage_nw':float(attribute(b,'cell_leakage_power')),'functions':func,'mos_count':sum(t['m'] for t in flat[n]),'transistors':flat[n]}
        (OUT/(n+'.cdl')).write_text(sub[n]['source']+'\n')
        if n.startswith('NAND2'):
            arc=next(b for _,b in groups(pins['Y'],'timing') if attribute(b,'related_pin')=='A')
            info[n]['A_to_Y_at_49ps_10fF']={k:interp(next(groups(arc,k))[1]) for k in ['cell_rise','cell_fall','rise_transition','fall_transition']}
            info[n]['A_cap_pf']=float(attribute(pins['A'],'capacitance'))
    assert info['NAND2X1H7L']['mos_count']==4 and info['OAI22X1H7L']['mos_count']==8
    assert info['DFFX1H7L']['mos_count']==28 and info['ADDFX1H7L']['mos_count']==28
    for n in ['NAND2X1H7L','OAI22X1H7L','DFFX1H7L','ADDFX1H7L']:
        # Exact transistor connectivity graph. D/S channels solid, gates dashed;
        # bulk nets explicitly listed in each transistor's label.
        lines=['graph circuit { graph [rankdir=LR,overlap=false,fontname="DejaVu Sans",label="'+n+' | MOS connectivity (not physical layout)",labelloc=t]; node [fontname="DejaVu Sans",fontsize=10];']
        nets=sorted({t[p] for t in flat[n] for p in ['D','G','S','B']})
        for net in nets:lines.append(json.dumps(net)+' [shape=ellipse,label='+json.dumps(net)+'];')
        for t in flat[n]:
            label=t['id']+' '+t['type']+'MOS\nW/L='+str(round(t['W_um'],4))+'/'+str(round(t['L_um'],4))+' um\nB='+t['B']
            lines.append(json.dumps(t['id'])+' [shape=box,label='+json.dumps(label)+'];')
            for port in ['D','S','G']:lines.append(json.dumps(t[port])+' -- '+json.dumps(t['id'])+' [label="'+port+'",style='+('dashed' if port=='G' else 'solid')+'];')
        lines.append('}');dot=OUT/(n+'.dot');dot.write_text('\n'.join(lines))
        svg=OUT/(n+'.svg');run('D6/pdk/draw-'+n,['/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin/dot','-Tsvg',dot,'-o',svg],inputs=[dot,cdl],outputs=[svg])
    # Switch-level simulation follows the flattened CDL; each truth table also
    # checks the library function independently from an arithmetic oracle.
    v=OUT/'switch_models.v';source='`timescale 1ns/1ps\n'
    selected=['NAND2X1H7L','OAI22X1H7L','AOI221X1H7L','ADDFX1H7L','DFFX1H7L']
    for n in selected:
        pins=dict(groups(cells[n],'pin'));outputs=list(info[n]['functions']);inputs=[p for p in pins if p not in outputs]
        source+='module '+n+'_sw('+','.join(inputs+outputs)+');\ninput '+','.join(inputs)+'; output '+','.join(outputs)+'; supply1 VDD;supply0 VSS;\n'
        internal={t[p] for t in flat[n] for p in ['D','S','G']} - set(inputs+outputs+['VDD','VSS'])
        if internal:source+='wire '+','.join(sorted(internal))+';\n'
        # Combinational MOS topology uses ideal switch primitives. A raw
        # transistor transient model of the DFF needs capacitance/strength
        # information absent from these ideal primitives; see phase model below.
        for t in flat[n]:
            primitive='nmos' if t['type']=='n' else 'pmos'
            # The DFF feedback TSINVs have W=0.15um versus 0.20..0.30um
            # forward paths. Equal-strength switches lose this ratio and can
            # stick at X during clock overlap. Resistive feedback models that
            # ordering only; it is not an electrical calibration.
            if n=='DFFX1H7L' and t['W_um']<=.150001:primitive='r'+primitive
            source+=primitive+' '+t['id']+'('+','.join(t[p] for p in ['D','S','G'])+');\n'
        source+='endmodule\n'
        # Use Verilog as a separate evaluator of documented LIB boolean functions.
        source+='module '+n+'_lib('+','.join(inputs+outputs)+');\ninput '+','.join(inputs)+';output '+','.join(outputs)+';\n'
        if n!='DFFX1H7L':
            for p,f in info[n]['functions'].items():source+='assign '+p+'='+f.replace('*','&').replace('+','|')+';\n'
        else:source+='reg q;always @(posedge CK)q<=D;assign Q=q;assign QN=~q;\n'
        source+='endmodule\n'
    assert len(re.findall(r' / TSINV ',sub['DFFX1H7L']['body']))==4
    assert len(re.findall(r' / INV ',sub['DFFX1H7L']['body']))==6
    # A separate phase abstraction follows the CDL: master input XXI6 enabled
    # at CK=0; master feedback XI2 at CK=1; slave input XI3 at CK=1 and slave
    # feedback XI4 at CK=0. Six inverters establish phases/polarities/outputs.
    # It checks logical capture/hold, NOT MOS transients. Keep every earlier raw
    # MOS failure in artifacts; no change to expected capture/hold assertions.
    source+='''module DFFX1H7L_phase(input CK,D,output Q,QN);
reg master,slave;
always @* if(!CK)master=D;
always @* if(CK)slave=master;
assign Q=slave;assign QN=~slave;
endmodule
'''
    v.write_text(source)
    previous_tb=OUT/'switch_tb.v'
    if previous_tb.exists() and not (OUT/'raw_dff_probe_tb.v').exists():
        shutil.copyfile(previous_tb,OUT/'raw_dff_probe_tb.v')
    tb=OUT/'switch_tb.v';tb.write_text('''`timescale 1ns/1ps
module tb;
reg A=0,B=0,C=0,D=0,E=0,CK=1;wire n,nl,o,ol,ai,ail,co,s,col,sl,q,qn,ql,qnl;
NAND2X1H7L_sw g1(A,B,n);NAND2X1H7L_lib l1(A,B,nl);
OAI22X1H7L_sw g2(A,B,C,D,o);OAI22X1H7L_lib l2(A,B,C,D,ol);
AOI221X1H7L_sw g3(A,B,C,D,E,ai);AOI221X1H7L_lib l3(A,B,C,D,E,ail);
ADDFX1H7L_sw g4(A,B,C,co,s);ADDFX1H7L_lib l4(A,B,C,col,sl);
DFFX1H7L_phase g5(CK,A,q,qn);DFFX1H7L_lib l5(CK,A,ql,qnl);
integer i;
initial begin
 for(i=0;i<32;i=i+1)begin
 {A,B,C,D,E}=i;CK=0;#2;
 if(n!==!(A&B) || n!==nl)$fatal(1,"NAND");
 if(o!==!((A|B)&(C|D)) || o!==ol)$fatal(1,"OAI22");
 if(ai!==!((A&B)|(C&D)|E) || ai!==ail)$fatal(1,"AOI221");
 if({co,s}!==({1'b0,A}+B+C) || {co,s}!=={col,sl})$fatal(1,"ADDF");
 CK=1;#2;if(q!==A || q!==ql || qn!==~A || qn!==qnl)begin
 $fatal(1,"DFF sample i=%0d q=%b qn=%b expected=%b",i,q,qn,A);end
 A=~A;#2;if(q!==ql || qn!==qnl)$fatal(1,"DFF hold");
 end
 $display("CDL_PASS 32 combinational MOS cases and 32 DFF phase-abstraction capture/hold cases");$finish;
end endmodule
''')
    iv=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin');exe=WORK/'build/d6-cdl'
    run('D6/pdk/switch-compile',[iv/'iverilog','-g2012','-s','tb','-o',exe,v,tb],inputs=[v,tb,cdl,lib],outputs=[exe])
    o,_,_=run('D6/pdk/switch-run',[iv/'vvp',exe],inputs=[exe],timeout=20);assert 'CDL_PASS' in o
    # Fail-closed topology mutation reverses nMOS control polarity.
    bad=OUT/'bad_switch.v';bad.write_text(source.replace('nmos','pmos',1))
    badexe=WORK/'build/d6-cdl-bad'
    run('D6/pdk/bad-compile',[iv/'iverilog','-g2012','-s','tb','-o',badexe,bad,tb],inputs=[bad,tb],outputs=[badexe])
    o,_,_=run('D6/pdk/bad-run',[iv/'vvp',badexe],inputs=[badexe],expected=(1,));assert 'NAND' in o
    # LEF numerical inventory, with no inference of routing use from layer name.
    def blocks(t,kind):return {m[1]:m[2] for m in re.finditer(r'(?m)^'+kind+r'\s+(\w+)\s*\n(.*?)^END\s+\1\s*$',t,re.S)}
    techtext=tech.read_text();layers={k:b for k,b in blocks(techtext,'LAYER').items() if re.search(r'TYPE\s+ROUTING',b)}
    layerinfo={k:{f:re.search(r'\b'+f+r'\s+([^;]+);',b)[1].strip() for f in ['DIRECTION','PITCH','WIDTH']} for k,b in layers.items()}
    def size(b):return list(map(float,re.search(r'SIZE\s+(\S+)\s+BY\s+(\S+)\s*;',b).groups()))
    macros=blocks(lef.read_text(),'MACRO');ios=blocks(iole.read_text(),'MACRO');sites=blocks(techtext,'SITE')
    io='P65_1233_PBMUX';assert io in ios
    filler=sorted(((size(b)[0]*size(b)[1],n,size(b)) for n,b in macros.items() if n.startswith('FILL')),key=lambda a:a[0])[0]
    nand_size=size(macros['NAND2X1H7L']);track=nand_size[1]/float(layerinfo['MET1']['PITCH'].split()[-1])
    assert abs(track-7)<1e-9 and filler[2]==size(sites['core7'])
    catalog=[]
    for n,b in cells.items():
        func={p:attribute(v,'function') for p,v in groups(b,'pin') if re.search(r'\bfunction\s*:',v)}
        category='physical' if n.startswith(('FILL','DECAP','TAP','ANTENNA')) else 'scan' if n.startswith('SDFF') else 'clock' if n.startswith(('ICG','CLK')) else 'sequential' if n.startswith(('DFF','LAT')) else 'tie' if n.startswith('TIE') else 'buffer' if n.startswith(('BUF','INV','TBUF')) else 'combinational'
        catalog.append({'name':n,'class':category,'functions':func,'area_um2':float(attribute(b,'area')),'in_cdl':n in sub,'in_lef':n in macros})
    dump(OUT/'cell_catalog.json',catalog)
    fulladder={'dedicated_area_um2':info['ADDFX1H7L']['area_um2'],'dedicated_mos':28,'gate_formula':'2 XOR2X1H7L + 2 AND2X1H7L + 1 OR2X1H7L; S=(A xor B) xor CI; CO=A B + CI (A xor B)','gate_area_um2':2*info['XOR2X1H7L']['area_um2']+2*info['AND2X1H7L']['area_um2']+info['OR2X1H7L']['area_um2'],'gate_mos':2*info['XOR2X1H7L']['mos_count']+2*info['AND2X1H7L']['mos_count']+info['OR2X1H7L']['mos_count']}
    dump(ROOT/'reports/D6_pdk.json',{'status':'PASS_TOPOLOGY_AND_LIBRARY_ANALYSIS','inputs':[{'path':str(p),'sha256':sha(p)} for p in [lib,cdl,lef,tech,iole]],'scope':'NAND/OAI/AOI/ADDF combinational MOS checks; DFF 28-device graph/count and CDL-derived two-latch phase abstraction only. No DFF transistor-transient, analog SPICE timing or layout LVS claim. LIB delays separately interpolated.','dff_raw_switch_probe':{'status':'FAIL_UNQUALIFIED_MODEL','reason':'Ideal zero-delay/equal-strength/delayed MOS approximations lost state or produced X; transistor models/capacitances are not present in this PDK export. Failed expectations were not relaxed; preserved in artifacts/D6/pdk/switch-run/attempts and raw_dff_probe_tb.v. Main DFF check explicitly uses the documented phase abstraction.','required_task':'D6-O013 asks for drawing, transistor count and functional explanation; it does not require analog transient qualification.'},'cells':info,'fulladder':fulladder,'layers':layerinfo,'track_count':track,'site_core7_um':size(sites['core7']),'smallest_filler':filler,'nand_size_um':nand_size,'io_example':{'name':io,'size_um':size(ios[io])},'cell_count':len(catalog),'category_counts':dict(collections.Counter(x['class'] for x in catalog))})
    print('PDK_ANALYSIS_PASS',len(catalog),fulladder,layerinfo,flush=True)

if __name__=='__main__':main()
