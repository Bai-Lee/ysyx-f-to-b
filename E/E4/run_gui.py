from common import *
run('gui/session',['xvfb-run','-a','-s','-screen 0 1600x1200x24 -nolisten tcp','python3',ROOT/'E/E4/gui_verify.py'],
    inputs=[ROOT/'E/E4/gui_verify.py',WORK/'build/lab_board/lab_board',NVBOARD/'example/build/top'],timeout=240)
