set nocompatible nomore
set undolevels=1000
enew!
call setline(1, ["alpha beta gamma"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0dw"
call assert_equal(["beta gamma"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0x"
call assert_equal(["bc"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0iX\<Esc>"
call assert_equal(["Xabc"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! A!\<Esc>"
call assert_equal(["abc!"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0rZ"
call assert_equal(["Zbc"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0cwXYZ\<Esc>"
call assert_equal(["XYZ"], getline(1,"$"))
enew!
call setline(1, ["one", "two", "three"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggdd"
call assert_equal(["two", "three"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggyyGp"
call assert_equal(["one", "two", "one"], getline(1,"$"))
enew!
call setline(1, ["one", "two", "three"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggddGp"
call assert_equal(["two", "three", "one"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggddu"
call assert_equal(["one", "two"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggddu\<C-r>"
call assert_equal(["two"], getline(1,"$"))
enew!
call setline(1, ["abc"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0d$"
call assert_equal([""], getline(1,"$"))
enew!
call setline(1, ["alpha beta"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0/beta\<CR>cwB\<Esc>"
call assert_equal(["alpha B"], getline(1,"$"))
enew!
call setline(1, ["call(old)"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0f(ci(XYZ\<Esc>"
call assert_equal(["call(XYZ)"], getline(1,"$"))
enew!
call setline(1, ["abcd"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0vld"
call assert_equal(["cd"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggJ"
call assert_equal(["one two"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggonew\<Esc>"
call assert_equal(["one", "new", "two"], getline(1,"$"))
enew!
call setline(1, ["one", "two"])
normal! gg0
let &undolevels=&undolevels
execute "normal! ggOhead\<Esc>"
call assert_equal(["head", "one", "two"], getline(1,"$"))
enew!
call setline(1, ["abcd"])
normal! gg0
let &undolevels=&undolevels
execute "normal! 0RXZ\<Esc>"
call assert_equal(["XZcd"], getline(1,"$"))
enew!
call setline(1, ["foo foo","foo"])
%s/foo/bar/g
call assert_equal(["bar bar","bar"],getline(1,"$"))
normal! gg$
call assert_equal(7,col("."))
normal! ggG
call assert_equal(2,line("."))
enew!
call setline(1, "(a[b]c)")
normal! 0%
call assert_equal(7,col("."))
set ignorecase
call assert_equal(1, &ignorecase)
help motion
call assert_equal("help",&buftype)
call writefile(v:errors,"/home/USER/e3-lab/missing-semester/vim-lab/tutor-errors.json")
if len(v:errors) | cquit 1 | endif
qa!
