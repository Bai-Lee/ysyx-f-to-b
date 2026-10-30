#!/bin/bash
set -euo pipefail
test "$(id -u)" -eq 0
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends g++-riscv64-linux-gnu python-is-python3 libreadline-dev libelf-dev bsdextrautils poppler-utils time parallel python3-numpy libsdl2-dev libsdl2-image-dev pulseaudio-utils
