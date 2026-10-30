param([switch]$Quick,[switch]$Full,[switch]$Online)
$ErrorActionPreference = 'Stop'
if ($Quick -and $Full) { throw 'Choose Quick or Full, not both.' }
$taskRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython = Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$taskEnvironment = Join-Path $workspaceRoot 'tools\oss-cad-suite-20261022\oss-cad-suite\environment.ps1'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'The existing archive Python environment is required.' }
. $taskEnvironment
$env:PYTHONIOENCODING='utf-8'
function Invoke-FPython([string]$TaskFile,[string[]]$TaskArgs=@()) {
    & $taskPython (Join-Path $PSScriptRoot $TaskFile) @TaskArgs
    if ($LASTEXITCODE -ne 0) { throw "F verification failed: $TaskFile (exit $LASTEXITCODE)" }
}
# Only F tests are called. This entry point never launches GUI or enters E.
if ($Full) { Invoke-FPython 'run_F_circuits.py' @('--batch') }
Invoke-FPython 'verify_F_cpu.py'
Invoke-FPython 'verify_F_theory.py'
Invoke-FPython 'verify_F_optional.py'
if ($Full) { Invoke-FPython 'verify_F2_methods.py' }
if ($Online) { Invoke-FPython 'verify_F4.py' }
Invoke-FPython 'finalize_F.py'
Invoke-FPython 'verify_F_stage.py'
