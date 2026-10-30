"""Produce the public single-file, synthesizable release RTL entrypoint."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
import re

DEFINES=['-DSYNTHESIS',"-DC5_RESET_PC=32'h30000000",'-DB_PIPELINE=1',
         '-DB_FORWARD=1','-DB_PREDICT=2','-DB_FETCH_PIPELINED=1',
         '-DB_ICACHE_ENABLE=1','-DB_ICACHE_LINES=4','-DB_ICACHE_WORDS=8',
         '-DB_ICACHE_WAYS=2','-DB_ICACHE_BURST=1']

def main():
    source=ROOT/'B/soc/rtl';files=[*sorted(source.glob('*.v')),*sorted(source.glob('*.sv'))]
    target=ROOT/'B/soc/build/ysyx_00000000.sv';target.parent.mkdir(exist_ok=True)
    raw=ROOT/'B/B5/export/unsanitized.sv';raw.parent.mkdir(exist_ok=True)
    iv=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin/iverilog')
    run('B5/export/preprocess',[iv,'-g2012','-E','-o',raw,*DEFINES,*files],inputs=[iv,*files,Path(__file__)],outputs=[raw])
    text=raw.read_text()
    # Syntax-only normalization: all comparisons stay unsigned32; logical truth
    # of integer PREDICT is explicitly !=0; names do not change generated logic.
    assert text.count('beat==WORDS-1')==3 and text.count('PREDICT&&')==2
    text=text.replace('beat==WORDS-1',"beat_word==32'(WORDS-1)").replace('PREDICT&&','(PREDICT!=0)&&')
    old='if(g==0)assign debug_gpr[g*32+:32]=0;else assign debug_gpr[g*32+:32]=r[g];'
    assert text.count(old)==1
    text=text.replace(old,'if(g==0)begin : zero_register\n      assign debug_gpr[g*32+:32]=0;\n    end else begin : other_registers\n      assign debug_gpr[g*32+:32]=r[g];\n    end')
    target.write_text(text)
    assert 'module ysyx_00000000(' in text and "32'h30000000" in text
    assert 'DPI-C' not in text and 'negedge' not in text
    run('B5/export/compile',[iv,'-g2012','-s','ysyx_00000000','-t','null',target],inputs=[iv,target])
    dump(ROOT/'reports/B5_export.json',{'status':'PASS','project_id':'00000000',
        'path':str(target),'sha256':sha(target),'reset_pc':'0x30000000','defines':DEFINES,
        'sources':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in files],
        'normalization':['Explicit zero extension of beat in three comparisons','Explicit integer-to-Boolean comparison for PREDICT in two expressions','Names for the two generate alternatives'],
        'scope':'Public single-file SystemVerilog contract, generated reproducibly from the accepted RTL. Bit widths and generate labels are normalized without changing logic; equivalence is checked separately. Simulation DPI and event counters are excluded; project ID is not an official student identity.'})
    print('B5_EXPORT_PASS',target,sha(target))

if __name__=='__main__':main()
