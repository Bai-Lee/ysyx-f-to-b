from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 p=ROOT/'E/E8';example=p/'examples';addresses=[0,1,2,3,0x0fffffff,0x10000000,0x20001000,0x30000000,0x7fffffff,0x80000000,0x807fffff,0x88000000,0xa0000048,0xdeadbeef,0xf0000000,0xffffffff];words=[]
 for a in addresses:
  high=((a+0x800)>>12)&0xfffff;low=a&4095
  words += [(high<<12)|(1<<7)|0x37,(low<<20)|(1<<15)|(1<<7)|0x13,(1<<15)|(4<<12)|(2<<7)|3,(2<<20)|(1<<15)|0x23]
 words.append(0x00100073);assert len(words)==65
 rom=example/'address_rom.hex';addr=example/'addresses.hex';rom.write_text(''.join(f'{x:08x}\n' for x in words));addr.write_text(''.join(f'{x:08x}\n' for x in addresses))
 src=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',p/'address_tb.sv'];rows=[]
 for fault in [False,True]:
  name='clipped' if fault else 'full';exe=WORK/('address_'+name+'.vvp')
  run('E8/address/'+name+'/compile',['iverilog','-g2012',*(['-DTEST_ADDRESS_CLIPPING'] if fault else []),'-s','address_tb','-o',exe,*src],inputs=src)
  o,e,r=run('E8/address/'+name+'/run',['vvp',exe,'+rom='+str(rom),'+addresses='+str(addr)],inputs=[exe,rom,addr],expected=(1,) if fault else (0,));assert ('ADDRESS_FORWARDING_ERROR' in o) if fault else ('FULL_ADDRESS_AND_WARM_RESET_PASS' in o)
  rows.append({'case':name,'stdout':o,'exit_code':r['exit_code']})
 dump(ROOT/'reports/E8_address_reset.json',{'status':'PASS','addresses_hex':[f'{a:08x}' for a in addresses],'cases':rows,'scope':'Actual core byte loads/stores across full32-bit addresses, lane masks, cold and repeated reset. Negative interface clipping rejected. RAM contents are not assumed to be reset by hardware.'})
 print('E8_ADDRESS_RESET_PASS',flush=True)
if __name__=='__main__':main()
