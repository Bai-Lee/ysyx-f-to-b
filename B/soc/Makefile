PYTHON ?= python3
HERE := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PROFILE ?= b5-release
SIZE ?= train
FREQUENCY_MHZ ?= 325
PADDING ?= 24
PERF_TRACE ?= 0
NETLIST ?= $(HERE)/../B5/netlist/ysyx_00000000.v
CELLS ?= $(HERE)/../models/nangate45/sim/cells.v

.PHONY: verilog sim sim-iverilog sim-iverilog-netlist perf perf-test build-release build-baseline
verilog:
	$(PYTHON) $(HERE)/../B5/export.py
sim:
	$(PYTHON) $(HERE)/../B4/verify_soc.py
sim-iverilog: verilog
	@test -n "$(IMG)" || { echo 'IMG must name a standalone AM .bin file'; exit 2; }
	$(PYTHON) $(HERE)/../B5/public_sim.py --image "$(IMG)"
sim-iverilog-netlist:
	@test -n "$(IMG)" || { echo 'IMG must name a standalone AM .bin file'; exit 2; }
	$(PYTHON) $(HERE)/../B5/public_sim.py --image "$(IMG)" --netlist "$(NETLIST)" --cells "$(CELLS)"
perf:
	$(PYTHON) $(HERE)/../B3/perf.py --variant $(PROFILE) --size $(SIZE) --frequency-mhz $(FREQUENCY_MHZ) --padding $(PADDING) $(if $(filter 1,$(PERF_TRACE)),--trace,)
perf-test:
	$(MAKE) perf SIZE=test PERF_TRACE=1
build-release:
	$(PYTHON) $(HERE)/build_soc.py --reset 0x30000000 --cycle-sim --psram-qpi --psram-bytes 4194304 --sdram-width 32 --sdram-ranks 2 --optimized --label b5-release --apb-ratio-q 832 --axi-sdram --axi-ratio-q 832 --cache-lines 4 --cache-words 8 --cache-ways 2 --cache-burst --pipeline --forward --predict-jal --stream-fetch
build-baseline:
	$(PYTHON) $(HERE)/build_soc.py --reset 0x30000000 --cycle-sim --psram-qpi --psram-bytes 4194304 --sdram-width 32 --sdram-ranks 2 --optimized --label b3-uncached-unscaled --apb-ratio-q 256
	$(PYTHON) $(HERE)/build_soc.py --reset 0x30000000 --cycle-sim --psram-qpi --psram-bytes 4194304 --sdram-width 32 --sdram-ranks 2 --optimized --label b3-uncached-calibrated --apb-ratio-q 1024
