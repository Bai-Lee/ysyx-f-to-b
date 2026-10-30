#!/bin/bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
export LC_ALL=C
if ! id ysyx >/dev/null 2>&1; then
    useradd --create-home --shell /bin/bash ysyx
fi
apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=20 -o APT::Update::Error-Mode=any update
apt-get -y --no-install-recommends install build-essential gdb valgrind man-db manpages-dev zip unzip ripgrep openssh-server wamerican time pkg-config
dpkg-query -W -f='${Package}\t${Version}\n' gcc g++ make gdb valgrind git vim tmux curl python3 zip unzip ripgrep openssh-server wamerican
install -d -o ysyx -g ysyx /home/USER/e3-lab /home/USER/build
