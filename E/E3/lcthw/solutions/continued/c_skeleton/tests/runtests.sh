#!/bin/sh
set -eu
found=0
for test_file in tests/*_tests; do
 if [ -f "$test_file" ]; then
  found=1
  if "$test_file" 2>>tests/tests.log; then printf '%s PASS\n' "$test_file"; else tail tests/tests.log; exit 1; fi
 fi
done
test "$found" -eq 1
