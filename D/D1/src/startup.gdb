set pagination off
set confirm off
set backtrace past-main on
set backtrace past-entry on
starti
x/i $pc
break _start
continue
bt
x/8i $pc
break *main
continue
bt
set $main_return = *(void **)$rsp
tbreak *$main_return
continue
x/i $pc
bt
catch syscall exit_group
continue
bt
continue
quit
