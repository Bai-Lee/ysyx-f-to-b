from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iverilog=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iverilog.parent/'vvp'
base=ROOT/'C/C5/perip/sdram';ext=base/'c5_sdram32_controller.v';out=WORK/'c5/sdram-controller-unit';out.mkdir(parents=True,exist_ok=True);rows=[]
cases=[('16x1',16,1,None),('32x1',32,1,None),('32x2',32,2,None),('bad-mask',32,2,('sdram_dqm<=~strobe','sdram_dqm<=0')),('bad-rank',32,2,('wire selected_rank=(RANKS==2)&&address[26];','wire selected_rank=0;'))]
for name,width,ranks,mutation in cases:
    implementation=ext
    if mutation:
        text=ext.read_text();assert text.count(mutation[0])==1;implementation=out/(name+'.v');implementation.write_text(text.replace(*mutation))
    sources=[base/'sdram.v',base/'sdram_top_apb.v',base/'core_sdram_axi4/sdram_axi_core.v',implementation,ROOT/'C/C5/rtl_tests/sdram_controller_tb.sv']
    image=out/(name+'.vvp');tag='C5/sdram-controller/'+name
    run(tag+'/compile',[iverilog,'-g2012',f'-DC5_SDRAM_DQ={width}',f'-DC5_SDRAM_RANKS={ranks}','-s','sdram_controller_tb','-o',image,*sources],inputs=sources,outputs=[image],timeout=60)
    expected=1 if mutation else 0;text,err,record=run(tag+'/run',[vvp,image],inputs=[image],expected=(expected,),timeout=30)
    assert ('SDRAM_CONTROLLER_READ' if mutation else 'SDRAM_CONTROLLER_PASS') in text+err
    rows.append({'name':name,'width':width,'ranks':ranks,'status':'PASS','expected_exit':expected,'stdout':text,'evidence':'artifacts/'+tag,'implementation_sha256':sha(implementation)})
dump(ROOT/'reports/C5_sdram_controller.json',{'status':'PASS_SMALL_FOUR_STATE_CONTROLLER_AND_RANK_TESTS','runs':rows,'scope':'Original16-bit core unchanged; parallel32-bit one/two-rank controller uses2/4 independentx16 chip models. APB byte/halfword masks, column/bank/row/rank boundaries, refresh and warmreset retention. Small8row models only; actual32/64/128MiB CPU tests separate. Broken byte mask and rank-select mutants rejected. No real-board electrical timing claim.'})
print('C5_SDRAM_CONTROLLERS_PASS',flush=True)
