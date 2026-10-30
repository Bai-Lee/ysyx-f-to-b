from common import *
def main():
    source=ROOT/'F/rtl/scpu.sv';dest=ROOT/'E/E4/rtl/scpu.sv'
    text=source.read_text().replace('parameter ENHANCED=0','parameter bit ENHANCED=0')
    text=text.replace("next_pc=pc+{4'b0,instruction[5:2]};","next_pc=pc+displacement+(instruction[5]?8'd16:8'd0);")
    dest.write_text(text)
    for name in ['f5_sum10','f6_sum10','f6_output']:
        shutil.copyfile(ROOT/'F/programs'/(name+'.hex'),ROOT/'E/E4/data'/(name+'.hex'))
    image=bytes(int(x,16) for x in (ROOT/'E/E4/data/f6_output.hex').read_text().split());assert len(image)==256
    packed=int.from_bytes(image,'little')
    (ROOT/'E/E4/rtl/program_rom.sv').write_text(f'''module program_rom(input wire [7:0] address,output wire [7:0] instruction);
  instruction_rom_mux rom(address,2048'h{packed:0512x},instruction);
endmodule
''')
    dump(OUT/'cpu_source.json',{'source':str(source),'source_sha256':sha(source),'derived':str(dest),'derived_sha256':sha(dest),'change':'Explicit one-bit ENHANCED parameter; equivalent injected unsigned-branch fault uses displacement so the fault build remains lint-clean. Correct logic and original F source unchanged.','isa':'F6 enhanced sISA; separate F5 base-mode emulator self-check also provided. Not RISC-V.'})
    print('CPU_SOURCE_PREPARED',flush=True)
if __name__=='__main__':main()
