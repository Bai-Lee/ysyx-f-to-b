#!/bin/bash
set -euo pipefail
export LC_ALL=C
task_source_list=/etc/apt/sources.list.d/ysyx-source.list
task_source_draft=$(mktemp /tmp/ysyx-sources.XXXXXX)
awk '$1=="deb" {$1="deb-src"; print}' /etc/apt/sources.list > "$task_source_draft"
test -s "$task_source_draft"
if [ -e "$task_source_list" ]; then
    cmp "$task_source_draft" "$task_source_list"
else
    install -m 644 "$task_source_draft" "$task_source_list"
fi
rm -f "$task_source_draft"
apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=20 -o APT::Update::Error-Mode=any update
