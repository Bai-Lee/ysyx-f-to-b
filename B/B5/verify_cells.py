"""Check the official cell models against independent Liberty truth tables."""
from pathlib import Path
import sys,re,itertools
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def blocks(text,keyword):
    result={}
    for match in re.finditer(r'\b'+keyword+r'\s*\(\s*([^()]+)\s*\)\s*\{',text):
        start=match.end();depth=1;quoted=False;escaped=False;end=start
        while depth:
            c=text[end]
            if quoted:
                if escaped:escaped=False
                elif c=='\\':escaped=True
                elif c=='"':quoted=False
            elif c=='"':quoted=True
            elif c=='{':depth+=1
            elif c=='}':depth-=1
            end+=1
        result[match[1].strip().strip('"')]=text[start:end-1]
    return result

def evaluate(expression,values):
    tokens=re.findall(r'[A-Za-z_][A-Za-z_0-9]*|[01()!&|^]',expression);assert ''.join(tokens)==re.sub(r'\s+','',expression)
    position=0
    def unary():
        nonlocal position
        token=tokens[position];position+=1
        if token=='!':return 1-unary()
        if token=='(':
            value=expr(0);assert tokens[position]==')';position+=1;return value
        if token in ('0','1'):return int(token)
        return values[token]
    def expr(level):
        nonlocal position
        if level==3:return unary()
        op=['|','^','&'][level];value=expr(level+1)
        while position<len(tokens) and tokens[position]==op:
            position+=1;right=expr(level+1);value=(value|right) if op=='|' else (value^right) if op=='^' else (value&right)
        return value
    result=expr(0);assert position==len(tokens);return result

def main():
    lib=ROOT/'B/models/nangate45/lib/Nangate45_typ.lib';models=ROOT/'B/models/nangate45/sim/cells.v'
    assert json.loads((ROOT/'reports/B_nangate_course_library.json').read_text())['status']=='PASS_ALL_USED_LIBRARY_CONTENT_IDENTICAL'
    structure=ROOT/'B/B5/netlist/mapped.json';module=json.loads(structure.read_text())['modules']['ysyx_00000000'];used=sorted({c['type'] for c in module['cells'].values() if c['type']!='$scopeinfo'})
    cells=blocks(re.sub(r'/\*.*?\*/','',lib.read_text(),flags=re.S),'cell')
    declarations=['module cells_tb;'];checks=['initial begin'];vectors=0;sequential=[]
    for name in used:
        cell=cells[name];pins=blocks(cell,'pin');inputs=[n for n,p in pins.items() if re.search(r'direction\s*:\s*input',p)];outputs=[n for n,p in pins.items() if re.search(r'direction\s*:\s*output',p)]
        assert inputs and outputs
        declarations += [f'reg [{len(inputs)-1}:0] v_{name};',f'wire [{len(outputs)-1}:0] o_{name};',name+' u_'+name+'('+','.join(f'.{p}(v_{name}[{i}])' for i,p in enumerate(inputs))+','+','.join(f'.{p}(o_{name}[{i}])' for i,p in enumerate(outputs))+');']
        checks.append(f'v_{name}=0; #1;')
        if re.search(r'\bff\s*\(',cell):
            assert name=='DFF_X1' and set(inputs)=={'D','CK'} and set(outputs)=={'Q','QN'}
            ck=inputs.index('CK');d=inputs.index('D');q=outputs.index('Q');qn=outputs.index('QN')
            checks += [f'v_{name}[{ck}]=1; #1; if(o_{name}[{q}]!==0 || o_{name}[{qn}]!==1) $fatal(1,"DFF_INITIAL_CAPTURE");',
                       f'v_{name}[{d}]=1; #1; if(o_{name}[{q}]!==0) $fatal(1,"DFF_NOT_EDGE_TRIGGERED");',
                       f'v_{name}[{ck}]=0; #1; if(o_{name}[{q}]!==0) $fatal(1,"DFF_NEGEDGE_WRITE");',
                       f'v_{name}[{ck}]=1; #1; if(o_{name}[{q}]!==1 || o_{name}[{qn}]!==0) $fatal(1,"DFF_SECOND_CAPTURE");',
                       f'v_{name}[{d}]=1\'bx;v_{name}[{ck}]=0; #1;v_{name}[{ck}]=1;#1;if(o_{name}[{q}]!==1\'bx||o_{name}[{qn}]!==1\'bx) $fatal(1,"DFF_NOT_FOUR_STATE");']
            sequential.append(name)
        else:
            functions={pin:re.search(r'function\s*:\s*"([^"]+)"',pins[pin])[1] for pin in outputs}
            for pattern in range(1<<len(inputs)):
                values={pin:(pattern>>i)&1 for i,pin in enumerate(inputs)};answer=sum(evaluate(functions[pin],values)<<i for i,pin in enumerate(outputs));vectors+=1
                checks.append(f'v_{name}={len(inputs)}\'d{pattern};#1;if(o_{name}!=={len(outputs)}\'d{answer}) $fatal(1,"CELL_FUNCTION_MISMATCH {name} vector{pattern}");')
    checks += [f'$display("CELL_FUNCTIONS_PASS cells={len(used)} vectors={vectors} sequential={len(sequential)}");','$finish;end','endmodule']
    scope=ROOT/'B/B5/cell-checks';scope.mkdir(parents=True,exist_ok=True);tb=scope/'cells_tb.sv';tb.write_text('\n'.join(declarations+checks)+'\n')
    bad=scope/'cells-mutant.v';text=models.read_text();assert 'AND2_X1' in used
    pattern=r'(module AND2_X1\b.*?assign ZN = )\(A1 & A2\)';text,count=re.subn(pattern,r'\1~(A1 & A2)',text,count=1,flags=re.S);assert count==1;bad.write_text(text)
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');iv=suite/'bin/iverilog';vvp=suite/'bin/vvp';rows=[]
    run('B5/iverilog/version',[iv,'-V'],inputs=[iv]);run('B5/vvp/version',[vvp,'-V'],inputs=[vvp])
    for name,source,expected in [('positive',models,0),('wrong-cell',bad,1)]:
        exe=WORK/'b5'/('cells-'+name+'.vvp');exe.parent.mkdir(exist_ok=True)
        run('B5/cells/'+name+'-build',[iv,'-g2012','-s','cells_tb','-o',exe,tb,source],inputs=[iv,tb,source],outputs=[exe],timeout=120)
        stdout,stderr,_=run('B5/cells/'+name+'-run',[vvp,exe],inputs=[vvp,exe],expected=(expected,),timeout=60)
        assert ('CELL_FUNCTIONS_PASS' in stdout) if not expected else ('CELL_FUNCTION_MISMATCH AND2_X1' in stdout+stderr)
        rows.append({'name':name,'status':'PASS' if not expected else 'PASS_WRONG_CELL_REJECTED','evidence':'artifacts/B5/cells/'+name+'-run'})
    dump(ROOT/'reports/B5_cell_models.json',{'status':'PASS','used_cells':used,'binary_truth_vectors':vectors,'sequential_cells':sequential,'liberty_sha256':sha(lib),'models_sha256':sha(models),'netlist_structure_sha256':sha(structure),'runs':rows,'scope':'Every combinational cell type used by the compact CPU is exhaustively checked over binary inputs against parsed Liberty functions. DFF edge behavior and X propagation are tested in Icarus. Wrong AND2 implementation is rejected. These models are zero-delay functional models, not SDF timing simulation.'});print('B5_CELL_MODELS_PASS',len(used),vectors)

if __name__=='__main__':main()
