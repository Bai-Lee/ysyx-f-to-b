set pagination off
shell while [ ! -f /home/USER/e3-lab/lcthw/attach.ready ]; do sleep 0.01; done
attach 32
break /workspace/projects/ysyx_f_to_b/E/E3/lcthw/solutions/continued/ex31_attach.c:13
continue
print i
set var i=200
print i
delete breakpoints
continue
quit
