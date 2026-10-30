"""Reassemble early minirv fixtures for the D memory map; retain original E files."""
from pathlib import Path
import sys, struct, importlib.util
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from common import *

BASE = 0x80000000
MASK = 0xffffffff

def oracle(blob, steps=0):
    memory = bytearray(1024*1024); memory[:len(blob)] = blob
    r = [0]*16; pc = BASE
    for count in range(1, (steps or 20000)+1):
        inst = int.from_bytes(memory[pc-BASE:pc-BASE+4], 'little')
        op = inst & 127; rd = (inst >> 7) & 31; a = (inst >> 15) & 31; b = (inst >> 20) & 31; f = (inst >> 12) & 7
        imm = inst >> 20; imm -= 4096 if imm & 2048 else 0
        nxt = (pc+4) & MASK; value = None
        if inst == 0x00100073: return {'gpr':r, 'pc':nxt, 'instructions':count}
        if op == 0x13: value = (r[a]+imm) & MASK
        elif op == 0x33: value = (r[a]+r[b]) & MASK
        elif op == 0x37: value = inst & 0xfffff000
        elif op == 0x17: value = (pc+(inst & 0xfffff000)) & MASK
        elif op == 0x67: nxt = ((r[a]+imm) & MASK) & ~1; value = pc+4
        elif op == 0x6f:
            offset = ((inst>>31)<<20)|(((inst>>12)&255)<<12)|(((inst>>20)&1)<<11)|(((inst>>21)&1023)<<1)
            if offset & (1<<20): offset -= 1<<21
            nxt=(pc+offset)&MASK; value=pc+4
        elif op in (3,0x23):
            if op == 0x23:
                imm=((inst>>25)<<5)|((inst>>7)&31); imm-=4096 if imm&2048 else 0
            n = 1 if f in (0,4) else 4; address=(r[a]+imm)&MASK
            assert BASE <= address and address+n <= BASE+len(memory)
            off=address-BASE
            if op == 3: value=int.from_bytes(memory[off:off+n],'little')
            else: memory[off:off+n]=(r[b] & ((1<<(8*n))-1)).to_bytes(n,'little')
        else: raise AssertionError(hex(inst))
        if value is not None and rd: r[rd]=value&MASK
        r[0]=0; pc=nxt
    assert steps
    return {'gpr':r, 'pc':pc, 'instructions':steps}

def jal(rd, off):
    v=off & ((1<<21)-1)
    return (((v>>20)&1)<<31)|(((v>>1)&1023)<<21)|(((v>>11)&1)<<20)|(((v>>12)&255)<<12)|(rd<<7)|0x6f

def main():
    d=ROOT/'D/D8/results/prior';d.mkdir(parents=True,exist_ok=True)
    lock=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(lock['executable']);ref=Path(lock['reference'])
    original=json.loads((ROOT/'reports/E5_vectors.json').read_text());rows=[]
    ld=ROOT/'D/D7/baremetal.ld'
    for case in ([] if '--timer-only' in sys.argv else original['cases']):
        name=case['name'];old=Path(case['path']);assert sha(old)==case['sha256']
        words=list(struct.unpack('<'+'I'*(old.stat().st_size//4),old.read_bytes()));adapt=[]
        if name.startswith('six_'):
            for i,w in enumerate(words):
                if (w&127)==0x67 and ((w>>15)&31)==0:
                    words[i]=jal((w>>7)&31,(w>>20)-4*i)
            adapt=['Absolute zero-base JALR becomes a PC-relative JAL to the same relocated label.']
        elif name=='jalr_alias_odd':
            words=[0x00000097,0x01508093,0x000080e7,0x06300513,0x00100073,0x01608513,0x00100073]
            adapt=['AUIPC+ADDI creates the relocated odd target; expected link value includes the new RAM base.']
        elif name=='memory_endian':
            words[0] |= BASE;adapt=['Data address relocated from 0x00040000 to 0x80040000.']
        elif name=='random_ops':
            words[0] |= BASE
            for i in range(1,len(words)-2):
                if words[i]&0xfff==0x0b7 and words[i+2]==0x000080e7: words[i] |= BASE
            adapt=['Data base and absolute generated JALR targets relocated; random seed and operation stream retained.']
        elif name=='address_wrap':
            adapt=['Original wrap to address zero is now an invalid access: D RAM starts at 0x80000000. Retained as an expected rejection, with arithmetic wrapping separately covered in D8_isa.']
        source=d/(name+'.S');source.write_text('.option norvc\n.section .text\n.globl _start\n_start:\n'+''.join(f'.word 0x{w:08x}\n' for w in words))
        elf=d/(name+'.elf');image=d/(name+'.bin');report=d/(name+'.json')
        run('D8/prior/'+name+'/compile',['riscv64-linux-gnu-gcc','-march=rv32e','-mabi=ilp32e','-nostdlib','-nostartfiles','-static','-Wl,--build-id=none','-T',ld,source,'-o',elf],inputs=[old,source,ld],outputs=[elf])
        run('D8/prior/'+name+'/objcopy',['riscv64-linux-gnu-objcopy','-O','binary',elf,image],inputs=[elf],outputs=[image])
        attrs,_,_=run('D8/prior/'+name+'/abi',['riscv64-linux-gnu-readelf','-h','-A',elf],inputs=[elf]);assert 'RVE' in attrs and 'rv32e' in attrs
        negative=bool(case['error']) or name=='address_wrap';steps=case['steps']
        expect=None if negative else oracle(image.read_bytes(),steps)
        rc=3 if negative else (1 if expect['gpr'][10] and not steps else 0)
        args=[exe,'--image',image,'--ref',ref,'--elf',elf,'--report',report];feed=None
        if steps:
            feed=d/(name+'.commands');feed.write_text(f'si {steps}\nq\n');args.append('--interactive')
        _,err,_=run('D8/prior/'+name+'/run',args,inputs=[exe,ref,image,elf],outputs=[report],expected=(rc,),stdin_file=feed)
        result=json.loads(report.read_text())
        if negative:
            assert result['result'] in ('NPC_FAULT','MEMORY_ERROR') and ('NPC_FAULT' in err or 'MEMORY_ERROR' in err)
        else:
            for key in ('gpr','pc','instructions'):assert result[key]==expect[key],(name,key,result[key],expect[key])
            assert result['diff_checked']==result['instructions'] and result['device_sync_checked']==0
            assert result['result']==('USER_QUIT' if steps else 'BAD_TRAP' if rc else 'GOOD_TRAP')
        rows.append({'name':name,'status':'PASS_EXPECTED_REJECTION' if negative else 'PASS_BOUNDED_STEPS' if steps else 'PASS_EXPECTED_ARCHITECTURAL_STATE','source_original_sha256':case['sha256'],'adaptations':adapt,'expected':expect,'simulation':result,'evidence':'artifacts/D8/prior/'+name})
    if rows:dump(ROOT/'reports/D8_prior_tests.json',{'status':'PASS','case_count':len(rows),'seed':original['seed'],'rows':rows,'scope':'All 12 early authored fixtures accounted for. Reassembled words retain an RVE ELF envelope; reserved encodings deliberately remain negative tests. Nonzero a0 fixtures deliberately produce BAD_TRAP and are checked against their independent expected register state.'})
    kernels=BENCH/'am-kernels';am=BENCH/'abstract-machine';cwd=kernels/'tests/am-tests';report=cwd/'build/amtest-riscv32e-npc.bin.npc.json'
    # The unchanged menu references PA3 interrupt functions even in timer mode.
    # Supply test-local fail-fast link entries, never fake successful interrupts.
    support=ROOT/'D/D8/timer_trm_only.c'
    sources=sorted(p for p in (cwd/'src').rglob('*') if p.suffix in ('.c','.S'))
    menu_make=ROOT/'D/D8/timer_menu.mk'
    command=['make','-j1','-f',menu_make,'ARCH=riscv32e-npc','run']
    o,e,_=run('D8/devices/official_timer',command+['mainargs=t',"NPC_ARGS=--wall-timer --until-output 'seconds).' --until-count 2"],cwd=cwd,inputs=[exe,ref,support,menu_make,am/'am/src/riscv/npc/timer.c',*sources],outputs=[report,cwd/'build/amtest-riscv32e-npc.elf'],timeout=180)
    result=json.loads(report.read_text());assert result['result']=='BOUNDED_OUTPUT_OBSERVATION'
    assert all(f'{n} second' in o for n in (1,2,3))
    assert result['diff_checked']+result['device_sync_checked']==result['instructions']
    o,e,_=run('D8/devices/interrupt_unavailable',command+['mainargs=i'],cwd=cwd,inputs=[exe,ref,support,*sources],outputs=[report],expected=(2,),timeout=30)
    rejection=json.loads(report.read_text());assert rejection['result']=='BAD_TRAP' and 'D_STAGE_NO_CTE' in o
    dump(ROOT/'reports/D8_timer.json',{'status':'PASS_BOUNDED_OBSERVATION','observed_seconds':[1,2,3],'simulation':result,'unavailable_interrupt_negative':rejection,'evidence':'artifacts/D8/devices/official_timer','scope':'Unchanged official infinite AM timer program, semantic output stop; not a timeout or completed program. Test-local CTE link stubs fail explicitly, verified by selecting the interrupt menu; no interrupt implementation claim.'})

if __name__=='__main__':main()
