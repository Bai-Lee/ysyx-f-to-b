from common import *
def main():
    tools=Path('/home/USER/tools/e-stage');ecc=tools/'ecos-alpha9/squashfs-root/resources/binaries/ecc';suite=tools/'oss-20261022/oss-cad-suite';parent=WORK/'backend';project=parent/'light_r_only';project.mkdir(exist_ok=True);(project/'rtl').mkdir(exist_ok=True)
    shutil.copyfile(parent/'light/rtl/light.v',project/'rtl/light.v')
    pdk=Path('/home/USER/tools/icsprout55-e-stage');root=pdk/'IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7CR'
    cfg=project/'ecc.toml';cfg.write_text('''[design]
name="light_r_only"
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
libs=["'''+str(root/'liberty/ics55_LLSC_H7CR_typ_tt_1p2_25_nldm.lib')+'''"]
lefs=["'''+str(root/'lef/ics55_LLSC_H7CR_ecos.lef')+'''"]
dont_use=["*AO222*","*2BB2*","*AOI222*","*AOI33*","*OA222*","*OAI222*","*OAI33*","*NOR4*"]
''')
    env={'PATH':str(suite/'bin')+':'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
    run('E/backend/light_single_lib',[ecc,'run','--project',project,'--plain'],inputs=[ecc,cfg,project/'rtl/light.v'],cwd=parent,env=env,timeout=1200)
    print('SINGLE_LIBRARY_PREFLIGHT_DONE',flush=True)
if __name__=='__main__':main()
