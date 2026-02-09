# Safety Guardian v4.0 (Layer 2)
# Monitors Gateway health and triggers multi-layer recovery (Layer 1) on repeated failures.

param([int]$Interval = 30)

$LogPath = "E:\PulsareonThinker\logs\safety_guardian.log"
$MaxFailures = 5
$RecoveryScript = "E:\PulsareonThinker\skills\system-maintenance\scripts\repair_gateway.py"

function Log($msg, $level="INFO") {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] [$level] $msg"
    Write-Host $line
    $line | Out-File -Append $LogPath -Encoding utf8
}

function Run-Recovery {
    Log "Initiating multi-layer recovery..." "WARN"
    # Call Layer 1: Config Repair + Zombie Kill + Port Check
    Start-Process python -ArgumentList "$RecoveryScript" -Wait -NoNewWindow
    Log "Recovery script finished." "INFO"
}

Log "Safety Guardian v4.0 started (interval: ${Interval}s)" "INFO"

$failGw = 0

while ($true) {
    # Check Gateway (18789)
    $gwOk = Test-NetConnection -ComputerName localhost -Port 18789 -InformationLevel Quiet
    
    if (-not $gwOk) {
        $failGw++
        Log "Gateway down (failure count: $failGw)" "WARN"
        
        if ($failGw -ge $MaxFailures) {
            Log "Gateway failed repeatedly ($failGw). Triggering full recovery..." "CRITICAL"
            Run-Recovery
            $failGw = 0 # Reset counter after recovery attempt
            Start-Sleep -Seconds 10
        }
        
        Log "Attempting restart..." "INFO"
        Start-Process openclaw -ArgumentList "gateway start" -WindowStyle Minimized
        Start-Sleep -Seconds 10
    } else {
        if ($failGw -gt 0) {
            Log "Gateway recovered." "SUCCESS"
            $failGw = 0
        }
    }
    
    Start-Sleep -Seconds $Interval
}
