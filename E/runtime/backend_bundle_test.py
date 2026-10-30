from common import *
def main():
    tools=Path('/home/USER/tools/e-stage');ecc=tools/'ecos-alpha9/squashfs-root/resources/binaries/ecc';suite=tools/'oss-20261022/oss-cad-suite';project=WORK/'backend/light'
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    o,e,r=run('E/backend/bundle_version',[ecc,'version','--json'],inputs=[ecc],env=env);dump(ROOT/'reports/E_backend_bundle_version.json',json.loads(o))
    run('E/backend/light_synthesis_bundle',[ecc,'run','--project',project,'--run-id','ecos_bundle','--plain'],inputs=[ecc,project/'ecc.toml',project/'rtl/light.v'],cwd=project.parent,env=env,timeout=1200)
    print('BUNDLED_ECC_SYNTHESIS_DONE',flush=True)
if __name__=='__main__':main()
