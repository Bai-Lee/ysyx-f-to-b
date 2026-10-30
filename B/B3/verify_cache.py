from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    rtl=ROOT/'B/soc/rtl/ysyx_00000000_icache.sv';cpp=ROOT/'B/B3/cache_test.cpp';rows=[]
    for lines,words,ways,burst,bad,pipelined in [(16,1,1,0,0,0),(16,4,1,0,0,0),(16,4,1,1,0,0),(16,4,2,1,0,0),(8,8,2,1,0,0),(16,1,1,0,1,0),(4,8,2,1,0,1)]:
        label=f'cache-l{lines}-w{words}-a{ways}-b{burst}-bad{bad}'+('-pipe' if pipelined else '');out=WORK/'b3/unit'/label;out.mkdir(parents=True,exist_ok=True);exe=out/'sim'
        run('B3/unit/'+label+'/build',[VERILATOR,'--cc','--exe','--build','-j','4','--trace','--assert','-Wall','-Wno-fatal','--top-module','ysyx_00000000_icache','--Mdir',out,'-o','sim',f'-GLINES={lines}',f'-GWORDS={words}',f'-GWAYS={ways}',f'-GUSE_BURST={burst}',f'-GFAULT_TAG={bad}',f'-GPIPELINED={pipelined}',rtl,cpp],inputs=[VERILATOR,rtl,cpp],outputs=[exe],timeout=180,resume=True)
        wave=ROOT/'artifacts/B3/unit'/label/'transactions.vcd'
        text,err,_=run('B3/unit/'+label+'/run',[exe,wave,str(pipelined)],inputs=[exe],outputs=[wave],expected=(1 if bad else 0,));assert ('CACHE_DATA_MISMATCH' in err) if bad else ('ICACHE_PASS' in text)
        rows.append({'lines':lines,'words':words,'ways':ways,'burst':burst,'negative':bool(bad),'status':'PASS_TAG_FAULT_REJECTED' if bad else 'PASS','result':text.strip(),'wave':str(wave),'wave_sha256':sha(wave),'evidence':'artifacts/B3/unit/'+label})
    dump(ROOT/'reports/B3_icache_unit.json',{'status':'PASS','runs':rows,'seed':'0x2607b301','scope':'Independent data function, randomized memory/CPU backpressure, conflicting tags, full line words,1/2ways,1/4/8word lines, single/INCR burst reads, flash serial fill, SRAM/MMIO bypass, backing-memory edits followed by invalidation. Finite test suite, not universal proof.'})
    print('B3_ICACHE_UNIT_PASS')

if __name__=='__main__':main()
