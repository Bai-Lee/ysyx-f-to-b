param([switch]$External, [string]$Archive)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = 'C:\YSYX_WORKSPACE\.venv\Scripts\python.exe'
$verifyArgs = @('-X', 'utf8', (Join-Path $PSScriptRoot 'verify_E_delivery.py'))
if ($External) { $verifyArgs += '--external' }
if ($Archive) { $verifyArgs += @('--archive', $Archive) }
& $pythonPath @verifyArgs
if ($LASTEXITCODE -ne 0) { throw "E evidence verification failed: $LASTEXITCODE" }
