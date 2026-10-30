from pathlib import Path
import sys,struct,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def branch(offset):
    off=offset&8191
    return ((off>>12)&1)<<31|((off>>5)&63)<<25|(6<<20)|(5<<15)|((off>>1)&15)<<8|((off>>11)&1)<<7|0x63

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--variant',default='b3-cache128-profile');parser.add_argument('--padding',type=int,default=0);args=parser.parse_args()
    out=WORK/'b4/tools';out.mkdir(parents=True,exist_ok=True);exe=out/'branchsim';source=ROOT/'B/B4/branchsim.cpp'
    run('B4/branchsim/build',['g++','-std=c++17','-O3','-Wall','-Wextra',source,'-o',exe],inputs=[source],outputs=[exe],timeout=90,resume=True)
    control=out/'control.bin';control.write_bytes(b''.join(struct.pack('<5I',pc,branch(off),next_pc,0,0) for pc,off,next_pc in [(0x100,8,0x108),(0x108,-8,0x100),(0x110,-8,0x114),(0x118,8,0x11c)]))
    text,_,_=run('B4/branchsim/control',[exe,control],inputs=[exe,control]);c=json.loads(text);assert c['conditional_branches']==4 and set(c['correct_next_pc'].values())=={2}
    short=out/'short.bin';short.write_bytes(control.read_bytes()[:-1]);_,err,_=run('B4/branchsim/negative',[exe,short],inputs=[exe,short],expected=(2,));assert 'TRUNCATED_TRACE' in err
    base=next(r for r in json.loads((ROOT/'reports/B3_performance.json').read_text())['runs'] if r['variant']==args.variant and r.get('padding',0)==args.padding and r['size']=='test')
    trace=Path(base['trace']);text,_,_=run('B4/branchsim/'+args.variant+'-test',[exe,trace],inputs=[exe,trace]);data=json.loads(text)
    assert data['instructions']==base['simulation']['instructions'];assert data['conditional_branches']==base['simulation']['performance']['class_counts'][3]
    name='B4_branchsim.json' if args.variant=='b3-cache128-profile' and args.padding==0 else 'B4_branchsim_'+args.variant+'.json'
    dump(ROOT/'reports'/name,{'status':'PASS','results':data,'trace_sha256':sha(trace),'source_variant':base['variant'],'controls':c,'scope':'Full retired trace. Accuracies are predicted next-PC accuracy; branch-to-fallthrough degeneracies are counted explicitly. Hypothetical5-stage/15-stage/four-issue formulas are1/(1+2x(1-a)),1/(1+12x(1-a)),1/(1/4+12x(1-a)); no memory/RAW/structural stalls and perfect jumps, as specified by the exercise. They are not predictions of the implemented CPU IPC.'});print('B4_BRANCHSIM_PASS',data['branch_fraction'],data['correct_next_pc'])

if __name__=='__main__':main()
