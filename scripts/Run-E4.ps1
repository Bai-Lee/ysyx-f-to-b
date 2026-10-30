param([switch]$Replay,[switch]$SkipPackage)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython=Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$sciencePython=Join-Path $workspaceRoot '.venv\Scripts\python.exe'
$env:PYTHONUTF8='1'
function Invoke-LinuxE4([string]$name,[string[]]$extra=@()) {
    & wsl.exe -d YSYX-Linux -u ysyx --exec python3 ('/workspace/projects/ysyx_f_to_b/E/E4/'+$name) @extra
    if ($LASTEXITCODE -ne 0) { throw "E4 failed: $name" }
}
Push-Location $taskRoot
try {
    $status=Get-Content -LiteralPath config\task_status.json -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($status.current_stage -ne 'E4') { throw 'E4 is a historical checkpoint; do not overwrite a later stage ledger.' }
    if ($Replay) {
        $free=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
        if ($free -lt (3*1024*1024)) { throw 'RESOURCE_LIMIT: less than3GiB host memory; no new heavy job started.' }
        Invoke-LinuxE4 'verify_runtime.py'
        Invoke-LinuxE4 'run_basic.py'
        Invoke-LinuxE4 'run_units.py' @('--fresh')
        Invoke-LinuxE4 'run_cpu.py'
        Invoke-LinuxE4 'build_board.py'
        Invoke-LinuxE4 'run_gui.py'
        & $sciencePython scripts\check_E4_visual.py
        if ($LASTEXITCODE -ne 0) { throw 'Rendered pixel validation failed.' }
        Invoke-LinuxE4 'run_negative.py'
        Invoke-LinuxE4 'run_fourstate.py'
        Invoke-LinuxE4 'verify_waves.py'
        Invoke-LinuxE4 'verify_rom.py'
        & .\scripts\Run-E4-Structure.ps1
        Invoke-LinuxE4 'verify_offline.py'
        Invoke-LinuxE4 'verify_runtime.py'
    }
    & $taskPython scripts\finalize_E4.py
    if ($LASTEXITCODE -ne 0) { throw 'E4 evidence audit failed.' }
    & $taskPython scripts\check_E4_delivery.py
    if ($LASTEXITCODE -ne 0) { throw 'E4 document/source check failed.' }
    if (-not $SkipPackage) {
        & $taskPython scripts\package_delivery.py --label E4
        if ($LASTEXITCODE -ne 0) { throw 'E4 ZIP verification failed.' }
    }
} finally { Pop-Location }
