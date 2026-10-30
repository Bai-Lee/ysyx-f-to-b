"""Simulation-only flat-port wrapper; synthesizable cores remain separate."""
from pathlib import Path
import importlib.util
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('wiring',D/'rtl_tests/generate_interconnect.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SB=[('i_req_valid',1,1),('i_req_addr',32,1),('i_req_ready',1,0),('i_resp_valid',1,0),('i_resp_data',32,0),('i_resp_error',2,0),('i_resp_ready',1,1),('d_req_valid',1,1),('d_req_addr',32,1),('d_req_write',1,1),('d_req_wdata',32,1),('d_req_wstrb',4,1),('d_req_ready',1,0),('d_resp_valid',1,0),('d_resp_data',32,0),('d_resp_error',2,0),('d_resp_ready',1,1)]
ports=['input wire clock,reset','input wire [63:0] sim_cycle','input wire [2:0] delay_enable','input wire [31:0] lfsr_seed']
ports += [f'output wire {m.width(w)}{n}' for n,w in m.OBS]
ports += [f'{"output" if o else "input"} wire {m.width(w)}{n}' for n,w,o in SB]
ports += m.ports('mem_','master')+m.ports('mon_','monitor')
ports += ['output wire uart_tx_valid','output wire [7:0] uart_tx_data','output wire [63:0] mtime','output wire debug_arb_busy,debug_arb_owner']
text='module c4_sim #(parameter integer MODE=4,parameter bit FAULT_ADDI=0,parameter logic[63:0] MTIME_RESET=0)(\n '+',\n '.join(ports)+'\n);\n'
common=['.clock(clock)','.reset(reset)','.delay_enable(delay_enable)','.lfsr_seed(lfsr_seed)']+[f'.{n}({n})' for n,w in m.OBS]
text+='generate if(MODE<=4)begin: simple\n c4_simple_core #(.STAGE(MODE),.FAULT_ADDI(FAULT_ADDI)) core(\n'+',\n'.join(common+[f'.{n}({n})' for n,w,o in SB])+');\n'
for n,w,o in m.FIELDS:
    if o:text+=f' assign mem_{n}={w}\'d0;\n'
    text+=f' assign mon_{n}={w}\'d0;\n'
text+=" assign uart_tx_valid=0;assign uart_tx_data=0;assign mtime=0;assign debug_arb_busy=0;assign debug_arb_owner=0;\nend else begin: axi\n"
for n,w,o in SB:
    if o:text+=f' assign {n}={w}\'d0;\n'
text+=' if(MODE==5)begin: external_devices\n c4_axi_core #(.FAULT_ADDI(FAULT_ADDI)) core(\n'+',\n'.join(common+[f'.m_{n}(mem_{n})' for n,w,o in m.FIELDS]+['.debug_arb_busy(debug_arb_busy)','.debug_arb_owner(debug_arb_owner)'])+');\n'
for n,w,o in m.FIELDS:text+=f' assign mon_{n}=mem_{n};\n'
text+=' assign uart_tx_valid=0;assign uart_tx_data=0;assign mtime=0;\n end else begin: rtl_devices\n c4_axi_soc #(.FAULT_ADDI(FAULT_ADDI),.MTIME_RESET(MTIME_RESET)) core(\n'
text+=',\n'.join(common+[f'.{p}{n}({p}{n})' for p in ['mem_','mon_'] for n,w,o in m.FIELDS]+['.uart_tx_valid(uart_tx_valid)','.uart_tx_data(uart_tx_data)','.mtime(mtime)','.debug_arb_busy(debug_arb_busy)','.debug_arb_owner(debug_arb_owner)'])+');\n end\nend endgenerate\n'
text+='''import "DPI-C" function void npc_commit(input int unsigned pc,input int unsigned instruction);
import "DPI-C" function void npc_finish(input int unsigned pc,input int unsigned code);
import "DPI-C" function void c4_data_commit(input int unsigned address,input int unsigned size,input int unsigned value,input bit is_write);
always @(posedge clock) if(!reset && exec_fire) begin
  npc_commit(exec_pc,exec_inst);
  if(exec_mem_valid)c4_data_commit(exec_mem_addr,{29'b0,exec_mem_size},exec_mem_write?exec_mem_wdata:exec_mem_rdata,exec_mem_write);
  if(exec_ebreak)npc_finish(exec_pc,debug_gpr[351:320]);
end
wire unused_cycle = ^sim_cycle;
endmodule
'''
out=D/'sim';out.mkdir(exist_ok=True);(out/'c4_sim.sv').write_text(text,encoding='utf8',newline='\n')
print('C4_SIM_TOP_READY')
