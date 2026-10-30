#!/usr/bin/env python3
"""Portable four-state smoke test of the frozen final B CPU (Python stdlib only)."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]

def addi(rd,rs1,imm):return ((imm&4095)<<20)|(rs1<<15)|(rd<<7)|0x13
def lui(rd,value):return (value&0xfffff000)|(rd<<7)|0x37
def store(rs2,rs1,offset,funct3):
    return (((offset>>5)&127)<<25)|(rs2<<20)|(rs1<<15)|(funct3<<12)|((offset&31)<<7)|0x23

def hello_image(exit_code):
    # Every instruction is RV32E: t0=x5 and t1=x6. See examples/hello.S.
    words=[lui(5,0x10000000)]
    for char in b'Hello from the final B-stage RV32E CPU!\n':
        words += [addi(6,0,char),store(6,5,0,0)]
    words += [lui(5,0x10001000),addi(6,0,exit_code),store(6,5,0,2),
              lui(6,0xb00d6000),addi(6,6,13),store(6,5,4,2),0x0000006f]
    return b''.join(struct.pack('<I',word) for word in words)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def tool(name):
    value=os.environ.get(name.upper(),name)
    found=shutil.which(value)
    if not found:raise RuntimeError(f'{name} is missing; install Icarus Verilog or set {name.upper()} to its executable path')
    return found

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative',action='store_true',help='expect a deliberately nonzero mailbox exit')
    parser.add_argument('--image',type=Path,help='custom little-endian BIN linked at 0x80000000; see docs/SIMULATION.md')
    parser.add_argument('--wave',type=Path,help='optional VCD output')
    parser.add_argument('--netlist',action='store_true',help='use the final Nangate45 mapped netlist and its simulation cells')
    parser.add_argument('--timeout',type=int,default=180)
    parser.add_argument('--max-cycles',type=int,default=100000)
    args=parser.parse_args()
    if args.negative and args.image:parser.error('--negative is for the bundled hello program only')
    if args.timeout<=0 or args.max_cycles<=0:parser.error('limits must be positive')
    stamp=time.strftime('%Y%m%dT%H%M%S')+'-'+str(time.time_ns()%1000000000)
    work=ROOT/'build'/('negative' if args.negative else 'hello')/stamp
    work.mkdir(parents=True)
    data=args.image.read_bytes() if args.image else hello_image(1 if args.negative else 0)
    if not 0<len(data)<=4*1024*1024:raise RuntimeError('image must contain 1 byte to 4 MiB')
    (work/'image.bin').write_bytes(data)
    hexfile=work/'image.hex'
    # Unwritten RAM remains X. The final partial word gets X bytes, never zeros.
    hexfile.write_text('\n'.join('xx'*(4-len(data[i:i+4]))+data[i:i+4][::-1].hex() for i in range(0,len(data),4))+'\n')
    tb=ROOT/'B/B5/cpu_four_state_tb.sv'
    sources=[ROOT/'B/B5/netlist/ysyx_00000000.v',ROOT/'B/models/nangate45/sim/cells.v'] if args.netlist else [ROOT/'B/soc/build/ysyx_00000000.sv']
    iv,vvp=tool('iverilog'),tool('vvp')
    executable=work/'sim.vvp'
    commands=[[iv,'-g2012','-s','cpu_four_state_tb','-o',str(executable),str(tb),*[str(p) for p in sources]],
              [vvp,str(executable),'+IMAGE='+str(hexfile),'+WORDS='+str((len(data)+3)//4),'+MAX_CYCLES='+str(args.max_cycles),'+FAST=0']]
    if args.wave:
        wave=args.wave.resolve();wave.parent.mkdir(parents=True,exist_ok=True)
        commands[1].append('+WAVE='+str(wave))
    result={'status':'NOT_RUN','mode':'netlist' if args.netlist else 'rtl',
            'expected':'BAD_TRAP' if args.negative else 'PROGRAM_PASS',
            'image_sha256':hashlib.sha256(data).hexdigest(),
            'inputs':{p.relative_to(ROOT).as_posix():digest(p) for p in [tb,*sources]},'commands':commands,'runs':[]}
    try:
        for index,command in enumerate(commands):
            start=time.monotonic()
            try:
                run=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=args.timeout)
            except subprocess.TimeoutExpired as error:
                result['status']='TIMEOUT'
                (work/f'{index}.stdout.log').write_bytes(error.stdout or b'')
                (work/f'{index}.stderr.log').write_bytes(error.stderr or b'')
                raise RuntimeError(f'stage {index} reached the {args.timeout}s time limit') from error
            (work/f'{index}.stdout.log').write_bytes(run.stdout)
            (work/f'{index}.stderr.log').write_bytes(run.stderr)
            result['runs'].append({'exit_code':run.returncode,'elapsed_seconds':round(time.monotonic()-start,4)})
            if index==0 and run.returncode:raise RuntimeError('Icarus compilation failed')
            if index==1:
                output=run.stdout.decode(errors='replace')
                print(output,end='')
                valid=(run.returncode!=0 and 'B5_BAD_TRAP code=00000001' in output and 'B5_PROGRAM_PASS' not in output) if args.negative else (run.returncode==0 and 'B5_PROGRAM_PASS' in output and 'B5_BAD_TRAP' not in output)
                if not valid:raise RuntimeError('program outcome did not match the expected mailbox result')
        result['status']='PASS_EXPECTED_REJECTION' if args.negative else 'PASS'
        print('PUBLIC_DEMO_'+result['status'])
    except Exception:
        if result['status']!='TIMEOUT':result['status']='FAIL'
        raise
    finally:
        (work/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print('Evidence:',work.relative_to(ROOT))

if __name__=='__main__':
    try:main()
    except Exception as error:print('ERROR:',error,file=sys.stderr);sys.exit(1)

