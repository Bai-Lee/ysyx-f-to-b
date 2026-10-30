param([switch]$Archive, [switch]$Shallow)
$ErrorActionPreference = 'Stop'
$projectPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pythonPath = 'C:\YSYX_WORKSPACE\.venv\Scripts\python.exe'
$verifyArguments = @('-X','utf8',(Join-Path $PSScriptRoot 'verify_B_delivery.py'),'--final')
if (-not $Shallow) { $verifyArguments += '--deep' }
if ($Archive) { $verifyArguments += @('--archive',(Join-Path $projectPath 'YSYX_B_DELIVERY.zip')) }
& $pythonPath @verifyArguments
if ($LASTEXITCODE -ne 0) { throw 'B evidence verification failed. See the specific diagnostic above.' }
