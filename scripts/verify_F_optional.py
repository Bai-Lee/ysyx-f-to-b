from evidence import *
def main():
    src=ROOT/'F/rtl/optional_logic.sv';tb=ROOT/'F/testbenches/optional_logic.sv';tb.write_text('''module tb;
reg[15:0]in;wire v;wire[3:0]code;wire[4:0]clz,ctz,clo,cto;
reg a,b,ci;wire s,c;integer n,k,hi,lz,tz,lo,to,found,checks=0;
priority16 enc(in,v,code);count_ends16 counts(in,clz,ctz,clo,cto);fa_two_halves adder(a,b,ci,s,c);
initial begin
for(n=0;n<65536;n=n+1)begin
in=n;hi=0;for(k=0;k<16;k=k+1)if((n>>k)&1)hi=k;
lz=0;found=0;for(k=15;k>=0;k=k-1)begin if(!found&&((n>>k)&1)==0)lz=lz+1;else found=1;end
tz=0;found=0;for(k=0;k<16;k=k+1)begin if(!found&&((n>>k)&1)==0)tz=tz+1;else found=1;end
lo=0;found=0;for(k=15;k>=0;k=k-1)begin if(!found&&((n>>k)&1)==1)lo=lo+1;else found=1;end
to=0;found=0;for(k=0;k<16;k=k+1)begin if(!found&&((n>>k)&1)==1)to=to+1;else found=1;end
#1;if(v!==(n!=0)||code!==hi[3:0]||clz!==lz[4:0]||ctz!==tz[4:0]||clo!==lo[4:0]||cto!==to[4:0])$fatal(1,"priority/count n=%0h",n);
checks=checks+1;end
for(n=0;n<8;n=n+1)begin a=(n>>2)&1;b=(n>>1)&1;ci=n&1;#1;if({c,s}!==({1'b0,a}+{1'b0,b}+{1'b0,ci}))$fatal(1,"half adder hierarchy");end
$display("PASS OPTIONAL priority/count=65536 half-adder=8");$finish;end endmodule
''',encoding='utf8')
    exe=ROOT/'temp/optional_logic.vvp';iver=Path(r'C:\YSYX_WORKSPACE\tools\oss-cad-suite-20261022\oss-cad-suite\bin\iverilog.exe');vvp=iver.with_name('vvp.exe')
    a=run('F/optional_compile',[iver,'-g2012','-Wall','-s','tb','-o',exe,src,tb],[src,tb],timeout=30)
    b=run('F/optional_logic',[vvp,exe],[src,tb,exe],timeout=40)
    report={'status':'PASS' if a['status']==b['status']=='PASS' else 'FAIL','compile':a,'simulation':b,'priority_and_count_cases':65536,'full_adder_cases':8,'tasks':['F3-O011','F3-O012','F3-O013'],'method':'User-authorized RTL alternative; priority16 instantiates four group priority4 encoders and one group selector; all 16-bit inputs exhaustively checked'}
    dump(ROOT/'reports/F_optional_results.json',report);print('F_OPTIONAL_RESULT',report['status'],flush=True);return 0 if report['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
