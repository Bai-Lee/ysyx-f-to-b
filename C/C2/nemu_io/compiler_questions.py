"""Actual isolated NEMU builds for PA2 static/inline/header-object questions."""
from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

def main():
    src=BENCH/'nemu';lab=WORK/'c2-compiler-questions';n=lab/'nemu';lab.mkdir(exist_ok=True)
    if not n.exists():
        shutil.copytree(src,n,symlinks=True,ignore=shutil.ignore_patterns('build','repo','.git','__pycache__'))
        for sub in ('capstone','spike-diff'):
            link=n/'tools'/sub/'repo';link.symlink_to(src/'tools'/sub/'repo',target_is_directory=True)
    d=ROOT/'C/C2/nemu_io/compiler';d.mkdir(exist_ok=True)
    paths={key:n/'include'/key for key in ['cpu/ifetch.h','common.h','debug.h']}
    originals={key:(src/'include'/key).read_bytes() for key in paths}
    env={'NEMU_HOME':str(n),'USE_PINNED_DIFF_SO':'1'};rows=[]
    template=(src/'configs/c2_perf_defconfig').read_text()
    variants=[('baseline','static inline',2,None,False),('no_static','inline',2,None,False),('no_inline','static',2,None,False),('neither','',2,None,False),('inline_O0','inline',0,None,False),('dummy_common','static inline',2,'common',False),('dummy_both','static inline',2,'both',False),('dummy_initialized','static inline',2,'both',True)]
    try:
        for name,prefix,opt,dummy,initialized in variants:
            for key,p in paths.items():p.write_bytes(originals[key])
            header=paths['cpu/ifetch.h'];text=header.read_text();assert 'static inline uint32_t inst_fetch' in text
            header.write_text(text.replace('static inline uint32_t inst_fetch',prefix+' uint32_t inst_fetch'))
            if dummy:
                declaration='\nvolatile static int dummy'+(' = 0' if initialized else '')+';\n'
                for key in (['common.h'] if dummy=='common' else ['common.h','debug.h']):
                    p=paths[key];text=p.read_text();pos=text.rfind('#endif');assert pos>=0;p.write_text(text[:pos]+declaration+text[pos:])
            config=template
            if opt==0:config=config.replace('# CONFIG_CC_O0 is not set','CONFIG_CC_O0=y').replace('CONFIG_CC_O2=y','# CONFIG_CC_O2 is not set').replace('CONFIG_CC_OPT="-O2"','CONFIG_CC_OPT="-O0"')
            definition=n/'configs/c2_question_defconfig';definition.write_text(config)
            run('C2/pa2/compiler/'+name+'/config',['make','-j1','c2_question_defconfig'],cwd=n,env=env,inputs=[definition],outputs=[n/'.config'],resume=True)
            output=n/'build'/name;exe=output/'riscv32-nemu-interpreter'
            expected=(2,) if name in ('neither','inline_O0','dummy_initialized') else (0,)
            o,e,r=run('C2/pa2/compiler/'+name+'/build',['make','-j1','BUILD_DIR='+str(output)],cwd=n,env=env,inputs=[n/'.config',*paths.values()],outputs=[] if expected==(2,) else [exe],expected=expected,timeout=300,resume=True)
            row={'name':name,'optimization':opt,'expected_exit':expected[0],'actual_exit':r['exit_code'],'status':'PASS_REJECTED' if expected==(2,) else 'PASS_COMPILED','header_hashes':{key:sha(p) for key,p in paths.items()}}
            if name=='neither':assert 'multiple definition' in e and 'inst_fetch' in e
            elif name=='inline_O0':assert 'undefined reference' in e and 'inst_fetch' in e
            elif name=='dummy_initialized':assert 'redefinition' in e and 'dummy' in e
            else:
                symbols,_,_=run('C2/pa2/compiler/'+name+'/symbols',['nm','-a','-S',exe],inputs=[exe])
                dummy_lines=[line for line in symbols.splitlines() if re.search(r'\b[bBdD]\s+dummy(?:\.\d+)?$',line)]
                fetch_lines=[line for line in symbols.splitlines() if re.search(r'\b[tT]\s+inst_fetch(?:\.\w+)?$',line)]
                row.update(dummy_entities=len(dummy_lines),dummy_symbols=dummy_lines,inst_fetch_symbols=fetch_lines,executable_sha256=sha(exe))
                if dummy:assert len(dummy_lines)>0
            rows.append(row)
            dump(ROOT/'reports/C2_pa2_compiler.json',{'status':'IN_PROGRESS','variants':rows})
        one=next(r for r in rows if r['name']=='dummy_common');both=next(r for r in rows if r['name']=='dummy_both')
        assert one['dummy_entities']==both['dummy_entities']
        # Observe the actual make expansion for the AM hello target.
        hello=WORK/'c2-nemu-apps/am-kernels/kernels/hello'
        plan,_,_=run('C2/pa2/compiler/hello_make_plan',['make','-n','-B','-j1','ARCH=riscv32-nemu'],cwd=hello,inputs=[hello/'Makefile',BENCH/'abstract-machine/Makefile'],timeout=60)
        (d/'hello.make-plan.txt').write_text(plan)
        dump(ROOT/'reports/C2_pa2_compiler.json',{'status':'PASS','variants':rows,'dummy_common_entities':one['dummy_entities'],'dummy_both_entities':both['dummy_entities'],'scope':'Actual isolated NEMU translation units and linker, using the recorded RV32IM performance configuration. Entity counts depend on configuration/compiler; not a universal fixed count. Original active C NEMU headers never changed. make -n -B displays the real AM build graph without claiming compilation.'})
        print('C2_PA2_COMPILER_PASS',one['dummy_entities'],flush=True)
    finally:
        for key,p in paths.items():p.write_bytes(originals[key])

if __name__=='__main__':main()
