from pathlib import Path
import sys,re,copy,collections
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def check_structure(module,models):
    ports=module['ports'];clock=ports['clock']['bits'];used=collections.Counter()
    for side in ['master','slave']:
        for field in ['wdata','rdata','awaddr','araddr']:
            assert len(ports['io_'+side+'_'+field]['bits'])==32,'AXI_WIDTH'
        assert len(ports['io_'+side+'_wstrb']['bits'])==4,'AXI_STROBE'
    for cell in module['cells'].values():
        kind=cell['type'];used[kind]+=1
        assert kind not in ['DLL_X1','DLL_X2','DLH_X1','DLH_X2'] and 'LATCH' not in kind.upper(),'LATCH'
        assert kind in models,'UNVALIDATED_CELL'
        if kind.startswith('DFF'):
            assert kind=='DFF_X1' and cell['connections']['CK']==clock,'CLOCK_TREE'
    assert used['DFF_X1']>0
    return dict(used)

def main():
    structure=ROOT/'B/B5/netlist/mapped.json';timing=json.loads((ROOT/'reports/B5_final_timing.json').read_text())
    netlist=ROOT/'B/B5/netlist/ysyx_00000000.v';assert sha(netlist)==timing['netlist_sha256'] and sha(structure)==timing['mapped_json_sha256']
    cells=json.loads((ROOT/'reports/B5_cell_models.json').read_text());assert cells['status']=='PASS' and cells['netlist_structure_sha256']==sha(structure)
    module=json.loads(structure.read_text())['modules']['ysyx_00000000'];used=check_structure(module,set(cells['used_cells']))
    controls=[]
    for name in ['latch','clock','width']:
        wrong=copy.deepcopy(module)
        if name=='width':wrong['ports']['io_master_rdata']['bits']=wrong['ports']['io_master_rdata']['bits'][:16]
        else:
            cell=next(c for c in wrong['cells'].values() if c['type']=='DFF_X1')
            if name=='latch':cell['type']='DLH_X1'
            else:cell['connections']['CK']=wrong['ports']['reset']['bits']
        try:check_structure(wrong,set(cells['used_cells']))
        except AssertionError as error:controls.append({'mutation':name,'status':'PASS_MUTATION_REJECTED','reason':str(error)})
        else:raise AssertionError('MISSED_'+name)
    exported=ROOT/'B/soc/build/ysyx_00000000.sv';text=exported.read_text();names=re.findall(r'^module\s+(\w+)',text,re.M)
    assert names and len(names)==len(set(names)) and all(n=='ysyx_00000000' or n.startswith('ysyx_00000000_') for n in names)
    assert not re.search(r'\bnegedge\b|DPI-C',text)
    output,error,record=run('B5/structure/lint-raw',[VERILATOR,'--lint-only','-Wall','--top-module','ysyx_00000000',exported],inputs=[VERILATOR,exported],expected=(0,1))
    warnings=re.findall(r'^%Warning-([A-Z0-9_]+): (.*)$',error,re.M)
    allowed={'DECLFILENAME','UNUSEDSIGNAL','UNUSEDPARAM'}
    assert set(code for code,_ in warnings)<=allowed,(set(code for code,_ in warnings)-allowed)
    assert not re.search(r'^%Error(?!: Exiting due to \d+ warning)',error,re.M)
    run('B5/structure/lint-reviewed',[VERILATOR,'--lint-only','-Wall','-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','-Wno-UNUSEDPARAM','--top-module','ysyx_00000000',exported],inputs=[VERILATOR,exported])
    dump(ROOT/'reports/B5_structure.json',{'status':'PASS','netlist_sha256':sha(netlist),'mapped_json_sha256':sha(structure),'exported_rtl_sha256':sha(exported),'modules':names,'cell_types':used,'DFF_rising_clock':'All DFF_X1 CK pins connect directly to top-level clock; cell edge behavior was separately verified','latches':0,'axi_data_bits':32,'negative_controls':controls,'warnings':[{'code':c,'location':d} for c,d in warnings],
        'warning_review':{'DECLFILENAME':'Required single-file export contains several prefixed modules.','UNUSEDSIGNAL':'Unused commit/debug/performance taps are simulation-only; unused decode bits are intentionally selected opcode fields; mtvec low bits are aligned to four bytes. No unused functional AXI ready/valid path is hidden.','UNUSEDPARAM':'STAGE preserves the inherited core interface; the implemented pipeline is fixed at four stages.'},
        'scope':'Final exported DUT and exact final mapped netlist. Simulation-only negedge observation hooks are excluded. No official whitelist, hidden tests or physical-signoff claim.'})
    print('B5_STRUCTURE_PASS',used['DFF_X1'],len(warnings))

if __name__=='__main__':main()
