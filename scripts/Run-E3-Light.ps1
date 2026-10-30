param()
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython=Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$currentPolicy=Get-Content -LiteralPath (Join-Path $taskRoot 'config\execution_policy.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $currentPolicy.temporary_resource_limit.active) { throw 'Historical 1GB checkpoint is superseded. Use scripts\Run-E3.ps1.' }
$taskBudget=Get-Content -LiteralPath (Join-Path $taskRoot 'reports\E3_low_memory_budget.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskBudget.temporary_memory_gib -ne 1) { throw 'Review the current resource authorization first.' }
$env:PYTHONIOENCODING='utf-8'
function Invoke-E3Small([string]$TaskFile) {
    $taskAvailableKiB=(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
    if ($taskAvailableKiB -lt (768*1024)) { throw 'RESOURCE_LIMIT: less than768MiB free; no new test process started.' }
    & $taskPython (Join-Path $PSScriptRoot $TaskFile)
    if ($LASTEXITCODE -ne 0) { throw "E3 light test failed: $TaskFile" }
}
Invoke-E3Small 'verify_E3_tools.py'
Invoke-E3Small 'e3\lct_early.py'
Invoke-E3Small 'e3\lct_early_extra.py'
Invoke-E3Small 'e3\lct_editor.py'
Invoke-E3Small 'e3\lct_arrays.py'
Invoke-E3Small 'e3\lct_literals.py'
Invoke-E3Small 'e3\build_xxd.py'
Invoke-E3Small 'finalize_E3_light.py'
