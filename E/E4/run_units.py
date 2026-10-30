from common import *
import re
def main():
    src=ROOT/'E/E4/rtl';cpp=ROOT/'E/E4/csrc';rows=[]
    for top in ['comb','sequential','keyboard','vga','motion']:
        rtl=src/('vga.sv' if top=='motion' else top+'.sv')
        old=OUT/'units'/top/'run.json';oldbuild=OUT/'build'/top/'run.json'
        if '--fresh' not in sys.argv and old.exists() and oldbuild.exists():
            past=json.loads(old.read_text());compiled=json.loads(oldbuild.read_text())
            complete_inputs=top!='vga' or str(WORK/'image.mem') in {x['path'] for x in past['inputs']}
            if complete_inputs and past['status']=='PASS' and compiled['status']=='PASS' and all(Path(x['path']).is_file() and sha(x['path'])==x['sha256'] for x in past['inputs']+compiled['inputs']):
                rows.append({'top':top,'result':(old.parent/'stdout.log').read_text().strip(),'run':past});print('REUSE_VERIFIED_UNCHANGED',top,flush=True);continue
        exe=build(top,[rtl],cpp/(top+'_test.cpp'),top,trace=False,flags=['-Wno-DECLFILENAME'])
        o,e,r=run('units/'+top,[exe],inputs=[exe,*([WORK/'image.mem'] if top=='vga' else [])],timeout=180)
        assert 'PASS' in o;rows.append({'top':top,'result':o.strip(),'run':r})
        if top=='vga':
            assert (WORK/'static_frame.ppm').read_bytes()==(ROOT/'E/E4/data/expected.ppm').read_bytes()
            shutil.copyfile(WORK/'static_frame.ppm',OUT/'static_frame.ppm')
    dump(ROOT/'reports/E4_units.json',{'status':'PASS','runs':rows,'trace_volume':'No waveform on exhaustive or long tests; selected short traces generated separately.'})
    result(['NJU-02-01','NJU-02-02','NJU-03-01','NJU-03-02','NJU-03-03','NJU-06-01','NJU-06-02','NJU-06-03','NJU-07-01','NJU-07-02','NJU-07-03','NJU-08-01','NJU-08-02','NJU-08-03'],['reports/E4_units.json'],'RTL exhaustive/model-backed unit validation completed. NVBoard integration is tracked separately; no physical FPGA claim.')
    print('E4_UNIT_BATCH_PASS',flush=True)
if __name__=='__main__':main()
