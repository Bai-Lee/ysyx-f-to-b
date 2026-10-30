#!/usr/bin/env python3
"""Check published file bytes against the public snapshot's SHA-256 list."""
from pathlib import Path
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--full',action='store_true',help='require the Release supplement as well as the Git files')
 args=parser.parse_args()
 optional={r['path'] for r in json.loads((ROOT/'publication/supplement.json').read_text(encoding='utf-8'))['files']}
 checked=0;omitted=0;errors=[]
 for line in (ROOT/'publication/FILES.sha256').read_text(encoding='utf-8').splitlines():
  expected,relative=line.split('  ',1);path=(ROOT/relative).resolve()
  if not path.is_relative_to(ROOT):raise RuntimeError('invalid manifest path')
  if not path.is_file():
   if relative in optional and not args.full:omitted+=1;continue
   errors.append(relative+': MISSING');continue
  if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:errors.append(relative+': SHA256_MISMATCH')
  checked+=1
 for error in errors:print(error,file=sys.stderr)
 print(json.dumps({'status':'FAIL' if errors else 'PASS','checked_files':checked,'optional_supplement_files_absent':omitted,'failures':len(errors)}))
 return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
