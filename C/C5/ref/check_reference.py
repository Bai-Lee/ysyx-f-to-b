import ctypes,json,struct,sys
from pathlib import Path
ROOT=Path('/workspace/projects/ysyx_f_to_b')
row=json.loads((ROOT/'reports/C5_reference_build.json').read_text());lib=ctypes.CDLL(row['binary'])
lib.difftest_init.argtypes=[ctypes.c_int];lib.difftest_regcpy.argtypes=[ctypes.c_void_p,ctypes.c_bool]
lib.difftest_memcpy.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_bool]
lib.difftest_exec.argtypes=[ctypes.c_uint64]
lib.difftest_init(0)
State=ctypes.c_uint32*33
state=State();state[32]=0x20000000
if '--bad-span' in sys.argv:
    buffer=ctypes.create_string_buffer(4);lib.difftest_memcpy(0x0f001ffe,buffer,4,False)
    raise AssertionError('OUT_OF_RANGE_NOT_REJECTED')
if '--bad-rom-write' in sys.argv:
    data=struct.pack('<III',0x200002b7,0x0002a023,0x00100073)
    buffer=ctypes.create_string_buffer(data);lib.difftest_memcpy(0x20000000,buffer,len(data),True)
    lib.difftest_regcpy(state,True);lib.difftest_exec(2)
    raise AssertionError('ROM_WRITE_NOT_REJECTED')
for address in [0x0f000000,0x0f001ff8,0x20000000,0x20000ff8,0x30000000,0x30fffff8,0x80000000,0x803ffff8,0xa0000000,0xa7fffff8,0xc0000000,0xc0000ff8]:
    payload=struct.pack('<II',address,address^0xa5a5a5a5);buffer=ctypes.create_string_buffer(payload)
    lib.difftest_memcpy(address,buffer,8,True);out=ctypes.create_string_buffer(8);lib.difftest_memcpy(address,out,8,False);assert out.raw==payload
code=struct.pack('<II',0x00700293,0x00100073);buffer=ctypes.create_string_buffer(code)
lib.difftest_memcpy(0x20000000,buffer,len(code),True);lib.difftest_regcpy(state,True);lib.difftest_exec(1);lib.difftest_regcpy(state,False)
assert state[5]==7 and state[32]==0x20000004
lib.difftest_exec(1);lib.difftest_regcpy(state,False);assert state[32]==0x20000008
print('C5_REFERENCE_MEMORY_AND_MROM_INSTRUCTIONS_PASS',flush=True)
