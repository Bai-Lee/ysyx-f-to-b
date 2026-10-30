from common import *
import tarfile
def main():
    a=json.loads((ROOT/'reports/E_older_oss_asset.json').read_text());src=Path(a['path'].replace('D:\\','/mnt/d/').replace('\\','/'));assert sha(src)==a['sha256']
    dest=Path('/home/USER/tools/e-stage/oss-20260821');dest.mkdir(exist_ok=True)
    if not (dest/'oss-cad-suite/bin/yosys').exists():
        with tarfile.open(src) as t:
            for m in t.getmembers():assert (dest/m.name).resolve().is_relative_to(dest.resolve())
            t.extractall(dest)
    suite=dest/'oss-cad-suite';ecc=Path('/home/USER/tools/e-stage/ecos-alpha9/squashfs-root/resources/binaries/ecc');project=WORK/'backend/light'
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    o,e,r=run('E/backend/older_yosys_version',[suite/'bin/yosys','-V'],inputs=[suite/'bin/yosys'],env=env)
    run('E/backend/light_older_yosys',[ecc,'run','--project',project,'--run-id','yosys_august','--plain'],inputs=[ecc,project/'ecc.toml',project/'rtl/light.v'],cwd=project.parent,env=env,timeout=1200)
    dump(ROOT/'reports/E_backend_compatible_tools.json',{'status':'RUN_FINISHED_AWAITING_REPORT_AUDIT','ecc':str(ecc),'yosys_root':str(suite),'version':o,'project':str(project/'runs/yosys_august')})
if __name__=='__main__':main()
