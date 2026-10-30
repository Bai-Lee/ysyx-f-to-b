from common import *
from resource_policy import load_policy

def main():
    old=json.loads((ROOT/'reports/D_toolchain_final.json').read_text());tools=[]
    for row in old['inherited_tools']:
        assert sha(row['path'])==row['sha256'],row['path'];tools.append({**row,'C_fingerprint_match':True})
    d=WORK/'preflight';d.mkdir(parents=True,exist_ok=True)
    source=d/'control.c';source.write_text('int main(void){volatile unsigned a=7,b=9;return (a+b==16)?0:1;}\n')
    binary=d/'control';run('C/preflight/host_compile',['gcc','-Wall','-Wextra','-Werror',source,'-o',binary],inputs=[source],outputs=[binary]);run('C/preflight/host_positive',[binary],inputs=[binary])
    bad=d/'bad.c';bad.write_text('int main(void){return undefined_name;}\n');run('C/preflight/host_negative',['gcc','-Wall','-Werror',bad,'-o',d/'bad'],inputs=[bad],expected=(1,))
    npc=BENCH/'npc';exe=npc/'build/sim';ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    run('C/preflight/npc_rebuild',['make','-j1'],cwd=npc,inputs=[npc/'Makefile',*sorted((npc/'vsrc').glob('*.sv')),*sorted((npc/'csrc').glob('*'))],outputs=[exe],timeout=300)
    image=ROOT/'D/D8/results/trace-rv32e.bin';elf=ROOT/'D/D8/results/trace-rv32e.elf';report=d/'npc.json'
    run('C/preflight/npc_positive',[exe,'--image',image,'--elf',elf,'--ref',ref,'--report',report],inputs=[exe,ref,image,elf],outputs=[report])
    r=json.loads(report.read_text());assert r['result']=='GOOD_TRAP' and r['diff_enabled'] and r['diff_checked']==r['instructions']
    invalid=d/'invalid.bin';invalid.write_bytes(bytes.fromhex('ffffffff'));badreport=d/'invalid.json'
    run('C/preflight/npc_negative',[exe,'--image',invalid,'--ref',ref,'--report',badreport],inputs=[exe,ref,invalid],outputs=[badreport],expected=(3,));assert json.loads(badreport.read_text())['result']=='NPC_FAULT'
    dump(ROOT/'reports/C_PREFLIGHT.json',{'status':'PASS_FOUNDATION_PENDING_SOC_GENERATOR_AND_NEW_MODELS','tools':tools,'scope':['C/C++ and RV32 compilation','Existing RV32E DUT rebuilt in C workspace, actual NEMU REF comparison and illegal-instruction negative','Retained Icarus/Yosys/Graphviz fingerprints unchanged; rerun feature-specific controls when new models or flow are introduced'],'unresolved':['Course C5 2607 source snapshot differs from old full-SoC tutorial; compatible official fixed ysyx6 commit being obtained','Actual Mill/Chisel/firtool generation still requires acceptance','AXI4/Lite official older specification supplement; course linked Issue K removed those protocols','IS66 PSRAM, MT48 SDRAM, SPI XIP, ChipLink and RT-Thread synchronous traps are new tasks, not yet accepted'],'resource_policy':load_policy(),'D_unchanged':True,'evidence':'artifacts/C/preflight'})
    print('C_PREFLIGHT_FOUNDATION_PASS',flush=True)

if __name__=='__main__':main()
