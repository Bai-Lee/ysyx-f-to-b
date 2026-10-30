from pathlib import Path
import sys,json,struct,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    builds=json.loads((ROOT/'reports/C4_sim_build.json').read_text())['variants'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so';d=ROOT/'C/C4/results';d.mkdir(exist_ok=True)
    image=ROOT/'D/D8/results/trace-rv32e.bin';elf=ROOT/'D/D8/results/trace-rv32e.elf';rows=[]
    for mode in (4,6):
        bad=next(r for r in builds if r['mode']==mode and r['mutant']);exe=Path(bad['executable']);report=d/f'mutant-mode{mode}.json'
        o,e,r=run(f'C4/negative/mode{mode}-addi',[exe,'--image',image,'--elf',elf,'--ref',ref,'--report',report,'--random-delay','--backpressure','--core-delays','7'],inputs=[exe,ref,image,elf],outputs=[report],expected=(1,))
        result=json.loads(report.read_text());assert result['result']=='DIFF_FAIL' and result['instructions']==2 and 'pc=80000004' in e;rows.append({'mode':mode,'mutant':result})
    exe=Path(next(r['executable'] for r in builds if r['mode']==6 and not r['mutant']))
    cases=[('invalid',[0xffffffff],1),('x16',[0x00100813],2),('M-extension',[0x02b50533],1),('jump-align',[0x0020006f],3),('half-align',[0x800002b7,0x00129303],4),('word-align',[0x800002b7,0x0022a303],4),('DECERR',[0x500002b7,0x0002a503],5),('write-readonly-uart',[0x100002b7,0x00100313,0x0062a223],5),('read-unknown-uart',[0x100002b7,0x0082a503],5),('write-readonly-clint',[0x200002b7,0x00100313,0x0062a023],5)]
    rejects=[]
    for name,words,code in cases:
        binary=d/(name+'.bin');binary.write_bytes(struct.pack('<'+'I'*len(words),*words));report=d/(name+'.json')
        o,e,r=run('C4/negative/'+name,[exe,'--image',binary,'--ref',ref,'--report',report,'--backpressure','--random-delay'],inputs=[exe,ref,binary],outputs=[report],expected=(3,))
        result=json.loads(report.read_text());assert result['result']=='NPC_FAULT' and 'code='+str(code) in e and result['uart_bytes']==0
        rejects.append({'name':name,'fault_code':code,'simulation':result})
    # The RTL UART contract permits reading TX offset0 as zero. Do not impose
    # the older C++-only device's write-only rule on this distinct RTL model.
    binary=d/'uart-zero-read.bin';binary.write_bytes(struct.pack('<III',0x100002b7,0x0002a503,0x00100073));report=d/'uart-zero-read.json'
    run('C4/negative/uart-zero-read-positive',[exe,'--image',binary,'--ref',ref,'--report',report],inputs=[exe,ref,binary],outputs=[report])
    uart_read=json.loads(report.read_text());assert uart_read['result']=='GOOD_TRAP' and uart_read['a0']==0 and uart_read['uart_bytes']==0
    scripts={'steps':'si\ninfo r\np $sp\nx 2 0x80000000\nsi 1\np $t0\nq\n','watch':'w $t0\nw *0x80020000\nc\nc\nc\ninfo w\nd 0\nd 1\nc\nq\n','bad':'si 0\nsi -1\np $x16\np 1/0\nx 1 0\nd 31\ninfo z\nblah\nsi\nq\n'}
    sessions=[]
    for name,script in scripts.items():
        commands=d/(name+'.commands');commands.write_text(script);report=d/(name+'.sdb.json')
        o,e,r=run('C4/sdb/'+name,[exe,'--interactive','--image',image,'--elf',elf,'--ref',ref,'--report',report,'--backpressure','--random-delay','--core-delays','7'],inputs=[exe,ref,image,elf,commands],outputs=[report],stdin_file=commands)
        if name=='steps':assert 'PC 0x80000004' in o and 'EXPR_VALUE 2147549184' in o and 'EXPR_VALUE 5 ' in o
        if name=='watch':assert o.count('WATCH_HIT')==3 and 'WATCH_DELETED 0' in o and json.loads(report.read_text())['result']=='GOOD_TRAP'
        if name=='bad':assert o.count('COMMAND_ERROR')>=5 and o.count('EXPR_ERROR')>=2 and 'MEMORY_ERROR outside RAM' in o
        sessions.append({'name':name,'result':json.loads(report.read_text())})
    dump(ROOT/'reports/C4_negative_sdb.json',{'status':'PASS','real_RTL_addi_mutants':rows,'faults':rejects,'RTL_uart_read_zero':uart_read,'sdb':sessions,'scope':'Actual stalled RTL vs independent NEMU catches arithmetic mutation at second retirement; decode/alignment/AXI DECERR/SLVERR reject correctly. SDB steps/watchpoints advance architectural instructions despite variable cycle latency. RTL UART reads at TX offset return zero, distinct from old C++ write-only model.'})
    print('C4_NEGATIVE_SDB_PASS',flush=True)

if __name__=='__main__':main()
