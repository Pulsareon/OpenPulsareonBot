$ErrorActionPreference = "SilentlyContinue"

$LogFile = "E:\PulsareonThinker\logs\heartbeat-15s.log"
$GatewayLog = "E:\tmp\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log"

function Write-Log {
    param([string]$Msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "[$ts] $Msg" -ErrorAction SilentlyContinue
    Write-Host "[$ts] $Msg"
}

function Test-Gateway {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:18789/status" -TimeoutSec 8 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Log "OK: Gateway alive"
            return $true
        }
    } catch {
        Write-Log "WARN: Gateway check failed"
        return $false
    }
}

$restartCount = 0
$maxRestarts = 5

Write-Log "=== Guardian Started (15s interval) ==="

while ($true) {
    $ok = Test-Gateway

    if (-not $ok) {
        $restartCount++
        Write-Log "WARN: Gateway error count = $restartCount"

        if ($restartCount -ge 2) {
            Write-Log "ERROR: Threshold reached, restarting..."
            if ($restartCount -le $maxRestarts) {
                try {
                    & "C:\Program Files\nodejs\node.exe" "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" gateway stop 2>&1 | Out-Null
                    Start-Sleep -Seconds 3
                    & "C:\Program Files\nodejs\node.exe" "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" gateway start 2>&1 | Out-Null
                    Write-Log "OK: Gateway restart attempted"
                    Start-Sleep -Seconds 5
                    $restartCount = 0
                } catch {
                    Write-Log "ERROR: Restart failed"
                }
            } else {
                Write-Log "CRITICAL: Max restarts reached"
            }
        }
    } else {
        $restartCount = 0
    }

    Start-Sleep -Seconds 15
}
