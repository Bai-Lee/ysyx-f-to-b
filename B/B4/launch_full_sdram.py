from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jobs',type=int,default=4);args=parser.parse_args();assert 1<=args.jobs<=8
    script=ROOT/'B/B4/parallel_sdram.py';folder=ROOT/'artifacts/B4/full128-job';folder.mkdir(parents=True,exist_ok=True)
    for label in ['release-pilot4k','release-pilot4k-bad','release-pilot64k']:
        report=json.loads((ROOT/'artifacts/B4/parallel-sdram'/label/'summary.json').read_text());assert report['status']=='PASS'
    for proc in Path('/proc').glob('[0-9]*'):
        try:cmd=(proc/'cmdline').read_bytes().decode(errors='replace').split('\0')
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
        if str(script) in cmd and 'release-full128' in cmd:raise RuntimeError('Full-address validation already active: '+proc.name)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');stdout=folder/(stamp+'.stdout.log');stderr=folder/(stamp+'.stderr.log')
    command=['python3',script,'--bytes','134217728','--jobs',str(args.jobs),'--label','release-full128','--pilot-label','release-pilot64k']
    with stdout.open('xb') as out,stderr.open('xb') as err:process=subprocess.Popen(list(map(str,command)),cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True,close_fds=True)
    dump(folder/(stamp+'.json'),{'status':'LAUNCHED_NOT_ACCEPTED','pid':process.pid,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'command':list(map(str,command)),'stdout':str(stdout),'stderr':str(stderr),'scope':'Eight original width/address/inverse patterns, each independently traversing the entire128MiB. Worker count adapts to current RAM and available shared simulator slots; no address partitioning.'})
    print('B_FULL128_LAUNCHED',process.pid)
if __name__=='__main__':main()
