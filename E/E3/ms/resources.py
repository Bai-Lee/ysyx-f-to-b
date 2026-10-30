from common import *
def main():
    dest=LAB/'resources';dest.mkdir(exist_ok=True);files=[]
    for name,url in [('vimrc','https://missing-semester-cn.github.io/2020/files/vimrc'),('example-data.xml','https://missing-semester-cn.github.io/2020/files/example-data.xml'),('regexone.html','https://regexone.com/'),('tmux.html','https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/'),('tmux-config.html','https://hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/')]:
        p=dest/name
        if not p.exists():run('resources/'+name,['curl','--fail','--location','--silent','--show-error','--max-time','45',url,'-o',str(p)],timeout=50)
        files.append({'name':name,'url':url,'path':str(p),'sha256':sha(p)})
    repos=[]
    for name,url,full in [('ctrlp','https://github.com/ctrlpvim/ctrlp.vim.git',False),('commentary','https://github.com/tpope/vim-commentary.git',False),('course','https://github.com/missing-semester-cn/missing-semester-cn.github.io.git',True)]:
        p=dest/name
        if not (p/'.git').exists():run('resources/git_'+name,['git','-c','http.version=HTTP/1.1','clone',* ([] if full else ['--depth','1']),url,str(p)],timeout=240)
        commit,_,_=run('resources/commit_'+name,['git','-C',str(p),'rev-parse','HEAD'])
        run('resources/fsck_'+name,['git','-C',str(p),'fsck','--full'],timeout=60)
        repos.append({'name':name,'url':url,'path':str(p),'commit':commit.strip(),'shallow':not full})
    dump(OUT/'resources/lock.json',{'files':files,'repos':repos})
    print('MS_RESOURCES_READY',flush=True)
if __name__=='__main__':main()
