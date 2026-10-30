from pathlib import Path
import sys,re,shlex
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
def main():
    dest=Path('/workspace/downloads/ysyx_c_stage/opensta');dest.mkdir(parents=True,exist_ok=True)
    install=Path('/home/USER/tools/c-stage/opensta');install.mkdir(exist_ok=True)
    o,_,_=run('C4/opensta/package-uri',['apt-get','--print-uris','download','opensta'])
    line=next(x for x in o.splitlines() if x.startswith("'"));url,name,size,checksum=shlex.split(line)
    assert url.startswith('http://archive.ubuntu.com/ubuntu/');kind,expected=checksum.split(':',1);assert kind in ('SHA256','SHA512')
    archive=dest/name
    if not archive.exists():run('C4/opensta/download',['apt-get','download','opensta'],cwd=dest,timeout=120)
    h=hashlib.new(kind.lower());h.update(archive.read_bytes());assert archive.stat().st_size==int(size) and h.hexdigest()==expected
    run('C4/opensta/extract',['dpkg-deb','-x',archive,install],inputs=[archive],resume=True)
    exe=install/'usr/bin/sta';v,_,_=run('C4/opensta/version',[exe,'-version'],inputs=[exe])
    d=ROOT/'C/C4/synthesis/opensta';d.mkdir(exist_ok=True);lib=Path('/home/USER/tools/icsprout55-e-stage/IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CL/liberty/ics55_LLSC_H7CL_typ_tt_1p2_25_nldm.lib')
    net=d/'control.v';net.write_text('module control(input clock,output q);wire d,qn;INVX1H7L inv(.A(q),.Y(d));DFFX1H7L ff(.CK(clock),.D(d),.Q(q),.QN(qn));endmodule\n')
    results=[]
    for label,period in [('good',10),('bad_timing',0.001)]:
        script=d/(label+'.tcl');script.write_text('if {[catch {\nread_liberty {'+str(lib)+'}\nread_verilog {'+str(net)+'}\nlink_design control\ncreate_clock -name clk -period '+str(period)+' [get_ports clock]\nset_load 0.005 [get_ports q]\nreport_checks -path_delay max -digits 6\nreport_worst_slack -digits 6\nputs "STA_SCRIPT_COMPLETE"\n} message]} {puts stderr "STA_SCRIPT_ERROR $message"; exit 1}\nexit\n')
        o,e,r=run('C4/opensta/control-'+label,[exe,'-exit',script],inputs=[exe,script,lib,net],timeout=120)
        assert 'STA_SCRIPT_COMPLETE' in o and 'STA_SCRIPT_ERROR' not in e and 'Error:' not in o+e
        slack=float(re.search(r'worst slack\s+(-?[\d.]+)',o)[1]);assert (slack>0)==(label=='good'),slack
        results.append({'case':label,'period_ns':period,'worst_slack_ns':slack,'status':'PASS' if label=='good' else 'EXPECTED_TIMING_VIOLATION_DETECTED'})
    dump(ROOT/'reports/C4_opensta_toolchain.json',{'status':'PASS_POSITIVE_AND_NEGATIVE_TIMING','binary':str(exe),'sha256':sha(exe),'version':v.strip(),'package':{'url':url,'archive':str(archive),'official_digest_algorithm':kind,'official_digest':expected,'official_digest_match':True,'sha256':sha(archive)},'controls':results,'scope':'Task-local official Ubuntu OpenSTA extraction; no system installation. Added because ECC post-synthesis STA exceeded the recorded memory guard on the required full2KB baseline. Uses same characterized TT cells, not replacement ideal delays.'})
    print('C4_OPENSTA_READY',v.strip(),flush=True)
if __name__=='__main__':main()
