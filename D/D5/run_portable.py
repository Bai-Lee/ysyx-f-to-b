from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=ROOT/'D/D5';am=BENCH/'abstract-machine';tests=BENCH/'am-kernels/tests/klib-tests';shutil.copyfile(p/'portable_tests.c',tests/'main.c')
    setup=json.loads((ROOT/'reports/D5_report_support.json').read_text());env=setup['environment'];rows=[]
    for arch in ['native','native-klib','riscv32-nemu']:
        image=tests/'build'/('klib-tests-'+arch+'.elf');report=tests/'build'/('klib-tests-'+arch+'.nemu.json')
        inputs=[tests/'Makefile',tests/'main.c',am/'Makefile',am/'scripts/platform/nemu.mk',*sorted((am/'klib/src').glob('*.c'))]
        if arch=='riscv32-nemu':inputs.extend([BENCH/'nemu/build/riscv32-nemu-interpreter',BENCH/'nemu/tools/spike-diff/build/riscv32-spike-so'])
        o,e,row=run('D5/portable/'+arch,['make','-j1','ARCH='+arch,'run','YSYX_HOME='+str(BENCH),'STUID=LOCAL_D_STAGE','STUNAME=Independent_Local_Implementation'],cwd=tests,env=env,inputs=inputs,outputs=[image]+([report] if arch=='riscv32-nemu' else []),timeout=180,resume=True)
        assert 'KLIB_PORTABLE_PASS' in o+e
        entry={'arch':arch,'status':'PASS','binary_sha256':sha(image),'evidence':'artifacts/D5/portable/'+arch,'elapsed_seconds':row['elapsed_seconds']}
        if arch=='riscv32-nemu':
            d=json.loads(report.read_text());assert d['result']=='GOOD_TRAP' and d['diff_enabled'] and d['diff_checked']+d['diff_skipped']==d['instructions'];entry['simulation']=d
        rows.append(entry);dump(ROOT/'reports/D5_portable.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/D5_portable.json',{'status':'PASS','runs':rows,'three_levels':'Native glibc, native owned klib, then the same source on RV32IM NEMU with Spike comparison.','native_allocator':'Uses glibc bridge; separate bare-metal allocator unit has independent evidence.'});print('D5_PORTABLE_PASS',flush=True)

if __name__=='__main__':main()
