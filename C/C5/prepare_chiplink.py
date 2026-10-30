from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import generation_environment,POLICY_PATH


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');args=parser.parse_args()
    original=WORK/'soc-generation/ysyxSoC';soc=WORK/'c5/chiplink/ysyxSoC'
    if not soc.exists():
        def ignore(path,names):return [name for name in names if name in ['out','__pycache__'] or (Path(path)==original and name=='build')]
        soc.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(original,soc,ignore=ignore)
    source=original/'src/Top.scala';target=soc/'src/Top.scala';text=source.read_text();assert text.count('def hasChipLink: Boolean = false')==1
    target.write_text(text.replace('def hasChipLink: Boolean = false','def hasChipLink: Boolean = true'))
    files=[p for p in sorted(soc.rglob('*')) if p.is_file() and p.suffix in ['.scala','.sc'] and not any(x in p.relative_to(soc).parts for x in ['out','build','.git'])]
    files += [soc/'Makefile',soc/'.mill-version',soc/'patch/rocket-chip.patch']
    before=[{'path':str(p.relative_to(soc)),'sha256':sha(p)} for p in files]
    folder=ROOT/'C/C5/generation/chiplink';folder.mkdir(exist_ok=True);manifest=folder/'source_manifest.json'
    dump(manifest,{'source_copy':str(soc),'original':str(original),'original_top_sha256':sha(source),'chiplink_top_sha256':sha(target),'change':'Only Config.hasChipLink false->true in the independent copied working tree. Accepted dev-init patch and submodule content reused; no second dev-init.','files':before})
    if not args.generate:
        dump(ROOT/'reports/C5_chiplink_generation.json',{'status':'PREPARED_NOT_GENERATED','manifest':str(manifest),'manifest_sha256':sha(manifest)});print('C5_CHIPLINK_SOURCES_PREPARED',flush=True);return
    tools=json.loads((ROOT/'reports/C5_toolchain.json').read_text());environment=generation_environment(tools['environment'])
    for binary in tools['binaries']:assert sha(binary['path'])==binary['sha256']
    output=soc/'build/ysyxSoCFull.v';budget=ROOT/'artifacts/C5/chiplink/generate/resources.json'
    run('C5/chiplink/generate',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--','taskset','-c','0,1','make','-j1','verilog'],cwd=soc,env=environment,inputs=[manifest,target,soc/'Makefile',soc/'build.sc',POLICY_PATH,ROOT/'C/runtime/budget_exec.py'],outputs=[output,budget],timeout=1800,resume=True)
    assert [{'path':str(p.relative_to(soc)),'sha256':sha(p)} for p in files]==before
    modules=re.findall(r'^module\s+(\w+)',output.read_text(),re.M);assert any('ChipLink' in name for name in modules) and len(modules)>39
    shutil.copyfile(output,folder/'ysyxSoCFull.v');resources=[]
    for item in sorted((soc/'build').glob('*')):
        if item.is_file() and item.suffix in ['.v','.sv'] and item!=output:
            resource=folder/'resources'/item.name;resource.parent.mkdir(exist_ok=True);shutil.copyfile(item,resource);resources.append({'path':str(resource),'sha256':sha(resource)})
    dump(ROOT/'reports/C5_chiplink_generation.json',{'status':'GENERATED_NOT_RUNTIME_ACCEPTED','manifest':str(manifest),'manifest_sha256':sha(manifest),'generated':{'path':str(folder/'ysyxSoCFull.v'),'sha256':sha(output),'bytes':output.stat().st_size,'modules':modules},'resources':resources,'budget':json.loads(budget.read_text()),'scope':'Actual pinned Mill/Chisel/firtool elaboration with ChipLink enabled in isolatedsource. Protocol/remote-memory acceptance not yet run.'})
    print('C5_CHIPLINK_GENERATED',len(modules),output.stat().st_size,flush=True)


if __name__=='__main__':main()
