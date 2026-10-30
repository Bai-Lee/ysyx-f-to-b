"""Extract the already validated combinational decode for the pipelined core."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
def main():
    source=ROOT/'B/soc/rtl/ysyx_00000000_execute.sv';text=source.read_text()
    fields=text[text.index('  wire [4:0] rd='):text.index('  logic [31:0] value,next_pc;')]
    fields='\n'.join(line for line in fields.splitlines() if not line.startswith(('  wire [31:0] a=','  wire [31:0] b=')))+'\n'
    first=text.index('  always_comb begin\n    value=0;');last=text.index('  always_ff @(posedge clock)',first)
    body=text[first:last]
    body=body.replace('    exec_valid=!reset&&!halted&&decode_fault==0;\n    mem_ren=exec_valid&&loads;mem_wen=exec_valid&&stores;\n','')
    header='''/* Pure RV32E decoder/ALU; load completion and architectural state live in the pipeline. */
module ysyx_00000000_alu #(parameter bit FAULT_ADDI=0)(
  input wire [31:0] pc,inst,a,b,mem_rdata,csr_old,csr_mtvec,csr_mepc,
  input wire csr_known,csr_readonly,
  output logic [31:0] value,next_pc,mem_addr,mem_wdata,csr_new,
  output logic [2:0] mem_size,decode_fault,
  output logic writes,loads,stores,uses_a,uses_b,exec_ebreak,csr_write,do_ecall,do_mret
);
  logic legal,take;logic [31:0] csr_operand;
'''
    out=ROOT/'B/soc/rtl/ysyx_00000000_alu.sv';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(header+fields+body+'endmodule\n')
    (ROOT/'reports/B4_decoder_source.json').write_text(json.dumps({'status':'GENERATED_NOT_VALIDATED','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'scope':'Only the combinational switch is reused. Pipeline state, hazards and retirement are new and require independent tests.'},indent=2))
if __name__=='__main__':main()
