"""Generate repetitive flat-port wiring; protocol state machines remain explicit."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'rtl'
FIELDS=[('awvalid',1,1),('awready',1,0),('awaddr',32,1),('awprot',3,1),
 ('wvalid',1,1),('wready',1,0),('wdata',32,1),('wstrb',4,1),
 ('bvalid',1,0),('bready',1,1),('bresp',2,0),
 ('arvalid',1,1),('arready',1,0),('araddr',32,1),('arprot',3,1),
 ('rvalid',1,0),('rready',1,1),('rdata',32,0),('rresp',2,0)]
OBS=[('pc',32),('halted',1),('fault',3),('commit_valid',1),('commit_pc',32),('commit_inst',32),('commit_next_pc',32),('debug_gpr',512),
 ('exec_fire',1),('exec_pc',32),('exec_inst',32),('exec_ebreak',1),('exec_mem_valid',1),('exec_mem_write',1),('exec_mem_addr',32),('exec_mem_size',3),('exec_mem_wdata',32),('exec_mem_rdata',32),('debug_state',3)]
def width(n):return '' if n==1 else f'[{n-1}:0] '
def ports(prefix,role,mult=1):
 return [f'{"output" if role=="monitor" or (bool(out)==(role=="master")) else "input"} logic {width(n*mult)}{prefix}{name}' for name,n,out in FIELDS]
def wires(prefix,mult=1):return '\n'.join(f'  wire {width(n*mult)}{prefix}{name};' for name,n,_ in FIELDS)
def links(port,net):return ',\n    '.join(f'.{port}{name}({net}{name})' for name,_,_ in FIELDS)
def save(name,text):ROOT.mkdir(exist_ok=True);(ROOT/name).write_text(text,encoding='utf8',newline='\n')

def arbiter():
 header='module axil_arbiter2(\n  '+',\n  '.join(['input logic clock,reset',*ports('s0_','slave'),*ports('s1_','slave'),*ports('m_','master'),'output wire debug_busy,debug_owner'])+'\n);\n'
 body='''  logic active,owner,write_mode,turn;
  wire want0=s0_arvalid||s0_awvalid||s0_wvalid;
  wire want1=s1_arvalid||s1_awvalid||s1_wvalid;
  wire choice=want0&&want1?turn:want1;
  assign debug_busy=!reset&&active;
  assign debug_owner=owner;
  always_comb begin
'''
 for name,_,out in FIELDS:
  if out:body+=f'    m_{name}=0;\n'
  else:body+=f'    s0_{name}=0;s1_{name}=0;\n'
 body+='    if(!reset&&active)begin\n      if(write_mode)begin\n'
 for wr in [True,False]:
  if not wr:body+='      end else begin\n'
  for owner in [0,1]:
   body+=f'        {"if(!owner)" if owner==0 else "else"} begin\n'
   for name,_,out in FIELDS:
    if name.startswith(('aw','w','b'))!=wr:continue
    body+=f'          m_{name}=s{owner}_{name};\n' if out else f'          s{owner}_{name}=m_{name};\n'
   body+='        end\n'
 body+='''      end
    end
  end
  always_ff @(posedge clock)begin
    if(reset)begin active<=0;owner<=0;write_mode<=0;turn<=0;end
    else if(!active)begin
      if(want0||want1)begin active<=1;owner<=choice;write_mode<=choice?!s1_arvalid:!s0_arvalid;end
    end else if((write_mode&&m_bvalid&&m_bready)||(!write_mode&&m_rvalid&&m_rready))begin
      active<=0;turn<=!owner;
    end
  end
endmodule
'''
 save('axil_arbiter2.sv',header+body)

def xbar():
 header='''module axil_xbar3 #(
  parameter logic [31:0] RAM_BASE=32'h80000000,
  parameter logic [31:0] RAM_BYTES=32'h08000000
)(
  '''+',\n  '.join(['input logic clock,reset',*ports('s_','slave'),*ports('m_','master',3)])+'\n);\n'
 body='''  localparam logic [2:0] IDLE=0,R_SEND=1,R_RESP=2,W_SEND=3,W_RESP=4,R_ERROR=5,W_ERROR=6;
  logic [2:0] state;logic [1:0] target;
  logic aw_have,w_have,aw_done,w_done;
  logic [31:0] address,data;logic [2:0] protection;logic [3:0] strobe;
  wire aw_fire=s_awvalid&&s_awready;
  wire w_fire=s_wvalid&&s_wready;
  wire [31:0] effective_addr=aw_have?address:s_awaddr;
  function automatic [1:0] decode(input logic [31:0] a);
    if({1'b0,a}>={1'b0,RAM_BASE} && {1'b0,a}<{1'b0,RAM_BASE}+{1'b0,RAM_BYTES})decode=0;
    else if(a[31:12]==20'h10000)decode=1;
    else if(a[31:12]==20'h20000)decode=2;
    else decode=3;
  endfunction
  always_comb begin
'''
 for name,_,out in FIELDS:
  body+=f'    {"m_" if out else "s_"}{name}=0;\n'
 body+='''    if(!reset)case(state)
      IDLE:begin
        s_awready=!aw_have;s_wready=!w_have;
        s_arready=!aw_have&&!w_have&&!s_awvalid&&!s_wvalid;
      end
      R_SEND:begin
        m_arvalid[target]=1;m_araddr[target*32+:32]=address;m_arprot[target*3+:3]=protection;
      end
      R_RESP:begin
        s_rvalid=m_rvalid[target];s_rdata=m_rdata[target*32+:32];s_rresp=m_rresp[target*2+:2];m_rready[target]=s_rready;
      end
      W_SEND:begin
        m_awvalid[target]=!aw_done;m_awaddr[target*32+:32]=address;m_awprot[target*3+:3]=protection;
        m_wvalid[target]=!w_done;m_wdata[target*32+:32]=data;m_wstrb[target*4+:4]=strobe;
      end
      W_RESP:begin s_bvalid=m_bvalid[target];s_bresp=m_bresp[target*2+:2];m_bready[target]=s_bready;end
      R_ERROR:begin s_rvalid=1;s_rresp=2'b11;end
      W_ERROR:begin s_bvalid=1;s_bresp=2'b11;end
      default:begin end
    endcase
  end
  always_ff @(posedge clock)begin
    if(reset)begin state<=IDLE;target<=0;aw_have<=0;w_have<=0;aw_done<=0;w_done<=0;address<=0;data<=0;protection<=0;strobe<=0;end
    else case(state)
      IDLE:begin
        if(aw_fire)begin address<=s_awaddr;protection<=s_awprot;aw_have<=1;end
        if(w_fire)begin data<=s_wdata;strobe<=s_wstrb;w_have<=1;end
        if((aw_have||aw_fire)&&(w_have||w_fire))begin
          target<=decode(effective_addr);aw_done<=0;w_done<=0;
          state<=(decode(effective_addr)==3)?W_ERROR:W_SEND;
        end else if(s_arvalid&&s_arready)begin
          address<=s_araddr;protection<=s_arprot;target<=decode(s_araddr);
          state<=((decode(s_araddr)==3)||(s_arprot[2]&&decode(s_araddr)!=0))?R_ERROR:R_SEND;
        end
      end
      R_SEND:if(m_arvalid[target]&&m_arready[target])state<=R_RESP;
      R_RESP:if(s_rvalid&&s_rready)state<=IDLE;
      W_SEND:begin
        if(m_awvalid[target]&&m_awready[target])aw_done<=1;
        if(m_wvalid[target]&&m_wready[target])w_done<=1;
        if((aw_done||(m_awvalid[target]&&m_awready[target]))&&(w_done||(m_wvalid[target]&&m_wready[target])))state<=W_RESP;
      end
      W_RESP:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      R_ERROR:if(s_rvalid&&s_rready)state<=IDLE;
      W_ERROR:if(s_bvalid&&s_bready)begin state<=IDLE;aw_have<=0;w_have<=0;end
      default:state<=IDLE;
    endcase
  end
endmodule
'''
 save('axil_xbar3.sv',header+body)

def core():
 header='''module c4_axi_core #(
  parameter logic [31:0] RESET_PC=32'h80000000,parameter bit FAULT_ADDI=0
)(
  '''+',\n  '.join(['input logic clock,reset','input logic [2:0] delay_enable','input logic [31:0] lfsr_seed',*[f'output wire {width(n)}{name}' for name,n in OBS],*ports('m_','master'),'output wire debug_arb_busy,debug_arb_owner'])+'\n);\n'
 body='''  wire i_req_valid,i_req_ready,i_resp_valid,i_resp_ready;
  wire [31:0] i_req_addr,i_resp_data;wire [1:0] i_resp_error;
  wire d_req_valid,d_req_ready,d_req_write,d_resp_valid,d_resp_ready;
  wire [31:0] d_req_addr,d_req_wdata,d_resp_data;wire [3:0] d_req_wstrb;wire [1:0] d_resp_error;
'''+wires('if_')+'\n'+wires('ls_')+'\n'
 body+='  c4_simple_core #(.STAGE(4),.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) core(.*);\n'
 for prefix,ro,prot in [('if_',1,4),('ls_',0,0)]:
  side='i' if ro else 'd'
  body+=f'  simple_to_axil #(.READ_ONLY({ro}),.PROT(3\'d{prot})) {side}_adapter(\n    .clock(clock),.reset(reset),\n'
  for name in ['req_valid','req_ready','req_addr','req_write','req_wdata','req_wstrb','resp_valid','resp_ready','resp_data','resp_error']:
   value={ 'req_write':"1'b0",'req_wdata':"32'b0",'req_wstrb':"4'b0"}.get(name,side+'_'+name) if ro else side+'_'+name
   body+=f'    .{name}({value}),\n'
  body+='    '+links('m_',prefix)+');\n'
 body+='  axil_arbiter2 arbiter(.clock(clock),.reset(reset),\n    '+links('s0_','if_')+',\n    '+links('s1_','ls_')+',\n    '+links('m_','m_')+',\n    .debug_busy(debug_arb_busy),.debug_owner(debug_arb_owner));\nendmodule\n'
 save('c4_axi_core.sv',header+body)

def soc():
 header='''module c4_axi_soc #(
  parameter logic [31:0] RESET_PC=32'h80000000,parameter bit FAULT_ADDI=0,
  parameter logic [31:0] RAM_BASE=32'h80000000,RAM_BYTES=32'h08000000,
  parameter logic [63:0] MTIME_RESET=0
)(
  '''+',\n  '.join(['input logic clock,reset','input logic [2:0] delay_enable','input logic [31:0] lfsr_seed',*[f'output wire {width(n)}{name}' for name,n in OBS],*ports('mem_','master'),*ports('mon_','monitor'),'output wire uart_tx_valid','output wire [7:0] uart_tx_data','output wire [63:0] mtime','output wire debug_arb_busy,debug_arb_owner'])+'\n);\n'
 body=wires('bus_')+'\n'+wires('x_',3)+'\n'
 for name,n,out in FIELDS:
  body+=f'  assign mon_{name}=bus_{name};\n'
  body+=f'  assign mem_{name}=x_{name}[{n-1}:0];\n' if out else f'  assign x_{name}[{n-1}:0]=mem_{name};\n'
 body+='  c4_axi_core #(.RESET_PC(RESET_PC),.FAULT_ADDI(FAULT_ADDI)) cpu(\n    .clock(clock),.reset(reset),.delay_enable(delay_enable),.lfsr_seed(lfsr_seed),\n    '
 body+=',\n    '.join(f'.{name}({name})' for name,n in OBS)+',\n    '+links('m_','bus_')+',\n    .debug_arb_busy(debug_arb_busy),.debug_arb_owner(debug_arb_owner));\n'
 body+='  axil_xbar3 #(.RAM_BASE(RAM_BASE),.RAM_BYTES(RAM_BYTES)) xbar(\n    .clock(clock),.reset(reset),\n    '+links('s_','bus_')+',\n    '+links('m_','x_')+');\n'
 for k,name in [(1,'uart'),(2,'clint')]:
  param='' if k==1 else ' #(.MTIME_RESET(MTIME_RESET))'
  body+=f'  axil_{name}{param} {name}(.clock(clock),.reset(reset),\n    '
  body+=',\n    '.join(f'.s_{field}(x_{field}[{k*n}+:{n}])' for field,n,_ in FIELDS)
  body+=',\n    .tx_valid(uart_tx_valid),.tx_data(uart_tx_data));\n' if k==1 else ',\n    .mtime(mtime));\n'
 body+='endmodule\n';save('c4_axi_soc.sv',header+body)

if __name__=='__main__':arbiter();xbar();core();soc()
