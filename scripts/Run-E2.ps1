param([switch]$Online)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskPython=Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe'
$env:PYTHONIOENCODING='utf-8'
$taskArguments=@()
if ($Online) { $taskArguments+= '--online' }
& $taskPython (Join-Path $PSScriptRoot 'verify_E2.py') @taskArguments
if ($LASTEXITCODE -ne 0) { throw 'E2 verification failed.' }
& $taskPython (Join-Path $PSScriptRoot 'finalize_E2.py')
if ($LASTEXITCODE -ne 0) { throw 'E2 audit failed. If source changed, use -Online to obtain new remote evidence.' }
