"""Reproducibly resize two slew-violating NOR drivers; preserve connectivity."""
from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from verify_cells import blocks

def main():
    base=ROOT/'B/B3/synthesis/b5-release-cpu';original=base/'mapped.v';lib=ROOT/'B/models/nangate45/lib/Nangate45_typ.lib'
    source_record=next(r for r in json.loads((ROOT/'reports/B3_synthesis.json').read_text())['variants'] if r['name']=='b5-release-cpu');assert sha(original)==source_record['netlist_sha256']
    cells=blocks(re.sub(r'/\*.*?\*/','',lib.read_text(),flags=re.S),'cell')
    for name in ['NOR4_X1','NOR4_X2']:
        pins=blocks(cells[name],'pin');functions={k:re.search(r'function\s*:\s*"([^"]+)"',v)[1] for k,v in pins.items() if 'direction\t\t: output' in v or re.search(r'direction\s*:\s*output',v)}
        if name.endswith('X1'):expected=functions
        else:assert functions==expected
    out=ROOT/'B/B5/netlist';out.mkdir(parents=True,exist_ok=True);mapped=out/'ysyx_00000000.v';before=out/'before-resize.json';after=out/'mapped.json';stat=out/'stat.json';script=out/'resize.ys'
    plan={'_19037_':'NOR4_X2','_19060_':'NOR4_X2'}
    script.write_text('read_liberty -lib '+str(lib)+'\nread_verilog '+str(original)+'\nwrite_json '+str(before)+'\n'+''.join('chtype -set '+kind+' ysyx_00000000/'+name+'\n' for name,kind in plan.items())+'check -assert\ntee -o '+str(stat)+' stat -liberty '+str(lib)+' -json\nwrite_verilog -noattr -noexpr -simple-lhs '+str(mapped)+'\nwrite_json '+str(after)+'\n')
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');yosys=suite/'bin/yosys';sta=Path(json.loads((ROOT/'reports/C4_opensta_toolchain.json').read_text())['binary'])
    run('B5/netlist/resize',[yosys,'-s',script],inputs=[yosys,original,lib,script],outputs=[mapped,before,after,stat],timeout=180)
    a=json.loads(before.read_text())['modules']['ysyx_00000000'];b=json.loads(after.read_text())['modules']['ysyx_00000000'];assert a['ports']==b['ports'] and a['netnames']==b['netnames'] and a['cells'].keys()==b['cells'].keys()
    for name,cell in a['cells'].items():
        expected_cell=dict(cell)
        if name in plan:assert cell['type']=='NOR4_X1';expected_cell['type']=plan[name]
        assert b['cells'][name]==expected_cell,name
    sdc=out/'model.sdc';shutil.copyfile(base/'model.sdc',sdc)
    analysis=out/'analysis.tcl';text=(base/'analysis.tcl').read_text().replace(str(original),str(mapped)).replace(str(base/'model.sdc'),str(sdc));analysis.write_text(text)
    stdout,stderr,_=run('B5/netlist/sta',[sta,'-exit',analysis],inputs=[sta,lib,mapped,sdc,analysis],timeout=180)
    assert 'Error:' not in stdout+stderr and 'B_STA_DONE' in stdout
    setup=float(re.search(r'worst slack\s+(-?[\d.]+)',stdout)[1]);hold=float(re.search(r'(-?[\d.]+)\s+slack\s+\((?:MET|VIOLATED)\)',stdout.split('HOLD_BEGIN',1)[1])[1]);violations=stdout.split('TRANSITION_BEGIN',1)[1].count('(VIOLATED)')
    stats=json.loads(stat.read_text())['modules']['\\ysyx_00000000'];assert stats['area']<=25000 and violations==0 and hold>=0
    maximum=1000/(1-setup);frequency=350 if maximum>=350 else 325
    final_sdc=out/'evaluation.sdc';final_sdc.write_text(sdc.read_text().replace('-period 1 ',f'-period {1000/frequency:.12f} '));final_tcl=out/'evaluation.tcl';final_tcl.write_text(text.replace(str(sdc),str(final_sdc)))
    checked,err,_=run('B5/netlist/evaluation-sta',[sta,'-exit',final_tcl],inputs=[sta,lib,mapped,final_sdc,final_tcl],timeout=180);assert 'Error:' not in checked+err and float(re.search(r'worst slack\s+(-?[\d.]+)',checked)[1])>=0
    dump(ROOT/'reports/B5_final_timing.json',{'status':'PASS_AREA_AND_STATED_TIMING_MODEL','source':source_record,'netlist':str(mapped),'netlist_sha256':sha(mapped),'mapped_json_sha256':sha(after),'library_sha256':sha(lib),'resized_cells':plan,'connectivity_unchanged':True,'replacement_functions_identical':True,'area_um2':stats['area'],'cells':stats['num_cells'],'setup_frequency_estimate_mhz':maximum,'evaluation_frequency_mhz':frequency,'evaluation_period_ns':1000/frequency,'hold_slack_ns':hold,'max_transition_violations':violations,'max_capacitance_check':'NOT_RUN_TOOL_REPORT_UNAVAILABLE','scope':'Same fixed ideal-wire Nangate45 model and unchanged IO constraints. Two functionally identical drive-strength substitutions remove the observed transition violations. No placement, routing, extracted parasitics or physical-signoff claim.'});print('B5_FINAL_TIMING_PASS',stats['area'],maximum,frequency)
if __name__=='__main__':main()
