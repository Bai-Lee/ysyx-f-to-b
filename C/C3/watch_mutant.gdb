set pagination off
set confirm off
set disable-randomization off
break sum_sequence
run
watch running_total
continue
continue
continue
set $prefix_before = running_total
continue
printf "FIRST_BAD_PREFIX=%d INDEX=%zu DELTA=%d\n", running_total, i, running_total - $prefix_before
bt
disassemble /s sum_sequence
disable 2
continue
bt
quit
