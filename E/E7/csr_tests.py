from common7 import *
import struct
def csr(rd,address,rs=0):return (address<<20)|(rs<<15)|(2<<12)|(rd<<7)|0x73
def addi(rd,rs,imm):return ((imm&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def main():
 p=ROOT/'E/E7/programs';cases={
  'identity':[csr(1,0xf11),csr(2,0xf12),addi(10,0,0),0x00100073],
  'cycle_rollover':[addi(1,0,-16),csr(2,0xb00,1)]+[addi(0,0,0)]*32+[csr(3,0xb80),csr(4,0xb00),addi(10,0,0),0x00100073],
  'readonly_write':[addi(1,0,0),csr(2,0xf11,1)],
  'reserved_register':[csr(16,0xf11)],
  'unknown_csr':[csr(2,0x7ff)]}
 rows=[]
 for name,words in cases.items():
  image=p/('csr_'+name+'.bin');image.write_bytes(struct.pack('<'+'I'*len(words),*words));result=ROOT/'artifacts/E7/csr'/name/'result.json'
  exe=WORK/'build/E7/valid/sim';good=name in ['identity','cycle_rollover']
  o,e,r=run('E7/csr/'+name,[exe,'--image',image,'--report',result,'--max-cycles','10000'],inputs=[exe,image],outputs=[result],expected=(0,) if good else (3,));d=json.loads(result.read_text())
  if name=='identity':assert d['gpr'][1]==0x79737978 and d['gpr'][2]==26070001
  elif name=='cycle_rollover':assert d['gpr'][3]==1 and d['gpr'][4]<1024 and d['counter']>0xffffffff
  else:assert d['result']=='NPC_FAULT' and d['fault']==1
  rows.append({'case':name,'status':'PASS' if good else 'PASS_EXPECTED_REJECTION','result':d})
 dump(ROOT/'reports/E7_csr_tests.json',{'status':'PASS','cases':rows,'spec':'mvendorid=f11, marchid=f12, mcycle=b00, mcycleh=b80; csrrs with rs1=x0 is read-only, writes to identity CSRs rejected, counter bit-set and rollover tested.'})
 print('E7_CSR_TESTS_PASS',flush=True)
if __name__=='__main__':main()
