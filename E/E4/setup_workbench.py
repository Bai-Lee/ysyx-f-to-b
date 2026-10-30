from common import *
def main():
    workbench=Path('/home/USER/ysyx-workbench')
    bundle=Path('/workspace/downloads/ysyx_e4/nvboard.bundle')
    if not (NVBOARD/'.git').exists():
        NVBOARD.mkdir(exist_ok=True)
        assert not any(NVBOARD.iterdir()),'Preserve unexpected existing work'
        run('framework/nvboard_init',['git','init','-b','master',str(NVBOARD)])
        shallow=Path('/workspace/YSYX_F_B_Archive/repos/NJU-ProjectN__nvboard__master/.git/shallow')
        assert shallow.read_text().strip()=='b5f49b68a85f4a1a185086cbd6532fff3ecda454'
        shutil.copyfile(shallow,NVBOARD/'.git/shallow')
        run('framework/nvboard_unbundle',['git','bundle','unbundle',str(bundle)],inputs=[bundle,shallow],cwd=NVBOARD)
        run('framework/nvboard_head',['git','update-ref','refs/heads/master','b5f49b68a85f4a1a185086cbd6532fff3ecda454'],cwd=NVBOARD)
    if not (NVBOARD/'README.md').exists():
        assert all(p.name=='.git' for p in NVBOARD.iterdir())
        run('framework/nvboard_read_tree',['git','read-tree','--reset','-u','HEAD'],cwd=NVBOARD)
    o,e,r=run('framework/nvboard_commit',['git','rev-parse','HEAD'],cwd=NVBOARD);assert o.strip()=='b5f49b68a85f4a1a185086cbd6532fff3ecda454'
    run('framework/nvboard_fsck',['git','fsck','--full'],cwd=NVBOARD)
    run('framework/nvboard_submodules',['git','submodule','status','--recursive'],cwd=NVBOARD)
    # Task-local environment; no permanent Windows or Linux PATH edit.
    env=ROOT/'E/E4/env.sh';env.write_text('export VERILATOR_ROOT=/home/USER/tools/verilator-stable-src\nexport NVBOARD_HOME=/home/USER/ysyx-workbench/nvboard\nexport NPC_HOME=/home/USER/ysyx-workbench/npc\nexport PATH="$VERILATOR_ROOT/bin:$PATH"\n')
    backup=OUT/'framework/original';backup.mkdir(parents=True,exist_ok=True)
    for p in [workbench/'npc/Makefile',workbench/'Makefile',workbench/'AGENTS.md']:
        dest=backup/('npc_Makefile' if p.parent.name=='npc' else p.name)
        if not dest.exists():shutil.copyfile(p,dest)
    # init.sh npc only prints the process-local export when SHELL is unsupported.
    run('framework/init_npc',['bash','init.sh','npc'],cwd=workbench,env={'SHELL':'/bin/sh'})
    ignore=workbench/'.gitignore';text=ignore.read_text()
    if '/nvboard' not in text.splitlines():ignore.write_text(text+'\n/nvboard\n')
    run('framework/local_branch',['git','checkout','-B','e4-local'],cwd=workbench)
    dump(ROOT/'reports/E4_framework.json',{'status':'SOURCE_READY_NOT_SIMULATED','workbench_commit':'a839def3f3b046f730537ea420d3075e725d27ce','nvboard_commit':o.strip(),'nvboard_source_bundle':str(bundle),'bundle_sha256':sha(bundle),'init_adaptation':'Offline clone from archived official objects; per-process env.sh instead of persistent shell rc edits. Original upstream AGENTS retained; direct user requests autonomous AI engineering benchmark, no student-authorship claim.'})
    print('FRAMEWORK_READY',flush=True)
if __name__=='__main__':main()
