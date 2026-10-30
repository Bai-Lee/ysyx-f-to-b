from common import *
def main():
    src=ROOT/'E/E4';tb=src/'csrc/rom_tb.sv'
    tb.write_text('''module tb;
reg[7:0] address;wire[7:0] instruction;reg[7:0] expected[0:255];integer i;
program_rom d(address,instruction);
initial begin
$readmemh("'''+str(src/'data/f6_output.hex')+'''",expected);
for(i=0;i<256;i=i+1)begin address=i;#1;if(instruction!==expected[i])$fatal(1,"ROM byte %d",i);end
$display("PASS RTL ROM256 bytes match frozen program");$finish;
end endmodule
''')
    exe=OUT/'rom.vvp';files=[src/'rtl/scpu.sv',src/'rtl/program_rom.sv',tb]
    run('rom/compile',['iverilog','-g2012','-s','tb','-o',exe,*files],inputs=files)
    o,e,r=run('rom/all_addresses',['vvp',exe],inputs=[exe,src/'data/f6_output.hex']);assert 'PASS RTL ROM256' in o
    script=src/'env.sh'
    o,e,r=run('framework/process_environment',['bash','-c','source "$1"; test "$NPC_HOME" = /home/USER/ysyx-workbench/npc; test "$NVBOARD_HOME" = /home/USER/ysyx-workbench/nvboard; printf "%s\\n" "$NPC_HOME" "$NVBOARD_HOME" "$VERILATOR_ROOT"; command -v verilator','bash',script],inputs=[script])
    o,e,r=run('export/nvboard_clean',['git','status','--porcelain'],cwd=NVBOARD);assert not o.strip()
    print('ROM_AND_ENVIRONMENT_PASS',flush=True)
if __name__=='__main__':main()
