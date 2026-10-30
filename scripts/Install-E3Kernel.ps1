$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$workspaceRoot=Split-Path -Parent (Split-Path -Parent $taskRoot)
$taskAuthorization=Get-Content -LiteralPath (Join-Path $taskRoot 'config\E3_authorization.json') -Raw | ConvertFrom-Json
if ($taskAuthorization.answer -ne '授权安装和上述资源配置') { throw 'User authorization is required.' }
$taskPackage=Join-Path $workspaceRoot 'downloads\ysyx_e3\wsl_update_x64.msi'
$taskSignature=Get-AuthenticodeSignature -LiteralPath $taskPackage
if ($taskSignature.Status -ne 'Valid' -or $taskSignature.SignerCertificate.Subject -notlike 'CN=Microsoft Corporation,*') { throw 'Microsoft Authenticode signature check failed.' }
$taskLogDir=Join-Path $taskRoot 'artifacts\E3\kernel_msi'
New-Item -ItemType Directory -Path $taskLogDir -Force | Out-Null
$taskStamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfff')
$taskLog=Join-Path $taskLogDir ('install_'+$taskStamp+'.log')
$taskRecord=Join-Path $taskLogDir ('result_'+$taskStamp+'.json')
$taskArguments=@('/i',('"'+$taskPackage+'"'),'/qn','/norestart','REBOOT=ReallySuppress','/L*v',('"'+$taskLog+'"'))
$taskData=@{ timestamp=[DateTime]::UtcNow.ToString('o'); package=$taskPackage; sha256=(Get-FileHash -LiteralPath $taskPackage -Algorithm SHA256).Hash.ToLower(); signature='Valid'; signer=$taskSignature.SignerCertificate.Subject; log=$taskLog; arguments=$taskArguments; status='STARTING_AUTHORIZED_ELEVATION'; automatic_reboot=$false }
$taskData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskRecord -Encoding utf8
try {
    $taskProcess=Start-Process -FilePath (Join-Path $env:WINDIR 'System32\msiexec.exe') -ArgumentList $taskArguments -Verb RunAs -WindowStyle Hidden -Wait -PassThru
    $taskData.exit_code=$taskProcess.ExitCode
    $taskData.status=if ($taskProcess.ExitCode -eq 0) { 'INSTALLER_PASS_CHECK_REQUIRED' } elseif ($taskProcess.ExitCode -eq 3010) { 'RESTART_REQUIRED_NOT_PERFORMED' } else { 'FAIL' }
} catch {
    $taskData.status='ELEVATION_OR_INSTALL_FAILED';$taskData.error=$_.Exception.Message
}
$taskData.finished=[DateTime]::UtcNow.ToString('o')
$taskData | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskRecord -Encoding utf8
$taskData | ConvertTo-Json -Depth 5 -Compress
if ($taskData.status -notin @('INSTALLER_PASS_CHECK_REQUIRED','RESTART_REQUIRED_NOT_PERFORMED')) { exit 1 }
