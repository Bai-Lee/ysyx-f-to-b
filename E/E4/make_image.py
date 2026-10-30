from common import *
def main():
    d=ROOT/'E/E4/data';d.mkdir(exist_ok=True)
    rgb=bytearray();values=[]
    for y in range(480):
        for x in range(640):rgb.extend((x%256,y%256,((x//8)^(y//8))*17%256))
    source=d/'source.ppm';source.write_bytes(b'P6\n640 480\n255\n'+rgb)
    for x in range(640):
        for y in range(512):
            r,g,b=rgb[3*(y*640+x):3*(y*640+x)+3] if y<480 else (255,255,255)
            values.append(((r>>4)<<8)|((g>>4)<<4)|(b>>4))
    (d/'image.mem').write_text(''.join(f'{v:03x}\n' for v in values))
    (d/'image.mif').write_text('WIDTH=12;\nDEPTH=327680;\nADDRESS_RADIX=HEX;\nDATA_RADIX=HEX;\nCONTENT BEGIN\n'+''.join(f'{i:05X} : {v:03X};\n' for i,v in enumerate(values))+'END;\n')
    # Independently recover the row-major displayed bytes from the MIF contents.
    import re
    parsed={int(a,16):int(b,16) for a,b in re.findall(r'^([0-9A-F]+) : ([0-9A-F]+);$',(d/'image.mif').read_text(),re.M)}
    assert len(parsed)==327680
    recovered=bytearray()
    for y in range(480):
        for x in range(640):
            v=parsed[x*512+y];recovered.extend(((v>>8)*16,((v>>4)&15)*16,(v&15)*16))
    assert recovered==bytearray(v&0xf0 for v in rgb)
    assert all(parsed[x*512+y]==0xfff for x in range(640) for y in range(480,512))
    (d/'expected.ppm').write_bytes(b'P6\n640 480\n255\n'+recovered)
    shutil.copyfile(d/'image.mem',WORK/'image.mem')
    dump(OUT/'image_conversion.json',{'status':'PASS','source':'Authored deterministic RGB test pattern; not externally sourced art','width':640,'height':480,'memory_width':12,'depth':327680,'layout':'column-major x*512+y; unused rows480..511 white','mif_sha256':sha(d/'image.mif'),'mem_sha256':sha(d/'image.mem'),'source_sha256':sha(source),'expected_sha256':sha(d/'expected.ppm')})
    print('IMAGE_CONVERSION_PASS',flush=True)
if __name__=='__main__':main()
