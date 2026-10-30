#!/bin/bash
set -euo pipefail
test "$(id -u)" -eq 0
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends autoconf flex bison help2man zlib1g-dev liblz4-dev libfl-dev libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev xvfb xauth xdotool scrot gtkwave iverilog
