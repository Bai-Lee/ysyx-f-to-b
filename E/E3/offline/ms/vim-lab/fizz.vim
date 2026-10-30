2s/range(limit)/range(1, limit+1)/
4s/print('fizz')/print('fizz', end='')/
6s/print('fizz')/print('buzz', end='')/
call append(8, ['        else:', '            print()'])
%s/fizz_buzz(10)/fizz_buzz(int(sys.argv[1]))/
call append(0, ['import sys', ''])
call append(line('$'), ['', 'if __name__ == "__main__":', '    main()'])
wq
