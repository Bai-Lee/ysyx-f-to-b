from common import *
import re
def values(text):
    names={};state={};timepoint=None;rows=[]
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('$var'):
            words=s.split();
            if words[4] in ('a','b','f'):names[words[3]]=words[4]
        elif s.startswith('#'):
            if timepoint is not None:rows.append((timepoint,dict(state)))
            timepoint=int(s[1:])
        elif s and s[0] in '01xz' and s[1:] in names:
            assert s[0] in '01';state[names[s[1:]]]=int(s[0])
    if timepoint is not None:rows.append((timepoint,dict(state)))
    return rows
def check(rows):
    for t,s in rows:
        assert set(s)=={'a','b','f'}
        assert s['f']==(s['a']+s['b'])%2,('XOR waveform mismatch',t,s)
    assert [t for t,s in rows]==list(range(0,160,10))
    assert {(s['a'],s['b']) for t,s in rows}=={(0,0),(0,1),(1,0),(1,1)}
def main():
    out,e,r=run('waves/fst_convert',['fst2vcd','-f',OUT/'waves/dual.fst'],inputs=[OUT/'waves/dual.fst'])
    a=values((OUT/'waves/dual.vcd').read_text());b=values(out);check(a);check(b);assert a==b
    bad=WORK/'dual.vcd';shutil.copyfile(bad,OUT/'waves/dual_bad.vcd')
    try:check(values(bad.read_text()))
    except AssertionError as x:assert 'XOR waveform mismatch' in str(x);rejected=str(x)
    else:raise AssertionError('Wrong circuit waveform accepted')
    dump(ROOT/'reports/E4_waves.json',{'status':'PASS','vcd_fst_same_samples':len(a),'end_ns':150,'vcd_bytes':(OUT/'waves/dual.vcd').stat().st_size,'fst_bytes':(OUT/'waves/dual.fst').stat().st_size,'actual_bad_trace_rejected':rejected,'scope':'16 bounded samples; size ratio is measured, not asserted to be always1/50.'})
    result(['E4-M005','E4-R002'],['reports/E4_waves.json','reports/E4_gui.json','artifacts/E4/waves'],'Real VCD and FST generated, decoded samples match; wrong-RTL VCD rejected; GTKWave actually displays all3 signals. Trace150ns, exhaustive/long runs do not dump huge waveforms.')
    print('WAVE_VERIFICATION_PASS',flush=True)
if __name__=='__main__':main()
