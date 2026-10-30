from pathlib import Path
import sys,argparse,gzip
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',action='store_true');args=parser.parse_args()
    row=next(r for r in json.loads((ROOT/'reports/B3_performance.json').read_text())['runs'] if r['variant']=='b5-release' and r['size']=='test')
    trace=Path(row['trace']);folder=ROOT/'artifacts/B3/trace-storage';folder.mkdir(parents=True,exist_ok=True)
    target=folder/'retired.bin.gz';metrics=folder/'metrics.json'
    if args.worker:
        start=time.monotonic()
        with trace.open('rb') as source,target.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=6) as output:
            shutil.copyfileobj(source,output,1048576)
        writing=time.monotonic()-start;start=time.monotonic();h=hashlib.sha256();count=0
        with gzip.open(target,'rb') as source:
            for block in iter(lambda:source.read(1048576),b''):h.update(block);count+=len(block)
        reading=time.monotonic()-start
        assert count==trace.stat().st_size==20*row['simulation']['instructions'] and h.hexdigest()==sha(trace)
        dump(metrics,{'status':'PASS','codec':'gzip/DEFLATE level6','raw_bytes':count,'compressed_bytes':target.stat().st_size,'compression_ratio':target.stat().st_size/count,'write_seconds':writing,'restore_hash_seconds':reading,'trace_sha256':h.hexdigest(),'archive_sha256':sha(target)});return
    run('B3/trace-storage/check',['python3',Path(__file__),'--worker'],inputs=[Path(__file__),trace],outputs=[target,metrics],timeout=120)
    result=json.loads(metrics.read_text());result['scope']='Complete final test-scale20-byte binary trace; gzip is an authored storage choice. Decompressed byte count and SHA match every source byte. Compression and restore/hash wall times are measured on this host; no RLE/bzip2 implementation claim.'
    dump(ROOT/'reports/B3_trace_storage.json',result);print('B3_TRACE_STORAGE_PASS',result['raw_bytes'],result['compressed_bytes'])

if __name__=='__main__':main()
