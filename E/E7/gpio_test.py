from common7 import *
def main():
 p=ROOT/'E/E7';rows=[]
 for fault in [False,True]:
  name='fault_setup' if fault else 'correct';exe=WORK/('gpio_'+name+'.vvp')
  run('E7/gpio/'+name+'/compile',['iverilog','-g2012','-s','gpio_tb',*(['-DFAULT_GPIO_SETUP_WRITE'] if fault else []),'-o',exe,p/'rtl/mygpio_top_apb.v',p/'gpio_tb.sv'],inputs=[p/'rtl/mygpio_top_apb.v',p/'gpio_tb.sv'])
  o,e,r=run('E7/gpio/'+name+'/run',['vvp',exe],inputs=[exe],expected=(1,) if fault else (0,))
  assert ('modified during APB setup' in o) if fault else ('GPIO_APB_PASS' in o)
  rows.append({'case':name,'exit':r['exit_code'],'stdout':o})
 dump(ROOT/'reports/E7_gpio_unit.json',{'status':'PASS','cases':rows,'scope':'Four-state Icarus, APB setup/access, every byte strobe, every hex digit, reads/read-only/reserved address and repeated reset; erroneous setup-phase write is rejected.'})
 print('GPIO_POSITIVE_NEGATIVE_PASS',flush=True)
if __name__=='__main__':main()
