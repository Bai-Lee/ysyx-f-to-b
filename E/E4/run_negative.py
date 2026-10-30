from common import *
def main():
    rtl=ROOT/'E/E4/rtl';cpp=ROOT/'E/E4/csrc';folder=ROOT/'E/E4/faults';folder.mkdir(exist_ok=True)
    source=(rtl/'comb.sv').read_text()
    old="!en?3'd0:x[7]?3'd7:x[6]?3'd6:x[5]?3'd5:x[4]?3'd4:x[3]?3'd3:x[2]?3'd2:x[1]?3'd1:3'd0"
    new="!en?3'd0:x[0]?3'd0:x[1]?3'd1:x[2]?3'd2:x[3]?3'd3:x[4]?3'd4:x[5]?3'd5:x[6]?3'd6:x[7]?3'd7:3'd0"
    assert source.count(old)==1;(folder/'low_priority.sv').write_text(source.replace(old,new))
    source=(rtl/'keyboard.sv').read_text();old='data_sync[2] && (^bits[9:1])';new="data_sync[2] && ((^bits[9:1]) || bits[8:1]==8'h1c)"
    assert source.count(old)==1;(folder/'parity_bypass.sv').write_text(source.replace(old,new))
    cases=[('priority','comb',folder/'low_priority.sv',[]),('overflow','comb',rtl/'comb.sv',['FAULT_OVERFLOW']),('lfsr','sequential',rtl/'sequential.sv',['FAULT_LFSR']),('parity','keyboard',folder/'parity_bypass.sv',[]),('vga_total','vga',rtl/'vga.sv',['FAULT_VGA_TOTAL'])]
    results=[]
    for name,top,src,defines in cases:
        exe=build(top,[src],cpp/(top+'_test.cpp'),'fault_'+name,defines=defines,trace=False,flags=['-Wno-DECLFILENAME'])
        o,e,r=run('negative/'+name,[exe],inputs=[exe],expected=(1,),timeout=60);assert 'FAIL ' in e
        results.append({'name':name,'reason':e.strip(),'run':r})
    bad=folder/'lint_bad.sv';bad.write_text('module lint_bad(input wire [7:0] a,input wire en,output reg [3:0] q);always @* if(en)q=a;endmodule\n')
    o,e,r=run('lint/negative',[VERILATOR,'--lint-only','-Wall',bad],inputs=[bad],expected=(1,));assert 'LATCH' in e and 'WIDTHTRUNC' in e
    for top,files in [('comb',['comb.sv']),('sequential',['sequential.sv']),('keyboard',['keyboard.sv']),('vga',['vga.sv']),('cpu_top',['scpu.sv','cpu_top.sv']),('lab_board',['comb.sv','sequential.sv','keyboard.sv','vga.sv','scpu.sv','cpu_top.sv','program_rom.sv','lab_board.sv'])]:
        sources=[rtl/n for n in files]
        o,e,r=run('lint/'+top,[VERILATOR,'--lint-only','-Wall','-Wno-DECLFILENAME','--timescale','1ns/1ns','--top-module',top,*sources],inputs=sources);assert not e.strip(),e
    dump(ROOT/'reports/E4_negative.json',{'status':'PASS','mutants':results,'style_waiver':'DECLFILENAME only: deliberately grouped reusable modules. No logical warning class suppressed.','known_runtime_controls':['XOR->OR','R0 write disabled','unsigned negative branch offset'],'lint_negative':'deliberate truncation and inferred latch rejected'})
    result(['E4-M010'],['reports/E4_negative.json','artifacts/E4/lint'],'All six production top modules lint clean with only documented multi-module filename style waiver; deliberate latch/width mistakes rejected; five additional compiled RTL mutants rejected at runtime.')
    print('MUTATION_AND_LINT_PASS',flush=True)
if __name__=='__main__':main()
