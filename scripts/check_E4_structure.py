from evidence import *
import re
def clocked(c):
    p=c.get('parameters',{})
    return 'CLK_POLARITY' in p and not (c['type'].startswith('$memrd') and int(p.get('CLK_ENABLE','1'),2)==0)
def main():
    exe=ROOT.parents[1]/'tools/oss-cad-suite-20261022/oss-cad-suite/bin/yosys.exe'
    rtl=ROOT/'E/E4/rtl';folder=ROOT/'artifacts/E4/structure';folder.mkdir(parents=True,exist_ok=True)
    video=folder/'vga_control_only.sv';video.write_text((rtl/'vga.sv').read_text('utf8').split('module vga(input')[0],encoding='utf8')
    rows=[]
    for top,sources in [('comb',[rtl/'comb.sv']),('sequential',[rtl/'sequential.sv']),('keyboard',[rtl/'keyboard.sv']),('cpu_top',[rtl/'scpu.sv',rtl/'cpu_top.sv']),('vga_timing',[video]),('motion',[video])]:
        target=folder/(top+'.json');script=folder/(top+'.ys')
        script.write_text('read_verilog -sv '+ ' '.join('"'+p.as_posix()+'"' for p in sources)+f'\nhierarchy -check -top {top}\nproc\nopt\ncheck -assert\nselect -assert-none t:$dlatch t:$adlatch\nwrite_json "'+target.as_posix()+'"\nstat\n',encoding='utf8')
        r=run('E4/structure/'+top,[exe,'-Q','-T','-s',script],[*sources,script],timeout=120);assert r['status']=='PASS'
        net=json.loads(target.read_text('utf8'));cells=[c for m in net['modules'].values() for c in m.get('cells',{}).values()]
        for c in cells:
            assert 'latch' not in c['type'].lower()
            if clocked(c):assert int(c['parameters']['CLK_POLARITY'],2)==1
        rows.append({'top':top,'cells_in_retained_modules':len(cells),'clocked_cells':sum(clocked(c) for c in cells),'asynchronous_memory_read_ports':sum(c['type'].startswith('$memrd') and not clocked(c) for c in cells),'json_sha256':sha(target),'run':r})
    bad=ROOT/'E/E4/faults/lint_bad.sv';script=folder/'negative.ys'
    script.write_text(f'read_verilog -sv "{bad.as_posix()}"\nhierarchy -top lint_bad\nproc\nselect -assert-none t:$dlatch\n',encoding='utf8')
    r=run('E4/structure/negative',[exe,'-Q','-T','-s',script],[bad,script],expected=1);assert r['status']=='PASS'
    assert 'Assertion failed' in (ROOT/'artifacts/E4/structure/negative/stderr.log').read_text('utf8')
    negclock=folder/'negedge.sv';negclock.write_text('module negedge_dut(input clk,d,output reg q);always @(negedge clk)q<=d;endmodule\n',encoding='utf8')
    target=folder/'negedge.json'
    n=run('E4/structure/negative_clock',[exe,'-Q','-T','-p',f'read_verilog "{negclock.as_posix()}"; proc; write_json "{target.as_posix()}"'],[negclock]);assert n['status']=='PASS'
    badcells=[c for m in json.loads(target.read_text('utf8'))['modules'].values() for c in m['cells'].values()]
    assert any(clocked(c) and int(c['parameters']['CLK_POLARITY'],2)==0 for c in badcells)
    dump(ROOT/'reports/E4_structure.json',{'status':'PASS','tool':str(exe),'tool_sha256':sha(exe),'results':rows,'negative':r,'negative_clock_rejected':True,'scope':'Process/netlist structural checks only: no inferred latches, only positive-edge clocked cells. $memrd CLK_ENABLE=0 is asynchronous and its unused CLK_POLARITY is not interpreted as a falling-edge flop. Full display image RAM excluded; no physical PPA or unbounded functional proof.'})
    print('E4_STRUCTURE_PASS',len(rows),flush=True)
if __name__=='__main__':main()
