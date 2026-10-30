"""Generate a four-state testbench at the public32-bit AXI boundary."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    widths={'awready':1,'awvalid':1,'awaddr':32,'awid':4,'awlen':8,'awsize':3,'awburst':2,'wready':1,'wvalid':1,'wdata':32,'wstrb':4,'wlast':1,'bready':1,'bvalid':1,'bresp':2,'bid':4,'arready':1,'arvalid':1,'araddr':32,'arid':4,'arlen':8,'arsize':3,'arburst':2,'rready':1,'rvalid':1,'rresp':2,'rdata':32,'rlast':1,'rid':4}
    incoming={'awready','wready','bvalid','bresp','bid','arready','rvalid','rresp','rdata','rlast','rid'}
    lines=['`timescale 1ns/1ps','module cpu_four_state_tb;','reg clock=0; always #5 clock=~clock;','reg reset=1;']
    for name,width in widths.items():lines.append(('wire ' if name not in incoming or name in ('arready','awready','wready') else 'reg ')+(f'[{width-1}:0] ' if width>1 else '')+'m_'+name+';')
    connections=['.clock(clock)','.reset(reset)',".io_interrupt(1'b0)"]
    connections += [f'.io_master_{name}(m_{name})' for name in widths]
    connections += [f'.io_slave_{name}('+('' if name in incoming else f"{width}'b0")+')' for name,width in widths.items()]
    lines+=['ysyx_00000000 dut('+','.join(connections)+');']
    body=(ROOT/'B/B5/tb_body.svh').read_text();out=ROOT/'B/B5/cpu_four_state_tb.sv';out.write_text('\n'.join(lines)+'\n'+body+'\nendmodule\n')
    print('B5_FOUR_STATE_TB_GENERATED')
if __name__=='__main__':main()
