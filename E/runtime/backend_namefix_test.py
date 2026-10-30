from common import *
def main():
    tools=Path('/home/USER/tools/e-stage');ecc=tools/'ecos-alpha9/squashfs-root/resources/binaries/ecc';suite=tools/'oss-20261022/oss-cad-suite';project=WORK/'backend/light';shims=WORK/'shims';shims.mkdir(exist_ok=True)
    script=ROOT/'E/runtime/normalize_net_names.py';wrapper=shims/'yosys'
    wrapper.write_text('''#!/bin/sh
"'''+str(suite/'bin/yosys')+'''" "$@"
result=$?
if [ "$result" -ne 0 ]; then exit "$result"; fi
if [ -n "$E_NAMEFIX_TARGET" ] && [ -f "$E_NAMEFIX_TARGET" ]; then
 /usr/bin/python3 "'''+str(script)+'''" "$E_NAMEFIX_TARGET" || exit $?
fi
''');wrapper.chmod(0o755)
    runid='identifier_compat';target=project/'runs'/runid/'Synthesis_yosys/output/light_Synthesis.v.gz'
    env={'PATH':str(shims)+':'+str(suite/'bin')+':'+os.environ['PATH'],'E_NAMEFIX_TARGET':str(target),'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    o,e,r=run('E/backend/light_namefix',[ecc,'run','--project',project,'--run-id',runid,'--plain'],inputs=[ecc,project/'ecc.toml',project/'rtl/light.v',script,wrapper],cwd=project.parent,env=env,timeout=1200)
    print('BACKEND_NAMEFIX_FLOW_DONE',flush=True)
if __name__=='__main__':main()
