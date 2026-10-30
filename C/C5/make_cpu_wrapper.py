"""Generate the exact public CPU port contract and a one-outstanding AXI4 master."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    widths={'awready':1,'awvalid':1,'awaddr':32,'awid':4,'awlen':8,'awsize':3,'awburst':2,
            'wready':1,'wvalid':1,'wdata':32,'wstrb':4,'wlast':1,'bready':1,'bvalid':1,'bresp':2,'bid':4,
            'arready':1,'arvalid':1,'araddr':32,'arid':4,'arlen':8,'arsize':3,'arburst':2,
            'rready':1,'rvalid':1,'rresp':2,'rdata':32,'rlast':1,'rid':4}
    incoming={'awready','wready','bvalid','bresp','bid','arready','rvalid','rresp','rdata','rlast','rid'}
    ports=['input wire clock,reset,io_interrupt']
    for interface in ['master','slave']:
        for name,width in widths.items():
            is_input=(name in incoming)==(interface=='master')
            ports.append(('input wire ' if is_input else 'output logic ')+(f'[{width-1}:0] ' if width>1 else '')+'io_'+interface+'_'+name)
    header="`ifndef C5_RESET_PC\n`define C5_RESET_PC 32'h20000000\n`endif\n`ifndef C5_FAULT_ADDI\n`define C5_FAULT_ADDI 0\n`endif\n`ifndef C5_CORE_DELAYS\n`define C5_CORE_DELAYS 0\n`endif\nmodule ysyx_00000000(\n"+',\n'.join(ports)+'\n);\n'
    unused='  wire unused_inputs=^{io_interrupt,'+','.join('io_slave_'+n for n in widths if n not in incoming)+'};\n'
    ties='\n'.join('  assign io_slave_'+n+"='0;" for n in widths if n in incoming)+'\n'
    body=r'''
  wire i_req_valid,i_req_ready,i_resp_valid,i_resp_ready;
  wire [31:0] i_req_addr,i_resp_data;wire [1:0] i_resp_error;
  wire d_req_valid,d_req_ready,d_req_write,d_resp_valid,d_resp_ready;
  wire [31:0] d_req_addr,d_req_wdata,d_resp_data;wire [3:0] d_req_wstrb;
  wire [2:0] d_req_size;wire [1:0] d_resp_error;
  wire [31:0] pc;wire halted;wire [2:0] fault,debug_state;
  wire commit_valid;wire [31:0] commit_pc,commit_inst,commit_next_pc;wire [511:0] debug_gpr;
  wire exec_fire,exec_ebreak,exec_mem_valid,exec_mem_write;
  wire [31:0] exec_pc,exec_inst,exec_mem_addr,exec_mem_wdata,exec_mem_rdata;wire [2:0] exec_mem_size;
  wire [2:0] delay_enable=`C5_CORE_DELAYS;wire [31:0] lfsr_seed=32'h2607c501;
  ysyx_00000000_core #(.STAGE(4),.RESET_PC(`C5_RESET_PC),.FAULT_ADDI(`C5_FAULT_ADDI)) core(.*);
  localparam logic [2:0] IDLE=0,READ_ADDRESS=1,READ_RESPONSE=2,WRITE_CHANNELS=3,WRITE_RESPONSE=4,LOCAL_RESPONSE=5;
  logic [2:0] state;
  logic owner_data,turn,aw_done,w_done;
  logic [31:0] address,data,local_data;
  logic [3:0] strobe;
  logic [2:0] size;
  logic [1:0] local_error;
  logic [63:0] mtime;
  logic [31:0] latched_high;
  logic high_valid;
  wire choose_data=d_req_valid&&(!i_req_valid||turn);
  wire request=(i_req_valid||d_req_valid)&&state==IDLE&&!reset;
  wire [31:0] chosen_address=choose_data?d_req_addr:i_req_addr;
  wire [2:0] chosen_size=choose_data?d_req_size:3'd2;
  wire chosen_write=choose_data&&d_req_write;
  wire internal_clint=chosen_address[31:16]==16'h0200;
  wire executable=(chosen_address>=32'h0f000000&&chosen_address<32'h0f002000)||
                  (chosen_address>=32'h20000000&&chosen_address<32'h20001000)||
                  chosen_address[31:28]==4'h3||chosen_address[31:29]==3'b100||
                  chosen_address[31:29]==3'b101||chosen_address[31:30]==2'b11;
  wire response_ready=owner_data?d_resp_ready:i_resp_ready;
  logic response_valid;logic [31:0] response_data;logic [1:0] response_error;
  assign i_req_ready=!reset&&state==IDLE&&!choose_data;
  assign d_req_ready=!reset&&state==IDLE&&choose_data;
  assign i_resp_valid=!owner_data&&response_valid;
  assign d_resp_valid=owner_data&&response_valid;
  assign i_resp_data=response_data;assign d_resp_data=response_data;
  assign i_resp_error=response_error;assign d_resp_error=response_error;
  always_comb begin
    io_master_awvalid=0;io_master_awaddr=address;io_master_awid=0;io_master_awlen=0;io_master_awsize=size;io_master_awburst=1;
    io_master_wvalid=0;io_master_wdata=data;io_master_wstrb=strobe;io_master_wlast=0;io_master_bready=0;
    io_master_arvalid=0;io_master_araddr=address;io_master_arid=0;io_master_arlen=0;io_master_arsize=size;io_master_arburst=1;
    io_master_rready=0;response_valid=0;response_data=0;response_error=0;
    if(!reset)case(state)
      READ_ADDRESS:io_master_arvalid=1;
      READ_RESPONSE:begin
        response_valid=io_master_rvalid;response_data=io_master_rdata;
        response_error=(io_master_rid!=0||!io_master_rlast)?2'b10:io_master_rresp;
        io_master_rready=response_ready;
      end
      WRITE_CHANNELS:begin io_master_awvalid=!aw_done;io_master_wvalid=!w_done;io_master_wlast=!w_done;end
      WRITE_RESPONSE:begin
        response_valid=io_master_bvalid;response_error=io_master_bid!=0?2'b10:io_master_bresp;io_master_bready=response_ready;
      end
      LOCAL_RESPONSE:begin response_valid=1;response_data=local_data;response_error=local_error;end
      default:begin end
    endcase
  end
  always_ff @(posedge clock)begin
    if(reset)begin
      state<=IDLE;owner_data<=0;turn<=0;aw_done<=0;w_done<=0;address<=0;data<=0;strobe<=0;size<=0;
      local_data<=0;local_error<=0;mtime<=0;latched_high<=0;high_valid<=0;
    end else begin
      mtime<=mtime+1;
      case(state)
        IDLE:if(request)begin
          owner_data<=choose_data;address<=chosen_address;data<=d_req_wdata;strobe<=d_req_wstrb;size<=chosen_size;
          aw_done<=0;w_done<=0;local_data<=0;local_error<=0;
          if((!choose_data&&!executable)||internal_clint)begin
            state<=LOCAL_RESPONSE;
            if(!choose_data) local_error<=2'b11;
            else if(chosen_write||chosen_size!=2) local_error<=2'b10;
            else if(chosen_address[15:0]==0)begin local_data<=mtime[31:0];latched_high<=mtime[63:32];high_valid<=1;end
            else if(chosen_address[15:0]==4)begin local_data<=high_valid?latched_high:mtime[63:32];high_valid<=0;end
            else local_error<=2'b10;
          end else state<=chosen_write?WRITE_CHANNELS:READ_ADDRESS;
        end
        READ_ADDRESS:if(io_master_arvalid&&io_master_arready)state<=READ_RESPONSE;
        READ_RESPONSE:if(response_valid&&response_ready)begin state<=IDLE;turn<=!owner_data;end
        WRITE_CHANNELS:begin
          if(io_master_awvalid&&io_master_awready)aw_done<=1;
          if(io_master_wvalid&&io_master_wready)w_done<=1;
          if((aw_done||(io_master_awvalid&&io_master_awready))&&(w_done||(io_master_wvalid&&io_master_wready)))state<=WRITE_RESPONSE;
        end
        WRITE_RESPONSE:if(response_valid&&response_ready)begin state<=IDLE;turn<=!owner_data;end
        LOCAL_RESPONSE:if(response_ready)begin state<=IDLE;turn<=!owner_data;end
        default:state<=IDLE;
      endcase
    end
  end
`ifndef SYNTHESIS
  import "DPI-C" function void c5_retire(input int unsigned at_pc,input int unsigned inst,input int unsigned next_pc,input bit [511:0] registers);
  import "DPI-C" function void c5_fault(input int unsigned at_pc,input int unsigned code);
  import "DPI-C" function void c5_memory(input int unsigned at_pc,input int unsigned addr,input int unsigned bytes,input int unsigned value,input bit write_op);
  import "DPI-C" function void c5_bus(input int unsigned channel,input int unsigned addr,input int unsigned value,input int unsigned attr);
  always @(negedge clock)if(!reset)begin
    if(commit_valid)c5_retire(commit_pc,commit_inst,commit_next_pc,debug_gpr);
    if(fault!=0)c5_fault(pc,{29'b0,fault});
  end
  always @(posedge clock)if(!reset)begin
    if(exec_fire&&exec_mem_valid)c5_memory(exec_pc,exec_mem_addr,{29'b0,exec_mem_size},exec_mem_write?exec_mem_wdata:exec_mem_rdata,exec_mem_write);
    if(io_master_arvalid&&io_master_arready)c5_bus(0,io_master_araddr,0,{13'b0,io_master_arid,io_master_arlen,io_master_arsize,io_master_arburst,2'b0});
    if(io_master_rvalid&&io_master_rready)c5_bus(1,0,io_master_rdata,{25'b0,io_master_rid,io_master_rlast,io_master_rresp});
    if(io_master_awvalid&&io_master_awready)c5_bus(2,io_master_awaddr,0,{13'b0,io_master_awid,io_master_awlen,io_master_awsize,io_master_awburst,2'b0});
    if(io_master_wvalid&&io_master_wready)c5_bus(3,0,io_master_wdata,{27'b0,io_master_wlast,io_master_wstrb});
    if(io_master_bvalid&&io_master_bready)c5_bus(4,0,0,{26'b0,io_master_bid,io_master_bresp});
  end
`endif
endmodule
'''
    out=ROOT/'rtl/ysyx_00000000.v';text=header+unused+ties+body
    if not out.exists() or out.read_text()!=text:out.write_text(text)
    print('C5_CPU_WRAPPER_GENERATED',out,flush=True)

if __name__=='__main__':main()
