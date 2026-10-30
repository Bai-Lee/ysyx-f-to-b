from common7 import *
def main():
 BENCH7.mkdir(exist_ok=True);rows=[]
 for name in ['abstract-machine','am-kernels','riscv-tests','archbench','ysyxSoC']:
  dest=BENCH7/name
  if not dest.exists():shutil.copytree(BENCH/name,dest,ignore=shutil.ignore_patterns('.git','build','result','__pycache__','.result','Makefile-*','Makefile.*'))
  rows.append({'repository':name,'source':str(BENCH/name),'destination':str(dest),'source_marker':json.loads((BENCH/name/'.ysyx-source.json').read_text()) if (BENCH/name/'.ysyx-source.json').exists() else None})
 for name in ['Makefile','AGENTS.md','.gitignore']:
  if (BENCH/name).exists() and not (BENCH7/name).exists():shutil.copyfile(BENCH/name,BENCH7/name)
 ignore=BENCH7/'.gitignore';text=ignore.read_text()
 if '/nvboard' not in text.splitlines():ignore.write_text(text+'\n/nvboard\n')
 for d in ['npc','npc/csrc','npc/vsrc']:(BENCH7/d).mkdir(exist_ok=True)
 lib=BENCH7/'abstract-machine/klib/build';lib.mkdir(exist_ok=True)
 for arch in ['minirv-npc','minirv-ysyxsoc']:
  dst=lib/('klib-'+arch+'.a');shutil.copyfile(BENCH/'abstract-machine/klib/build/klib-minirv-npc.a',dst);dst.touch()
 nv=BENCH7/'nvboard'
 if not nv.exists():shutil.copytree(Path('/home/USER/ysyx-workbench/nvboard'),nv,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
 if not (BENCH7/'.git').exists():
  run('E7/setup/git_init',['git','init','-b','main'],cwd=BENCH7)
  run('E7/setup/git_identity_name',['git','config','user.name','YSYX autonomous local experiment'],cwd=BENCH7)
  run('E7/setup/git_identity_email',['git','config','user.email','local-experiment@invalid.local'],cwd=BENCH7)
 dump(ROOT/'reports/E7_workbench_sources.json',{'status':'COPIED_NOT_YET_VALIDATED','repositories':rows,'policy':'Separate E7 workbench prevents its UART/CSR/SoC patches from changing E6 performance runs. Original downloaded archives and E6 workbench remain intact.'})
 print('E7_ISOLATED_WORKBENCH_READY',flush=True)
if __name__=='__main__':main()
