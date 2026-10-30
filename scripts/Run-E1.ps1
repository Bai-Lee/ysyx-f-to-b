param()
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython=Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$taskEnvironment=Join-Path $workspaceRoot 'tools\oss-cad-suite-20261022\oss-cad-suite\environment.ps1'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Existing archive Python environment is required.' }
. $taskEnvironment
$env:PYTHONIOENCODING='utf-8'
function Invoke-E1Python([string]$TaskFile,[string[]]$TaskArgs=@()) {
    & $taskPython (Join-Path $PSScriptRoot ('e1\'+$TaskFile)) @TaskArgs
    if ($LASTEXITCODE -ne 0) { throw "E1 failed: $TaskFile (exit $LASTEXITCODE)" }
}
# Reuse the frozen scope. prepare_E1.py is deliberately not rerun: it also records a resume transition.
Invoke-E1Python 'build_comb.py'
Invoke-E1Python 'build_seq.py'
Invoke-E1Python 'build_fsm_core.py'
Invoke-E1Python 'build_fsm_exam.py'
Invoke-E1Python 'run.py' @('--all','--controls')
Invoke-E1Python 'check_structure.py'
Invoke-E1Python 'check_faults.py'
Invoke-E1Python 'export_schematic.py'
Invoke-E1Python 'finalize.py'
