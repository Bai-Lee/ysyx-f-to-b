from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
spec=json.loads((ROOT/'C/runtime/course_specs.json').read_text());notes=ROOT/'C/C5/NOTES.md';entries=[]
required_reports=['C4_AUDIT.json','C5_ram.json','C5_flash_boot.json','C5_gui_gpio.json','C5_gui_keyboard.json','C5_gui_rtthread.json','C5_spi_shared.json','C5_gui_rtguard.json','C5_gui_rtbench.json']
reports={name:json.loads((ROOT/'reports'/name).read_text()) for name in required_reports}
for name in ['C5_gui_gpio.json','C5_gui_keyboard.json','C5_gui_rtthread.json','C5_gui_rtguard.json','C5_gui_rtbench.json']:assert reports[name]['status']=='PASS'
assert reports['C5_spi_shared.json']['status']=='PASS_REPRODUCED_XIP_MANUAL_SPI_CONFLICT_AND_RELOCATION'
sweeps=json.loads((ROOT/'reports/C5_psram_sweep.json').read_text());mem=next(row for row in sweeps['runs'] if row['bytes']==4194304 and not row['corrupt'])
loader=json.loads((ROOT/'reports/C5_loader.json').read_text());assert 'printf' not in mem['symbols'] and 'printf' in loader['runs'][0]['symbols']
descriptions={
 'C5-O001':('PASS','Actual C4 UART/CLINT runtime evidence reused for the C5 bus prerequisite.',['reports/C4_AUDIT.json']),
 'C5-R001':('REFERENCE_ONLY','Devicewindows andphysicalcapacities scoped to the pinnedcompleteSoC; futuretapeoutallocation not asserted.',['reports/C5_source_lock.json']),
 'C5-O002':('PASS','Originalfib writesROM andfails; SRAMdata/BSSplacement andpoisonedcopy/zero controls retained.',['reports/C5_ram.json']),
 'C5-O003':('REFERENCE_ONLY','ReturnedAXIerrors causeexplicitNPCfaultstop. Fullarchitecturalaccess-fault traps/allunmappedresponses are not implemented or asserted.',['reports/C5_xip.json']),
 'C5-O004':('PASS','ActualELFsymbols:printfabsentfromfullPSRAMmemtest,presentinloaderpayload; archiveextraction/sectionGC/KEEP explained.',['reports/C5_psram_sweep.json','reports/C5_loader.json','C/C5/am/ysyxsoc.mk']),
 'C5-O005':('REFERENCE_ONLY','Eightwidth/patternpasses do not establish allfaultmodels,retention,electricalrefreshorMBISTcoverage. Noextra memorytesttoolclaim.',[]),
 'C5-O006':('PASS','OnefunctionalCoreMarkiteration retainsalgorithms/CRC; not aqualifiedCoreMarkscore. Memoryplacementimprovementmeasuredseparately.',['reports/C5_flash_boot.json','reports/C5_psram_apps.json']),
 'C5-O007':('PASS','ActualXIP/manualSPIsharing conflict reproducedaswrongSPIcommand00h withmodelassertion; SRAMrelocationpasses.',['reports/C5_spi_shared.json']),
 'C5-O008':('OPTIONAL_NOT_IMPLEMENTED','SPIinterruptcompletion-queryvariant is optional andnot implemented. CurrentXIPusespolling; noenergysavingclaim.',[]),
 'C5-O009':('REFERENCE_ONLY','Logicalbank/row/column modeling; internalDRAMsubarraysandpaperperformance notmodeled.',[]),
 'C5-R002':('PASS','LockedNVBoard1.0code actuallytransmits/receivesUART; nofloatinggitpull duringacceptance.',['reports/C5_nvboard_setup.json','reports/C5_gui_gpio.json','reports/C5_gui_keyboard.json']),
 'C5-R003':('PASS','Updatedam-tests uses(char)-1 sentinel; actualUARTandPS2input includingEscape/PageUp passed.',['reports/C5_gui_keyboard.json']),
 'C5-R004':('PASS','PrivateRTconfiguration regenerated; pollingUARTinput, invalidcommand recovery andsubsequentcommands actuallyverified.',['reports/C5_rtthread_interactive_setup.json','reports/C5_gui_rtthread.json']),
 'C5-O010':('REFERENCE_ONLY','Frame1,228,800B;60Hz73.728MB/s;50MHzquadPSRAMraw25MB/s. VGAneedsDMA/arbiter/FIFOandbandwidthbudget to useexternalmemory; notimplemented.',[]),
 'C5-R005':('PASS','ActualRTAMapp integration andreturn-to-shell/relaunch; typedFCEUX,Helloandall10MicroBenchsubtests withheapownership/guardcontrols.',['reports/C5_gui_rtthread.json','reports/C5_gui_rtbench.json','reports/C5_gui_rtguard.json'])}
for task in spec['tasks']:
    if task['id'] not in descriptions:continue
    status,detail,evidence=descriptions[task['id']];evidence=['C/C5/NOTES.md',*evidence]
    for name in evidence:assert (ROOT/name).is_file()
    row={'id':task['id'],'classification':task['classification'],'status':status,'details':detail,'evidence':evidence};entries.append(row)
    mark([task['id']],status,evidence,detail)
assert len(entries)==15
dump(ROOT/'reports/C5_background.json',{'status':'SOURCE_SCOPE_RECONCILED','records':entries,'notes_sha256':sha(notes),'scope':'All15 C5 optional/background/reminder records explicitly addressed. Reference-only andunimplementedoptionalstates are not counted asruntimepasses. Mandatoryengineering taskstatus remains separate.'})
print('C5_BACKGROUND_RECONCILED',len(entries),flush=True)
