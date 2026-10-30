#!/bin/bash
set -euo pipefail
repo_dir=$(cd -- "$(dirname -- "$0")" && pwd)
target_dir=$1
test -d "$target_dir"
for name in bashrc profile bash_logout vimrc gitconfig gitignore_global bash_extra; do
 target="$target_dir/.$name"
 if [ -e "$target" ] || [ -L "$target" ]; then
  if [ "$(readlink -f "$target")" != "$repo_dir/$name" ]; then
   backup_dir="$target_dir/.dotfile-backups/$(date +%Y%m%dT%H%M%S%N)"
   mkdir -p "$backup_dir"
   mv -- "$target" "$backup_dir/.$name"
   ln -s "$repo_dir/$name" "$target"
  fi
 else
  ln -s "$repo_dir/$name" "$target"
 fi
done
