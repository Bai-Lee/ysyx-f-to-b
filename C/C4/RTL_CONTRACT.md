# C4 RTL integration contract

Owned by `c4_rtl`; parent owns simulation wrappers, C++ runner, synthesis and program suites. All ports are plain packed wires/logic, no SystemVerilog interfaces. All modules use `clock`, active-high synchronous `reset`, and 32-bit address/data. Current contract is fixed before implementation.

## Execution and architectural observation

`rv32e_execute` is the D RV32E implementation with additional inputs `advance` and `bus_fault[2:0]`. It changes architectural state only when `advance`; fault codes 1–4 retain D meaning and 5 denotes a failed bus response. Original `inst`, `mem_rdata`, `pc`, `mem_addr`, `mem_wdata`, `mem_size[2:0]`, `mem_ren`, `mem_wen`, `exec_valid`, `exec_ebreak`, `halted`, `fault[2:0]`, `commit_valid`, `commit_pc`, `commit_inst`, `commit_next_pc`, `debug_gpr[511:0]` remain. Parameters: `RESET_PC=0x80000000`, `FAULT_ADDI=0`.

Each public CPU top (`c4_simple_core`, `c4_axi_core`, `c4_axi_soc`) exports:

- `pc[31:0]`, `halted`, `fault[2:0]`.
- Post-edge `commit_valid`, `commit_pc[31:0]`, `commit_inst[31:0]`, `commit_next_pc[31:0]`, `debug_gpr[511:0]` (x0 in bits 31:0).
- Pre-edge `exec_fire`, `exec_pc[31:0]`, `exec_inst[31:0]`, `exec_ebreak`. Use these in a simulator-only posedge block for DPI notification; do not generate notifications for each waiting cycle.
- Pre-edge `exec_mem_valid`, `exec_mem_write`, `exec_mem_addr[31:0]` (logical byte address), `exec_mem_size[2:0]` (1/2/4), `exec_mem_wdata[31:0]` (unshifted rs2), `exec_mem_rdata[31:0]` (lane-extracted raw load). These are diagnostic observations; the host should independently check actual accepted bus transactions against the decoded instruction.
- `debug_state[2:0]`: 0 fetch request, 1 fetch response, 2 data request, 3 data response. Architectural PC/GPR remain stable while a response is awaited; LFSRs and device time may advance.

Reset directly gates externally visible bus VALID and UART tx_valid low, and its clock edge clears architectural state and pending ownership. Already accepted external writes are not rolled back. A simulator should reset connected slave state consistently and distinguish aborted pending operations from retired instructions.

## `c4_simple_core`

Parameters: `STAGE=4`, `RESET_PC`, `FAULT_ADDI`. Inputs `delay_enable[2:0]`, `lfsr_seed[31:0]` are configuration and must stay stable during a run; seed zero is replaced by a nonzero constant.

Instruction port (read only):

```text
out i_req_valid, i_req_addr[31:0]
in  i_req_ready
in  i_resp_valid, i_resp_data[31:0], i_resp_error[1:0]
out i_resp_ready
```

Data port:

```text
out d_req_valid, d_req_addr[31:0], d_req_write,
    d_req_wdata[31:0], d_req_wstrb[3:0]
in  d_req_ready
in  d_resp_valid, d_resp_data[31:0], d_resp_error[1:0]
out d_resp_ready
```

All requests use word-aligned bus addresses. Store payload is shifted into its byte lanes and WSTRB selects exactly the architectural bytes; a load extracts the appropriate lane before sign/zero extension. Error encoding is AXI-like (0 success, nonzero failure). There is one outstanding instruction and at most one data transaction; stores await a response too.

`STAGE=1`: one-cycle synchronous instruction backend, legacy combinational data backend. Data `ready=1`, and data response must be combinationally available for the request. A normal instruction, load or store takes two clocks from its fetch request to retirement.

`STAGE=2`: one-cycle synchronous instruction and data backends, ready tied high. ALU instructions take two clocks; loads/stores take three. The controller decodes the accepted instruction response directly and may issue its data request on that same edge.

`STAGE=3`: request/response VALID with variable response latency; ready tied high. `delay_enable[0]` delays IFU request issue through LFSR, bit 1 delays LSU request issue; backend separately supplies fixed 5/10/20 or its own LFSR latency.

`STAGE=4`: full independent ready/valid. Bits 0/1 still delay request initiation, bit 2 varies response READY. Once a request asserts VALID, its VALID and payload remain held until accepted. READY may vary before a response handshake.

No fixed-latency assumption is used by the correctness logic: early-stage environment restrictions are imposed by their test backends and identified in acceptance reports.

## AXI4-Lite modules

Every scalar AXI port uses the standard suffixes:

```text
awvalid, awready, awaddr[31:0], awprot[2:0]
wvalid, wready, wdata[31:0], wstrb[3:0]
bvalid, bready, bresp[1:0]
arvalid, arready, araddr[31:0], arprot[2:0]
rvalid, rready, rdata[31:0], rresp[1:0]
```

`simple_to_axil #(READ_ONLY=0, PROT=0)` takes `req_*`/`resp_*` (same data SimpleBus names without `d_`) and exposes scalar master `m_*`. A READ_ONLY instance ties AWVALID/WVALID/BREADY and write payloads to zero. A read-only write request returns SLVERR locally, never creates AXI write traffic. The IFU uses PROT=4, LSU PROT=0.

`axil_arbiter2` accepts scalar slave ports `s0_*` and `s1_*`, exposes scalar master `m_*`, plus `debug_busy`, `debug_owner`. A registered round-robin grant locks owner and read/write direction through the final response handshake. AW and W are accepted independently; no second source can steal a partial write.

`c4_axi_core` combines `c4_simple_core(STAGE=4)`, two adapters and arbiter. It exposes the shared CPU observation ports above, `delay_enable`, `lfsr_seed`, scalar external master `m_*`, and `debug_arb_busy`, `debug_arb_owner`. It contains no memory slave or DPI, and is the CPU+arbiter synthesis target.

`axil_xbar3` accepts scalar `s_*` and emits packed `m_*` for three targets. Target 0 occupies each least-significant lane, target 1 the middle, target 2 the highest. Valid/ready are `[2:0]`, address/data `[95:0]`, PROT `[8:0]`, WSTRB `[11:0]`, responses `[5:0]`. It buffers AR, AW and W independently before routing; each READY depends on registered state, not another channel current VALID. An already buffered AR is served before a new complete write pair; both same-edge requests are retained. Response target remains locked under backpressure. Unmapped accesses return DECERR with no downstream side effect.

Default map parameters: `RAM_BASE=0x80000000`, `RAM_BYTES=0x08000000` (128 MiB to preserve the accepted software EEI), UART 4 KiB at `0x10000000`, CLINT 4 KiB at `0x20000000`. The lecture's SRAM size is an example map; its synthesis-only two 256x32 memories are a separate baseline. Instruction PROT accesses outside RAM return DECERR, a fixed executable-region rule, not a complete PMP implementation.

`axil_uart` and `axil_clint` have scalar slave `s_*`. UART exports registered one-clock `tx_valid`, `tx_data[7:0]`: simulator-only code prints a character for that pulse. Offset 0 is TX (only WSTRB bit 0 causes a character), offset 4 returns ready=1; unknown registers or writes to ready return SLVERR. Zero-strobe TX is a no-op. CLINT exports `mtime[63:0]`, increments once per clock, parameter `MTIME_RESET=0` enables rollover fixtures. Offset 0 returns low and latches matching high; offset 4 consumes the latched high (or returns current high if no low preceded it). Writes return SLVERR. Clock-to-time conversion belongs to AM and the parent calibration experiment, not this RTL.

`c4_axi_soc` combines `c4_axi_core`, `axil_xbar3`, UART and CLINT. It exposes scalar external RAM master `mem_*`; all CPU observations/configuration; `uart_tx_valid`, `uart_tx_data[7:0]`, `mtime[63:0]`; and passive scalar `mon_*` taps of the shared master before Xbar (both directions, all channels) for independent host transaction validation. Parameters include `RESET_PC`, `FAULT_ADDI`, `RAM_BASE`, `RAM_BYTES`, `MTIME_RESET`.

All RTL remains synthesizable. Simulators/monitors and synthesis-only 2KB baseline memories are owned by the parent. Unit tests will explicitly cover AW-before-W, W-before-AW, simultaneous writes, stalled R/B stability, WSTRB, decode errors, reset, mtime rollover and meaningful wrong-design controls.
