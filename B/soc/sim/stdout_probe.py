"""Observe real simulator stdout before termination; no synthetic UART output."""
import argparse,json,os,selectors,signal,subprocess,time
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--exe',required=True);p.add_argument('--image',required=True)
    p.add_argument('--expected',choices=['A','line','none'],required=True);p.add_argument('--buffered',action='store_true')
    p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    command=[args.exe,'--mrom',args.image,'--max-cycles','1000000000','--no-diff']+(['--buffered'] if args.buffered else [])
    start=time.monotonic();data=b'';observed=None;limit=1.0 if args.expected=='none' else 3.0
    with (out/'child.stderr').open('wb') as err:
        child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=err,start_new_session=True)
        selector=selectors.DefaultSelector();selector.register(child.stdout,selectors.EVENT_READ)
        try:
            while time.monotonic()-start<limit and child.poll() is None:
                for key,_ in selector.select(.05):
                    block=os.read(key.fd,4096)
                    if not block:break
                    data+=block
                target=b'A\n' if args.expected=='line' else b'A'
                if args.expected!='none' and data==target:
                    observed=time.monotonic()-start;break
            running=child.poll() is None
        finally:
            selector.close()
            if child.poll() is None:os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
            data+=child.stdout.read();child.stdout.close()
    (out/'child.stdout').write_bytes(data)
    success=running and (data==b'' if args.expected=='none' else data==(b'A\n' if args.expected=='line' else b'A') and observed is not None)
    report={'status':'PASS_EXPECTED_OBSERVATION' if success else 'FAIL','command':command,'cwd':os.getcwd(),
            'expected':args.expected,'line_buffered':args.buffered,'stdout_hex':data.hex(),'observed_seconds':observed,
            'observation_limit_seconds':limit,'elapsed_seconds':time.monotonic()-start,'running_before_stop':running,
            'child_exit_code':child.returncode,'stop':'Explicit SIGTERM after bounded observation; not natural program completion.'}
    (out/'observation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
    return 0 if success else 1


if __name__=='__main__':raise SystemExit(main())
