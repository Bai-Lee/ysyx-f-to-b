from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    p=ROOT/'E/E5'
    x=build('E5/dpi','dpi_example',[p/'dpi_example.sv'],[p/'dpi_example.cpp'])
    o,e,r=run('E5/dpi/run',[x],inputs=[x]);assert 'PASS official DPI' in o and '00000003' in o
    x=build('E5/dpi_negative','dpi_example',[p/'dpi_example.sv'],[p/'dpi_example.cpp'],flags=['-CFLAGS','-DBAD_DPI'])
    o,e,r=run('E5/dpi_negative/run',[x],inputs=[x],expected=(1,));assert 'DPI_MISMATCH' in e
    mark(['E5-M015'],'PASS',['artifacts/E5/dpi','artifacts/E5/dpi_negative'],'Executed installed Verilator manual DPI add import/example, signed parameters and returns; compiled faulty C implementation rejected.')
    pdf=ARCHIVE/'assets/offline/github.com/riscv/riscv-isa-manual/releases/download/20240411/unpriv-isa-asciidoc.pdf'
    dest=ROOT/'artifacts/E5/manual'
    for page in [42,47,50,57]:run('E5/manual/render_'+str(page),['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1500','-singlefile','-png',pdf,dest/('page_'+str(page))],inputs=[pdf])
    print('E5_DPI_PREFLIGHT_PASS',flush=True)
if __name__=='__main__':main()
