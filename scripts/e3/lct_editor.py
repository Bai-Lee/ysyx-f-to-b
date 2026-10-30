from pathlib import Path
import sys,json,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *
from lct_early import lp,original,SOLUTION,BIN

def main():
    folder=ROOT/'artifacts/E3/lcthw/editor';folder.mkdir(parents=True,exist_ok=True);runs=[]
    def linux(name,args,inputs,expected=0):
        q=run('E3/lcthw/editor/'+name,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec',*map(str,args)],inputs,expected=expected,timeout=30);assert q['status']=='PASS';runs.append(q)
    good=BIN/'ex1_more_lines.elf';bad=folder/'ex1_vim_corrupted.elf'
    shutil.copyfile(good,bad);before=bad.read_bytes()
    linux('binary_edit',['vim','-u','NONE','-U','NONE','-i','NONE','-n','-es','-b','-c','set noeol','-c','normal! gg0rX','-c','wq',lp(bad)],[good])
    after=bad.read_bytes();assert len(before)==len(after) and [i for i,(x,y) in enumerate(zip(before,after)) if x!=y]==[0]
    linux('corrupted_execute',['bash','-c',lp(bad)],[bad],126)
    src=folder/'ex6_vim_fixed.c';orig=original(6);shutil.copyfile(orig,src)
    linux('source_edit',['vim','-u','NONE','-U','NONE','-i','NONE','-n','-es','-c','normal! ggI#','-c','wq',lp(src)],[orig])
    assert sha(src)==sha(SOLUTION/'ex6.c')
    exe=folder/'ex6_vim.elf'
    linux('compile',['gcc','-std=c17','-Wall','-Werror','-g',lp(src),'-o',lp(exe)],[src])
    linux('valgrind',['valgrind','--error-exitcode=99',lp(exe)],[src,exe])
    assert 'ERROR SUMMARY: 0 errors' in (ROOT/'artifacts/E3/lcthw/editor/valgrind/stderr.log').read_text('utf8')
    dump(ROOT/'reports/E3_LCT_editor_results.json',{'status':'PASS','scope':'Actual Vim binary/text editing; no GUI or user editor configuration changes. Good sources preserved.','runs':runs,'binary_changed_positions':[0],'vim_repair_matches_previously_validated_source':True})
    print('E3_VIM_EDITING_PASS',flush=True)

if __name__=='__main__':main()
