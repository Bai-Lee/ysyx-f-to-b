from common import *
def main():
    tools=Path('/home/USER/tools/e-stage');ecc=tools/'ecc-alpha10/ecc';suite=tools/'oss-20261022/oss-cad-suite';pdk=Path('/home/USER/tools/icsprout55-e-stage')
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    patch=pdk/'patch/icg.diff';marker=pdk/'.ysyx-icg-patch.json'
    if not marker.exists():
        o,e,r=run('E/backend/pdk_patch_check',['patch','--dry-run','--batch','--forward','-p0','-i',patch],cwd=pdk,inputs=[patch],expected=(0,1),timeout=180)
        if r['exit_code']==0:run('E/backend/pdk_patch',['patch','--batch','--forward','-p0','-i',patch],cwd=pdk,inputs=[patch],timeout=180);mode='applied'
        else:
            run('E/backend/pdk_patch_reverse_check',['patch','--dry-run','--batch','-R','-p0','-i',patch],cwd=pdk,inputs=[patch],timeout=180);mode='already_applied'
        dump(marker,{'mode':mode,'patch_sha256':sha(patch)})
    base=WORK/'backend';base.mkdir(exist_ok=True)
    project=base/'light'
    if not project.exists():run('E/backend/init_light',[ecc,'init','light','--plain'],cwd=base,env=env)
    rtl=project/'rtl/light.v';rtl.parent.mkdir(exist_ok=True)
    rtl.write_text('''module light(input clock,reset,output reg[15:0]led);
reg[31:0] count;
always @(posedge clock)begin
 if(reset)begin led<=16'd1;count<=0;end
 else begin if(count==0)led<={led[14:0],led[15]};count<=(count==32'd5000000)?32'd0:count+32'd1;end
end endmodule
''')
    libs=[];lefs=[]
    for k in ['R','L']:
        d=pdk/('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+k)
        libs.append(str(d/'liberty'/('ics55_LLSC_H7C'+k+'_typ_tt_1p2_25_nldm.lib')))
        lefs.append(str(d/'lef'/('ics55_LLSC_H7C'+k+'_ecos.lef')))
    config=project/'ecc.toml';config.write_text('''[design]
name="light"
top="light"
rtl=["rtl/light.v"]
clock_port="clock"
frequency_mhz=100.0
[pdk]
name="ics55"
root="'''+str(pdk)+'''"
[flow]
preset="syn_sta"
run="baseline"
[pdk.overrides]
libs='''+json.dumps(libs)+'''
lefs='''+json.dumps(lefs)+'''
dont_use=["*AO222*","*2BB2*","*AOI222*","*AOI33*","*OA222*","*OAI222*","*OAI33*","*NOR4*"]
''')
    run('E/backend/check_light',[ecc,'check','--project',project],cwd=base,inputs=[config,rtl],env=env,timeout=180)
    run('E/backend/light_synthesis',[ecc,'run','--project',project,'--plain','--overwrite'],cwd=base,inputs=[config,rtl],env=env,timeout=1200)
    dump(ROOT/'reports/E_backend_preflight.json',{'status':'SYNTHESIS_EXECUTED_REPORT_AUDIT_PENDING','project':str(project),'ecc':str(ecc),'yosys':str(suite/'bin/yosys'),'pdk':str(pdk),'library_sha256':[{'path':x,'sha256':sha(x)} for x in libs]})
    print('BACKEND_PREFLIGHT_SYNTHESIS_DONE',flush=True)
if __name__=='__main__':main()
