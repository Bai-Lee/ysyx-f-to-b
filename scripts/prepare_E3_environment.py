"""Read-only host probes and official image staging; never installs/changes WSL."""
from evidence import *
import requests,re,platform

def main():
    if (ROOT/'reports/E3_import_result.json').exists():
        print('Initial preparation already recorded. Use Run-E3-Light.ps1 to verify the current environment; no setup proposal was overwritten.',flush=True)
        return
    workspace=ROOT.parents[1];out=ROOT/'E/E3/preflight';out.mkdir(parents=True,exist_ok=True)
    download=workspace/'downloads/ysyx_e3';download.mkdir(parents=True,exist_ok=True)
    probes=[]
    for name,args in [('status',['wsl.exe','--status']),('distributions',['wsl.exe','--list','--verbose']),('help',['wsl.exe','--help'])]:
        q=run('E3/preflight/'+name,args,timeout=20,expected=[0,4294967295]);folder=ROOT/'artifacts/E3/preflight'/name
        raw=(folder/'stdout.log').read_bytes();decoded=raw.decode('utf-16-le','replace') if b'\x00' in raw else raw.decode('utf8','replace')
        (folder/'stdout_utf8.txt').write_text(decoded,encoding='utf8');probes.append({'name':name,'execution':q,'text':decoded})
    url='https://cloud-images.ubuntu.com/wsl/jammy/current/'
    filename='ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz'
    checksum=requests.get(url+'SHA256SUMS',timeout=(15,30));checksum.raise_for_status();(download/'SHA256SUMS').write_bytes(checksum.content)
    expected=next(line.split()[0] for line in checksum.text.splitlines() if line.split()[-1].lstrip('*')==filename)
    archive=download/filename
    if not archive.exists() or sha(archive)!=expected:
        partial=download/(filename+'.partial')
        with requests.get(url+filename,stream=True,timeout=(15,45)) as response:
            response.raise_for_status()
            with partial.open('wb') as f:
                for chunk in response.iter_content(1024*1024):f.write(chunk)
        if sha(partial)!=expected:raise ValueError('Ubuntu upstream SHA-256 mismatch')
        if archive.exists():raise ValueError('Existing differently hashed image preserved; inspect before replacing')
        partial.replace(archive)
    config=Path(os.environ['USERPROFILE'])/'.wslconfig';existing=config.read_text('utf-8-sig') if config.exists() else ''
    changes={'memory':'2GB','processors':'4','swap':'2GB','swapFile':str(workspace/'temp/wsl-swap.vhdx').replace('\\','\\\\')}
    lines=existing.splitlines();inside=False;seen=set();output=[];section_seen=False
    def missing():
        for key,value in changes.items():
            if key.lower() not in seen:output.append(key+'='+value);seen.add(key.lower())
    for line in lines:
        section=re.fullmatch(r'\s*\[([^]]+)\]\s*',line)
        if section:
            if inside:missing()
            inside=section[1].lower()=='wsl2'
            if inside:
                if section_seen:raise ValueError('Duplicate wsl2 sections require review')
                section_seen=True
        item=re.match(r'\s*([^#;=]+?)\s*=.*',line)
        if inside and item:
            key=next((k for k in changes if k.lower()==item[1].strip().lower()),None)
            if key:
                if key.lower() in seen:raise ValueError('Duplicate WSL setting')
                line=key+'='+changes[key];seen.add(key.lower())
        output.append(line)
    if not section_seen:output+=['','[wsl2]']
    missing();proposal=out/'wslconfig.proposed';proposal.write_text('\n'.join(output).lstrip('\n')+'\n',encoding='utf8')
    record={'status':'AWAITING_USER_AUTHORIZATION','timestamp':datetime.now(timezone.utc).isoformat(),'actions_executed':'Read-only wsl status/list/help; download official Ubuntu rootfs; compare upstream SHA256; write proposal under project only.','system_modified':False,'probes':probes,'image':{'path':str(archive),'url':url+filename,'sha256':sha(archive),'expected_sha256':expected,'upstream_sha256_match':True,'sha256_source':url+'SHA256SUMS','bytes':archive.stat().st_size,'edition':'Ubuntu22.04 LTS amd64, official archived WSL rootfs; apt updates required after import.'},'proposed_distro_name':'YSYX-Linux','proposed_install_path':str(workspace/'tools/wsl/YSYX-Linux'),'wsl_config':{'path':str(config),'exists':config.exists(),'current_sha256':sha(config) if config.exists() else None,'proposal':str(proposal),'proposal_sha256':sha(proposal),'changes':changes},'authorization_basis':'/workspace/AGENTS.md: WSL/系统组件安装、重启、全局 .wslconfig 变更需用户批准。','references':['https://learn.microsoft.com/en-us/windows/wsl/basic-commands','https://learn.microsoft.com/en-us/windows/wsl/wsl-config','https://ubuntu.com/wsl/docs/latest/howto/install-ubuntu-wsl2/']}
    dump(ROOT/'reports/E3_ENVIRONMENT_PROPOSAL.json',record)
    text=f'''# E3 Linux环境待授权方案

当前只读探测：WSL默认版本2，内核文件缺失，没有已安装的发行版。尚未更新WSL、启用系统组件、导入Linux或修改用户.wslconfig。

已下载Canonical官方Ubuntu22.04 amd64 WSL根文件系统：{archive}。大小{archive.stat().st_size:,}字节；SHA-256={expected}，与同一官方站点发布的SHA256SUMS一致。原始镜像是2025-03快照，导入后要从官方apt源更新，不把旧快照当成已更新系统。

拟执行：更新缺失的WSL2内核及必要组件，将独立发行版YSYX-Linux导入/workspace/tools/wsl/YSYX-Linux。新发行版内安装课程所需编译/调试工具，继续E3。系统组件本身依Windows要求可能留在C盘，发行版及课程数据在D盘。

拟先备份并合并/home/USER/.wslconfig，只设置memory=2GB、processors=4、swap=2GB，以及D盘swapFile；其他设置保持原文。待应用文件见[配置草案](../E/E3/preflight/wslconfig.proposed)。这是全局WSL2资源上限，不是仅单个发行版设置。全局PATH、代理、Windows更新偏好不修改。

不会自动重启Windows。如果必要组件变更要求重启，将保留安装状态并请用户决定时机。开始Linux虚拟机或重编译前重新检测可用内存；低于项目3GiB门槛时不派发重任务，也不关闭用户应用。最近可用内存约2.27GiB。

需要用户授权的原因来自[AGENTS.md](/workspace/AGENTS.md)的明确规则：“WSL/系统组件安装、重启、全局 .wslconfig 变更需用户批准。”下载及方案准备已完成，系统修改尚未执行。

官方依据：[WSL更新/导入命令](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)、[全局资源配置](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)、[Ubuntu WSL安装](https://ubuntu.com/wsl/docs/latest/howto/install-ubuntu-wsl2/)。
'''
    (ROOT/'reports/E3_ENVIRONMENT_PROPOSAL.md').write_text(text,encoding='utf8')
    print('E3_PREPARED_NO_SYSTEM_CHANGES',archive.stat().st_size,expected,flush=True)

if __name__=='__main__':main()
