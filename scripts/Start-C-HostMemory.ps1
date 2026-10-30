$ErrorActionPreference = 'Stop'
$projectPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if ($projectPath -ne 'C:\YSYX_WORKSPACE\projects\ysyx_f_to_b') { throw 'Unexpected project path.' }
$pointerFile = Get-ChildItem (Join-Path $projectPath 'temp\host-memory') -Filter 'pointer-*.json' -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
if ($pointerFile) {
    $previousSample = Get-Content -Raw -LiteralPath $pointerFile.FullName | ConvertFrom-Json
    $streamFile = Get-Item -LiteralPath (Join-Path $projectPath $previousSample.stream) -ErrorAction SilentlyContinue
    $sampleAge = if ($streamFile) { ([DateTime]::UtcNow - $streamFile.LastWriteTimeUtc).TotalSeconds } else { 999999 }
    $previousProcess = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $previousSample.pid) -ErrorAction SilentlyContinue
    if ($sampleAge -lt 10 -and $previousProcess.CommandLine -like '*host_memory_monitor.py*') {
        Write-Output ('HOST_MEMORY_SAMPLER_REUSED pid=' + $previousSample.pid)
        exit 0
    }
}
$sessionStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfff')
$evidencePath = Join-Path $projectPath ('artifacts\C\host-memory-monitor\' + $sessionStamp)
[void][IO.Directory]::CreateDirectory($evidencePath)
$monitorPython = 'C:\YSYX_WORKSPACE\.venv\Scripts\pythonw.exe'
if (-not (Test-Path -LiteralPath $monitorPython)) { throw 'Existing project pythonw.exe is missing.' }
$monitorScript = Join-Path $PSScriptRoot 'host_memory_monitor.py'
$commandLine = '"' + $monitorPython + '" "' + $monitorScript + '" --session ' + $sessionStamp
$startup = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{ ShowWindow = [uint16]0 }
$created = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $commandLine; CurrentDirectory = $projectPath; ProcessStartupInformation = $startup }
if ($created.ReturnValue -ne 0) { throw ('Memory sampler creation failed: ' + $created.ReturnValue) }
$ownedProcess = Get-CimInstance Win32_Process -Filter ('ProcessId=' + $created.ProcessId)
@{pid=$created.ProcessId;parent_pid=$ownedProcess.ParentProcessId;command=$commandLine;utc=[DateTime]::UtcNow.ToString('o');scope='Task-local hidden bounded Windows process; not a service or scheduled task.'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidencePath 'launch.json') -Encoding utf8
Write-Output ('HOST_MEMORY_SAMPLER_STARTED pid=' + $created.ProcessId + ' session=' + $sessionStamp)
exit 0
