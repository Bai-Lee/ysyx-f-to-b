from common7 import *
from software_soc import SOFT
def main():
 am=SOFT/'abstract-machine';rows=[]
 make=(am/'Makefile').read_text();assert '-D__PLATFORM_$(shell echo $(PLATFORM) | tr a-z A-Z | tr - _) ' in make
 for n in ['trm.c','timer.c']:
  f=am/'am/src/riscv/npc'/n;old=f.read_text();new=old.replace('__PLATFORM_YSYXSOC__','__PLATFORM_YSYXSOC');save=ROOT/'E/E7/upstream'/('soc_before_macro_fix_'+n)
  if not save.exists():save.write_text(old)
  f.write_text(new);rows.append({'file':str(f),'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':sha(f)})
 dump(ROOT/'reports/E7_soc_platform_macro.json',{'status':'FIXED_REBUILD_REQUIRED','files':rows,'reason':'AM Makefile appendsdoubleunderscore to ISA macros but not PLATFORM macros. Authored conditional incorrectly used a trailingdoubleunderscore. Correcting it enables actualUART16550initialization,8MiBheapandSoCfrequencybranch. Active standaloneworkbench untouched.'})
 print('SOC_PLATFORM_MACRO_CORRECTED',flush=True)
if __name__=='__main__':main()
