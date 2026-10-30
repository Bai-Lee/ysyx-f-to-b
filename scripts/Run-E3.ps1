param([switch]$VerifyOffline,[switch]$SkipPackage)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython=Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$env:PYTHONUTF8='1'
Push-Location $taskRoot
try {
    if ($VerifyOffline) {
        $availableKiB=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
        if ($availableKiB -lt (3*1024*1024)) { throw 'RESOURCE_LIMIT: less than3GiB host memory; offline compilation not started.' }
        & wsl.exe -d YSYX-Linux -u ysyx --exec python3 /workspace/projects/ysyx_f_to_b/E/E3/verify_offline.py
        if ($LASTEXITCODE -ne 0) { throw 'Offline E3 verification failed.' }
    }
    & wsl.exe -d YSYX-Linux -u ysyx --exec python3 /workspace/projects/ysyx_f_to_b/E/E3/recover_input_snapshots.py
    if ($LASTEXITCODE -ne 0) { throw 'Evidence input snapshot verification failed.' }
    & $taskPython (Join-Path $PSScriptRoot 'finalize_E3.py')
    if ($LASTEXITCODE -ne 0) { throw 'E3 audit failed.' }
    & $taskPython (Join-Path $PSScriptRoot 'check_E3_delivery.py')
    if ($LASTEXITCODE -ne 0) { throw 'E3 content/link validation failed.' }
    if (-not $SkipPackage) {
        & $taskPython (Join-Path $PSScriptRoot 'package_delivery.py') --label E3
        if ($LASTEXITCODE -ne 0) { throw 'E3 ZIP verification failed.' }
    }
} finally { Pop-Location }
