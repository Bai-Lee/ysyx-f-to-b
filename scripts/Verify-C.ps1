param([switch]$External, [string]$Archive)
$ErrorActionPreference = 'Stop'
$pythonPath = 'C:\YSYX_WORKSPACE\.venv\Scripts\python.exe'
$verifyArgs = @('-X', 'utf8', (Join-Path $PSScriptRoot 'verify_C_delivery.py'))
if ($External) { $verifyArgs += '--external' }
if ($Archive) { $verifyArgs += @('--archive', $Archive) }
& $pythonPath @verifyArgs
if ($LASTEXITCODE -ne 0) { throw "C evidence verification failed: $LASTEXITCODE" }
