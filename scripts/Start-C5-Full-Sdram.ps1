$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if ($projectRoot -ne 'C:\YSYX_WORKSPACE\projects\ysyx_f_to_b') { throw 'Unexpected project root; inspect paths before launching.' }
& (Join-Path $PSScriptRoot 'Start-C-HostMemory.ps1')
if ($LASTEXITCODE -ne 0) { throw "Host memory sampler failed: $LASTEXITCODE" }
Start-Sleep -Seconds 2
& 'C:\Windows\System32\wsl.exe' -d YSYX-Linux -u ysyx -- python3 /workspace/projects/ysyx_f_to_b/C/C5/run_parallel_sdram_job.py --launch
if ($LASTEXITCODE -ne 0) { throw "Detached C5 launch failed: $LASTEXITCODE" }
