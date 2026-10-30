"""Independent small references for data-cache replacement and locality."""
from pathlib import Path
import sys,struct
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    folder=WORK/'b3/trace-controls';folder.mkdir(parents=True,exist_ok=True)
    executable=WORK/'b3/tools/cachesim';assert executable.is_file()
    sequence=[(0xa0000000,False),(0xa0000004,True),(0xa0000004,False),
              (0xa0000008,False),(0xa000000c,False),(0xa0000000,False),(0x10000000,True)]
    fixture=folder/'data.bin';fixture.write_bytes(b''.join(struct.pack('<5I',0x80000000+4*i,0x23 if w else 0x03,0x80000004+4*i,a,3 if w else 1) for i,(a,w) in enumerate(sequence)))
    text,_,_=run('B3/trace-controls/data',[executable,'--trace',fixture,'--data','--lines','2','--words','1','--ways','1'],inputs=[executable,fixture])
    data=json.loads(text)['configs'][0]
    for name,expected in {'accesses':7,'misses':5,'bypasses':1,'reads':5,'writes':2,'writebacks':1}.items():assert data[name]==expected,(name,data)
    locality=[]
    for name,stride,expected in [('array',4,16),('scattered-list',128,64)]:
        path=folder/(name+'.bin');path.write_bytes(b''.join(struct.pack('<5I',0x80000000,0x03,0x80000004,0xa0000000+i*stride,1) for i in range(64)))
        text,_,_=run('B3/trace-controls/'+name,[executable,'--trace',path,'--data','--lines','8','--words','4','--ways','2'],inputs=[executable,path])
        row=json.loads(text)['configs'][0];assert row['misses']==expected and row['accesses']==64
        locality.append({'layout':name,'stride_bytes':stride,'result':row,'source':'Authored synthetic address sequence, not an observed application trace'})
    dump(ROOT/'reports/B3_trace_controls.json',{'status':'PASS','data_reference':data,'locality':locality,'scope':'Hand-calculated direct-mapped WB/WA fixture exercises hits, clean replacement, dirty eviction and MMIO bypass. Synthetic locality examples hold access count and cache parameters fixed; linked lists allocated contiguously need not behave like this scattered example.'})
    print('B3_TRACE_CONTROLS_PASS')

if __name__=='__main__':main()
