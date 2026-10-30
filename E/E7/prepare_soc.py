from common7 import *
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 p=ROOT/'E/E7';run('E7/light_soc/translate',['python3',p/'build.py','--mode','soc','--prepare-only'],inputs=[p/'build.py'],timeout=100)
 run('E7/light_soc/cpp_syntax',['g++','-std=c++17','-fsyntax-only','-I'+str(WORK/'build/E7/soc'),'-I'+str(VROOT/'include'),'-I'+str(VROOT/'include/vltstd'),'-I'+str(ROOT/'E/runtime'),p/'soc_runner.cpp'],inputs=[p/'soc_runner.cpp'],timeout=40)
 print('SOC_TRANSLATION_AND_CPP_SYNTAX_PASS_NOT_LINKED',flush=True)
if __name__=='__main__':main()
