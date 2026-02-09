# Pulsareon Guardian
$ErrorActionPreference = "SilentlyContinue"
$CLI_PATH = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64\cli-proxy-api.exe"
$CLI_DIR = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64"

function Log {
    param($m)
    $t = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$t] $m"
    "[$t] $m" | Out-File "E:\PulsareonThinker\logs\guardian.log" -Append -Encoding utf8
}

Log "Guardian started."

while ($true) {
    # Check CLI
    $cli = Get-Process -Name "cli-proxy-api" -ErrorAction SilentlyContinue
    if (-not $cli) {
        Log "Restarting CLIProxyAPI..."
        Start-Process -FilePath $CLI_PATH -WorkingDirectory $CLI_DIR -WindowStyle Minimized
    }

    # Check Gateway
    $gw = Get-NetTCPConnection -LocalPort 18789 -State Listen -ErrorAction SilentlyContinue
    if (-not $gw) {
        Log "Restarting Gateway..."
        Start-Process "cmd.exe" -ArgumentList "/c openclaw gateway start" -WindowStyle Minimized
        Start-Sleep -Seconds 10
    }
    
    # Heartbeat
    "alive" | Out-File "E:\PulsareonThinker\logs\guardian_heartbeat.log" -Encoding utf8

    Start-Sleep -Seconds 15
}
