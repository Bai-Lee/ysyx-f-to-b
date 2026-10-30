$ErrorActionPreference='Stop'
$workspaceRoot=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
. (Join-Path $workspaceRoot 'tools\oss-cad-suite-20261022\oss-cad-suite\environment.ps1')
$env:PYTHONUTF8='1'
& (Join-Path $workspaceRoot 'YSYX_F_B_Archive\.venv\Scripts\python.exe') (Join-Path $PSScriptRoot 'check_E4_structure.py')
if ($LASTEXITCODE -ne 0) { throw 'E4 structural checks failed.' }
