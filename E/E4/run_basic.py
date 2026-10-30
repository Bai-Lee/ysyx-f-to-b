from common import *
def main():
    official=ROOT/'E/E4/official';rtl=ROOT/'E/E4/rtl';cpp=ROOT/'E/E4/csrc'
    o,e,r=run('tools/versions',[VERILATOR,'--version'],inputs=[VERILATOR,VROOT/'bin/verilator_bin']);assert '5.052' in o
    exe=build('our',[official/'our.v'],official/'sim_main.cpp','official',trace=False)
    o,e,r=run('official/example',[exe],inputs=[exe]);assert 'Hello World' in o and '$finish' in o
    exe=build('dual',[rtl/'dual.sv'],cpp/'dual_test.cpp','dual')
    o,e,r=run('basic/dual',[exe],inputs=[exe]);assert 'PASS XOR' in o
    waves=OUT/'waves';waves.mkdir(exist_ok=True);shutil.copyfile(WORK/'dual.vcd',waves/'dual.vcd')
    bad=build('dual',[rtl/'dual.sv'],cpp/'dual_test.cpp','dual_bad',defines=['FAULT_XOR'])
    o,e,r=run('basic/xor_negative',[bad],inputs=[bad],expected=(1,));assert 'a=1 b=1 actual=1 expected=0' in e
    fst=build('dual',[rtl/'dual.sv'],cpp/'dual_test.cpp','dual_fst',trace=False,flags=['--trace-fst','-CFLAGS','-DTRACE_FST'])
    o,e,r=run('basic/fst',[fst],inputs=[fst]);assert 'PASS XOR' in o;shutil.copyfile(WORK/'dual.fst',waves/'dual.fst')
    run('tools/iverilog',['iverilog','-V'])
    result(['E4-M001','E4-M002','E4-M003','E4-M004'],['reports/E4_verilator_build.json','artifacts/E4/official/example','artifacts/E4/basic/dual','artifacts/E4/basic/xor_negative'],'Official fixed stable Linux source build and C++ example actually execute; bounded XOR exhaustive patterns and real wrong-RTL rejection, no version-only readiness claim.')
    print('BASIC_TOOLCHAIN_PASS',flush=True)
if __name__=='__main__':main()
