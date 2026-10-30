from common7 import *
def main():
 q=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=BENCH7,capture_output=True)
 if q.returncode==0:print('TRACER_BASE_ALREADY_PRESENT',q.stdout.decode().strip());return
 run('E7/setup/stage_baseline',['git','add','.gitignore','Makefile','AGENTS.md','npc'],cwd=BENCH7)
 run('E7/setup/baseline_commit',['git','commit','-m','Initialize isolated E7 autonomous engineering baseline; no student identity claimed'],cwd=BENCH7)
 print('E7_TRACER_BASE_READY',flush=True)
if __name__=='__main__':main()
