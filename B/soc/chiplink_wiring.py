"""Passive pin/remote-RAM observations and an isolated read-bit fault variant."""
import re


def replace_module(text,name,transform):
    matches=list(re.finditer(r'(?ms)^module '+re.escape(name)+r'\(.*?^endmodule\b',text));assert len(matches)==1,(name,len(matches))
    match=matches[0];return text[:match.start()]+transform(match[0])+text[match.end():]


def instrument(text,corrupt=False):
    def top(module):
        for signal in ['_asic_fpga_io_c2b_clk','_asic_fpga_io_c2b_rst','_asic_fpga_io_c2b_send','_asic_fpga_io_c2b_data','_fpga_fpga_io_c2b_clk','_fpga_fpga_io_c2b_rst','_fpga_fpga_io_c2b_send','_fpga_fpga_io_c2b_data']:assert signal in module
        observer='''
  import "DPI-C" function void c5_chiplink_word(input int unsigned direction,input int unsigned word);
  always @(posedge _asic_fpga_io_c2b_clk)
    if(!_asic_fpga_io_c2b_rst && _asic_fpga_io_c2b_send)c5_chiplink_word(0,_asic_fpga_io_c2b_data);
  always @(posedge _fpga_fpga_io_c2b_clk)
    if(!_fpga_fpga_io_c2b_rst && _fpga_fpga_io_c2b_send)c5_chiplink_word(1,_fpga_fpga_io_c2b_data);
'''
        return module.removesuffix('endmodule')+observer+'endmodule'
    def memory(module):
        assert 'reg [31:0] Memory[0:268435455]' in module
        if corrupt:
            original="assign R0_data = _R0_en_d0 ? Memory[_R0_addr_d0] : 32'bx;"
            assert module.count(original)==1
            module=module.replace(original,"assign R0_data = _R0_en_d0 ? (Memory[_R0_addr_d0] ^ 32'h00000001) : 32'bx;")
        observer='''
  import "DPI-C" function void c5_remote_memory(input int unsigned kind,input int unsigned address,input int unsigned data,input int unsigned mask);
  always @(posedge R0_clk)if(R0_en)c5_remote_memory(0,32'hc0000000+{R0_addr,2'b0},0,15);
  always @(posedge W0_clk)if(W0_en)c5_remote_memory(1,32'hc0000000+{W0_addr,2'b0},W0_data,32'(W0_mask));
'''
        return module.removesuffix('endmodule')+observer+'endmodule'
    return replace_module(replace_module(text,'ysyxSoCFull',top),'mem_268435456x32',memory)
