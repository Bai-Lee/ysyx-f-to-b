"""Original, redistributable NES NROM interaction fixture, no commercial ROM assets.

6502 opcodes and PPU/APU/controller addresses follow the archived FCEUX source.
J (NES A) changes the checkerboard colour and pulse-channel pitch while held.
This tests emulator video/input/audio, not game completion or human gameplay.
"""
from pathlib import Path
import struct,json,hashlib
BASE=0x8000
code=bytearray();labels={};fixups=[]
def emit(*b):code.extend(b)
def label(n):assert n not in labels;labels[n]=BASE+len(code)
def branch(op,n):emit(op,0);fixups.append((len(code)-1,n,True))
def jump(n):emit(0x4c,0,0);fixups.append((len(code)-2,n,False))
def lda(v):emit(0xa9,v)
def sta(a):emit(0x8d,a&255,a>>8)
def load(a):emit(0xad,a&255,a>>8)
def bit(a):emit(0x2c,a&255,a>>8)
def write(a,v):lda(v);sta(a)
label('reset');emit(0x78,0xd8,0xa2,0xff,0x9a,0xe8) # SEI,CLD,LDX #ff,TXS,INX
for a in [0x2000,0x2001,0x4010]:emit(0x8e,a&255,a>>8) # STX
for n in ['vblank1','vblank2']:label(n);bit(0x2002);branch(0x10,n)
write(0x2006,0x3f);write(0x2006,0);emit(0xa2,0x20);lda(0x0f)
label('palette');sta(0x2007);emit(0xca);branch(0xd0,'palette')
write(0x2006,0x20);write(0x2006,0);emit(0xa0,4,0xa2,0);lda(1)
label('fill');sta(0x2007);emit(0xe8);branch(0xd0,'fill');emit(0x88);branch(0xd0,'fill')
write(0x4015,1);write(0x4000,0xbf);write(0x4001,8);write(0x4002,0xfd);write(0x4003,8)
lda(0);emit(0x85,1) # previous controller state
write(0x2001,0x0a)
label('frame');bit(0x2002);branch(0x10,'frame')
write(0x4016,1);write(0x4016,0);load(0x4016);emit(0x29,1,0xc5,1);branch(0xf0,'audio_done')
emit(0x85,1,0xc9,0);branch(0xf0,'released_sound') # STA preserves flags: explicitly compare the new state
write(0x4002,0xfc);write(0x4003,9);jump('audio_done')
label('released_sound');write(0x4002,0xfd);write(0x4003,8)
# Writing APU $4003 every frame restarts its sequencer; update only on button edges.
label('audio_done');emit(0xa5,1);branch(0xf0,'released_color');lda(0x16);jump('color')
label('released_color');lda(0x21)
label('color');emit(0x85,0) # save colour in zero-page
write(0x2006,0x3f);write(0x2006,1);emit(0xa5,0);sta(0x2007)
write(0x2006,0x20);write(0x2006,0);write(0x2005,0);write(0x2005,0);jump('frame')
label('irq');emit(0x40)
for off,n,relative in fixups:
 target=labels[n]
 if relative:
  delta=target-(BASE+off+1);assert -128<=delta<=127;code[off]=delta&255
 else:code[off:off+2]=struct.pack('<H',target)
prg=bytearray([0xea]*16384);prg[:len(code)]=code
prg[-6:]=struct.pack('<HHH',labels['irq'],labels['reset'],labels['irq'])
chrrom=bytearray(8192);chrrom[16:24]=bytes([0xaa,0x55]*4)
rom=b'NES\x1a'+bytes([1,1,0,0])+bytes(8)+prg+chrrom
p=Path(__file__).parent/'homebrew';p.mkdir(exist_ok=True)
(p/'interaction.nes').write_bytes(rom)
(p/'symbols.json').write_text(json.dumps({'labels':labels,'code_bytes':len(code),'rom_sha256':hashlib.sha256(rom).hexdigest(),'license':'CC0-1.0, authored for this project; contains no third-party ROM data'},indent=2))
print('HOME_BREW_ROM',len(rom),hashlib.sha256(rom).hexdigest())
