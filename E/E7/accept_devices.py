from common7 import *
def main():
 gui_path=ROOT/'reports/E7_gui.json';gui=json.loads(gui_path.read_text());assert gui['status'] in ['PASS_PENDING_VISUAL_REVIEW','PASS']
 assert gui['simulation']['result']=='GOOD_TRAP' and gui['simulation']['serial_matches'] and gui['simulation']['serial_framing_errors']==0
 for image in gui['screenshots']:assert sha(ROOT/image['file'])==image['sha256']
 review=json.loads((ROOT/'reports/E7_visual_review.json').read_text());assert review['status']=='PASS' and review['images']==gui['screenshots'],'Current screenshots require a new visual review'
 gui['status']='PASS';gui['visual_review']='reports/E7_visual_review.json';dump(gui_path,gui)
 for p in ['E7_gpio_unit','E7_csr_tests','E7_soc_hello']:assert json.loads((ROOT/'reports'/(p+'.json')).read_text())['status']=='PASS'
 rows=[]
 for target,divisor in [(115200,13),(57600,27)]:
  actual=25000000/(16*divisor);rows.append({'target_baud':target,'ideal_divisor':25000000/(16*target),'selected_divisor':divisor,'actual_baud':actual,'relative_error_percent':(actual/target-1)*100,'nvboard_calls_per_bit':16*divisor})
 dump(ROOT/'reports/E7_uart_math.json',{'status':'PASS_CALCULATED_AND_SIMULATED','soc_clock_hz':25000000,'oversampling':16,'settings':rows,'note':'Default13matchessuppliedloaderandNVBoard208. For115200,14wouldgive111607.14baud(-3.1188%),closerthan13;13isnotclaimedoptimal. Both13and27actualTXstreamsdecodedinE7_soc_hello;physicalseriallinktoleranceunmeasured.'})
 mark(['E7-M014'],'PASS',['reports/E7_uart_math.json','reports/E7_soc_hello.json','E/E7/NOTES.md'],'Bauddivisor16xoversamplinganderrorcalculated;default13/alternative14and57600divisor27distinguished;realSoCTXdigitalstreamsverified.')
 mark(['E7-M016','E7-M017','E7-M018','E7-M019','E7-M020','E7-M021'],'PASS',['reports/E7_gui.json','reports/E7_visual_review.json','reports/E7_gpio_unit.json','reports/E7_csr_tests.json','artifacts/E7/gui'],'ActualNVBoardTXdisplay/wrongpassword/correctunlock/16walkingLEDstates/hexIDdisplayverified;GPIOunitstrobe/APBnegativeandCSRreadonly/rollovernegativesretained;allGUIimagesvisuallyinspected.')
 print('SOC_GPIO_UART_CSR_VISUAL_ACCEPTANCE_PASS',flush=True)
if __name__=='__main__':main()
