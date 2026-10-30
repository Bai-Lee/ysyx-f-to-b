from common import *
def main():
    d=json.loads((ROOT/'reports/E4_tools.json').read_text())
    for name,row in d['tools'].items():assert sha(row['path'])==row['sha256'],name
    for name in ['Makefile','.gitignore','vsrc/dual.sv','csrc/dual_main.cpp']:
        assert sha(ROOT/'E/E4/npc'/name)==sha(Path('/home/USER/ysyx-workbench/npc')/name),name
    mem={line.split(':')[0]:int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines()}
    assert 1800000<mem['MemTotal']<=2097152 and mem['SwapTotal']==2097152 and os.cpu_count()==4
    live=[]
    for p in Path('/proc').glob('[0-9]*'):
        try:
            name=(p/'comm').read_text().strip();status=(p/'status').read_text()
            if name in ['lab_board','gtkwave','Xvfb'] and '\nState:\tZ' not in status:live.append({'pid':p.name,'name':name})
        except (OSError,ProcessLookupError):pass
    assert not live,live
    binding=OUT/'board/auto_bind.cpp';shutil.copyfile(WORK/'auto_bind.cpp',binding)
    source=ROOT/'E/E4/sources';lines=['# 原讲义快照与可浏览入口','', '本目录保留原Markdown字节及原相对链接语境，用于来源核对。完整可离线浏览的HTML继续位于已归档资料库，工程ZIP不重复整个资料库。','']
    seen=set()
    for r in json.loads((ROOT/'E/E4/course_specs.json').read_text())['tasks']:
        s=r['source']
        if s['url'] in seen:continue
        seen.add(s['url']);lines.append('- ['+s['version']+' '+s['url']+'](/workspace/YSYX_F_B_Archive/'+s['offline']+')')
    (source/'README.md').write_text('\n'.join(lines)+'\n')
    dump(ROOT/'reports/E4_runtime.json',{'status':'PASS','tool_hashes_verified':len(d['tools']),'memory_total_kib':mem['MemTotal'],'swap_total_kib':mem['SwapTotal'],'processors':os.cpu_count(),'remaining_live_GUI_processes':live,'binding_sha256':sha(binding),'budget':'One heavy task; source Verilator build-j1, model builds<=j2; no global PATH or .wslconfig changes in E4.'})
    print('RUNTIME_LOCK_AND_CLEANUP_PASS',flush=True)
if __name__=='__main__':main()
