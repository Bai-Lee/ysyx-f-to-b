let @q=join([':g#</\?people>#d',':%s#<person>#{#g',':%s#</person>#},#g',':%s#<name>\(.*\)</name>#\=''"name": ''.json_encode(submatch(1)).'',''#',':%s#<email>\(.*\)</email>#\=''"email": ''.json_encode(submatch(1))#',':$s/},/}/'], "\<CR>")."\<CR>"
normal! @q
call append(0,"[")
call append(line("$"),"]")
wq
