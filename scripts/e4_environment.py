from evidence import *
import argparse

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['dependencies','source']);args=p.parse_args()
    if args.action=='dependencies':
        script=ROOT/'E/E4/bootstrap.sh'
        r=run('E4/environment/dependencies',['wsl.exe','-d','YSYX-Linux','-u','root','--exec','bash','/workspace/projects/ysyx_f_to_b/E/E4/bootstrap.sh'],[script],timeout=900)
    else:
        cmd='''set -eu
mkdir -p /home/USER/tools
if [ ! -d /home/USER/tools/verilator-stable-src/.git ]; then
 git -c http.version=HTTP/1.1 clone --depth 1 --branch stable https://github.com/verilator/verilator.git /home/USER/tools/verilator-stable-src
fi
git -C /home/USER/tools/verilator-stable-src rev-parse HEAD
git -C /home/USER/tools/verilator-stable-src describe --tags --always
git -C /home/USER/tools/verilator-stable-src fsck --full
head -35 /home/USER/tools/verilator-stable-src/Changes
'''
        r=run('E4/environment/source',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','bash','-lc',cmd],timeout=300)
    dump(ROOT/'reports'/('E4_'+args.action+'.json'),r)
    assert r['status']=='PASS'
if __name__=='__main__':main()
