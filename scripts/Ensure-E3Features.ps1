# Run elevated only after the direct user authorization recorded in config.
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$taskAuth=Get-Content -LiteralPath (Join-Path $taskRoot 'config\E3_authorization.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskAuth.authorized_actions -notcontains 'Update/install WSL2 kernel and necessary components') { throw 'User authorization missing.' }
try {
$taskRows=@()
foreach ($taskFeature in @('Microsoft-Windows-Subsystem-Linux','VirtualMachinePlatform')) {
    $taskBefore=Get-WindowsOptionalFeature -Online -FeatureName $taskFeature
    $taskRow=@{feature=$taskFeature;before=$taskBefore.State.ToString();changed=$false;restart_needed=$false}
    if ($taskBefore.State -eq 'Disabled') {
        $taskChange=Enable-WindowsOptionalFeature -Online -FeatureName $taskFeature -All -NoRestart
        $taskRow.changed=$true;$taskRow.restart_needed=[bool]$taskChange.RestartNeeded
    }
    $taskAfter=Get-WindowsOptionalFeature -Online -FeatureName $taskFeature
    $taskRow.after=$taskAfter.State.ToString();$taskRows+=$taskRow
}
$taskResult=@{timestamp=[DateTime]::UtcNow.ToString('o');features=$taskRows;automatic_reboot=$false}
$taskResult | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskRoot 'reports\E3_windows_features.json') -Encoding utf8
if ($taskRows | Where-Object { $_.after -notin @('Enabled','EnablePending') }) { exit 1 }
} catch {
    @{status='FAIL';error=$_.Exception.Message;details=$_.ScriptStackTrace} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskRoot 'reports\E3_windows_features.json') -Encoding utf8
    exit 1
}
