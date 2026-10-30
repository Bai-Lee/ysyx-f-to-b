from common7 import *
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 run('E7/light_gui/build',['python3',ROOT/'E/E7/build.py','--mode','soc_gui'],inputs=[ROOT/'E/E7/build.py',ROOT/'E/E7/constr/soc.nxdc'],timeout=240)
 print('NVBOARD_SOC_BINARY_BUILT_NOT_YET_INTERACTED',flush=True)
if __name__=='__main__':main()
