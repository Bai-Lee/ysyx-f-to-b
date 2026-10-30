from evidence import *
def main():
    cmd='''set -eu
cd /home/USER/tools/verilator-stable-src
test "$(git rev-parse HEAD)" = 983a06a16f2aea1cf4bda3a45099c8bad24d112c
autoconf
./configure --prefix=/home/USER/tools/verilator-5.052
make -C src -j1 opt
export VERILATOR_ROOT=$PWD
./bin/verilator --version
'''
    r=run('E4/environment/build_verilator',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','bash','-lc',cmd],[Path(__file__)],timeout=1800)
    dump(ROOT/'reports/E4_verilator_build.json',{'status':r['status'],'scope':'Official stable 5.052 commit983a06a; optimized executable, run-in-place; debug/coverage utilities not built','jobs':1,'run':r});assert r['status']=='PASS'
if __name__=='__main__':main()
