"""Apply the narrowly authorized WSL resource settings and update kernel.
Never restarts Windows, changes Windows Update preferences or global PATH.
"""
from evidence import *
import shutil

def main():
    if (ROOT/'reports/E3_toolchain.json').exists():
        print('Initial environment acceptance already recorded. Use the verifier; current resource settings were not changed.',flush=True)
        return 0
    authorization=ROOT/'config/E3_authorization.json';auth=json.loads(authorization.read_text('utf8'));assert auth['answer']=='授权安装和上述资源配置' and not auth['automatic_Windows_reboot_authorized']
    proposal=ROOT/'reports/E3_ENVIRONMENT_PROPOSAL.json';p=json.loads(proposal.read_text('utf8'));setting=p['wsl_config'];config=Path(setting['path']);draft=Path(setting['proposal'])
    assert sha(draft)==setting['proposal_sha256'];assert sha(p['image']['path'])==p['image']['expected_sha256']
    recordpath=ROOT/'reports/E3_environment_actions.json';record=json.loads(recordpath.read_text('utf8')) if recordpath.exists() else {'authorization':str(authorization),'actions':[]}
    if not config.exists() or sha(config)!=sha(draft):
        if setting['exists']:assert config.exists() and sha(config)==setting['current_sha256'],'Config changed concurrently'
        else:assert not config.exists(),'Config appeared concurrently'
        backup=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');backup.mkdir(parents=True)
        dump(backup/'wslconfig_before.json',{'path':str(config),'existed':config.exists(),'sha256':sha(config) if config.exists() else None})
        if config.exists():shutil.copyfile(config,backup/'wslconfig.before')
        shutil.copyfile(draft,config)
        record['actions'].append({'type':'wslconfig_authorized_merge','status':'PASS','path':str(config),'sha256':sha(config),'backup':str(backup),'scope':'memory2GB/processors4/swap2GB/D:swapFile only'})
        dump(recordpath,record)
    q=run('E3/wsl_update',['wsl.exe','--update','--web-download'],[authorization,proposal,draft],timeout=300)
    raw=(ROOT/'artifacts/E3/wsl_update/stdout.log').read_bytes();text=raw.decode('utf-16-le','replace') if b'\x00' in raw else raw.decode('utf8','replace')
    (ROOT/'artifacts/E3/wsl_update/stdout_utf8.txt').write_text(text,encoding='utf8');print(text,flush=True)
    record['actions'].append({'type':'wsl_update','execution':q});record['status']='KERNEL_UPDATE_COMMAND_PASS_CHECK_REQUIRED' if q['status']=='PASS' else 'UPDATE_NEEDS_DIAGNOSIS';dump(recordpath,record)
    return 0 if q['status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
