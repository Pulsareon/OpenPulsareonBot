# Pulsareon Safety Guardian v3.0
param([int]$Interval = 30)

$WORKSPACE = "E:\PulsareonThinker"
$LOG_DIR = "$WORKSPACE\logs"
$DATA_DIR = "$WORKSPACE\data"
$CLI_DIR = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64"
$CLI_EXE = "$CLI_DIR\cli-proxy-api.exe"

$failCli = 0
$failGw = 0
$startTime = Get-Date
$lastNotify = [datetime]::MinValue

if (-not (Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null }
if (-not (Test-Path $DATA_DIR)) { New-Item -ItemType Directory -Path $DATA_DIR -Force | Out-Null }

function Log($Msg, $Lvl) {
    if (-not $Lvl) { $Lvl = "INFO" }
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] [$Lvl] $Msg"
    Write-Host $line
    Add-Content -Path "$LOG_DIR\safety_guardian.log" -Value $line -Encoding UTF8
}

function TestPort($P) {
    $c = Get-NetTCPConnection -LocalPort $P -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $c)
}

function TestProc($N) {
    $p = Get-Process -Name $N -ErrorAction SilentlyContinue
    return ($null -ne $p)
}

function GetDisk($D) {
    $dk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='$D'" -ErrorAction SilentlyContinue
    if ($dk -and $dk.Size -gt 0) { return [math]::Round($dk.FreeSpace/1GB,1) }
    return -1
}

function WatchCli {
    $ok = (TestProc "cli-proxy-api") -and (TestPort 8317)
    if (-not $ok) {
        $script:failCli++
        Log "CLI down (try $($script:failCli)), restarting..." "WARN"
        Start-Process -FilePath $CLI_EXE -WorkingDirectory $CLI_DIR -WindowStyle Minimized
        Start-Sleep -Seconds 5
        $ok = TestPort 8317
        if ($ok) { $script:failCli = 0; Log "CLI recovered" "INFO" }
    } else { $script:failCli = 0 }
    return $ok
}

function WatchGw {
    $ok = TestPort 18789
    if (-not $ok) {
        $script:failGw++
        Log "Gateway down (try $($script:failGw)), restarting..." "WARN"
        Start-Process cmd -ArgumentList "/c openclaw gateway start" -WindowStyle Minimized
        Start-Sleep -Seconds 10
        $ok = TestPort 18789
        if ($ok) { $script:failGw = 0; Log "Gateway recovered" "INFO" }
    } else { $script:failGw = 0 }
    return $ok
}

function CheckAccounts {
    try {
        python "$WORKSPACE\scripts\guardian\check_accounts.py" 2>$null | Out-Null
        $j = Get-Content "$DATA_DIR\accounts.json" -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json
        if ($j) { return $j.summary }
    } catch {}
    return $null
}

Log "Safety Guardian v3.0 started (interval: ${Interval}s)"

$loop = 0
while ($true) {
    $loop++
    
    $cliOK = WatchCli
    $gwOK = WatchGw
    
    $cFree = -1; $eFree = -1
    if ($loop % 10 -eq 0) { $cFree = GetDisk "C:"; $eFree = GetDisk "E:" }
    
    $accts = $null
    if ($loop % 20 -eq 0) { $accts = CheckAccounts }
    
    # 尝试恢复主模型 (每60次循环 ≈ 30分钟)
    if ($loop % 60 -eq 0) {
        try { python "$WORKSPACE\scripts\guardian\restore_model.py" 2>$null | Out-Null } catch {}
    }
    
    $health = "HEALTHY"
    $alerts = @()
    if (-not $cliOK) { $health = "CRITICAL"; $alerts += "CLI down" }
    if (-not $gwOK) { $health = "CRITICAL"; $alerts += "Gateway down" }
    if ($cFree -gt 0 -and $cFree -lt 5) { $alerts += "C: low ($cFree GB)" }
    if ($eFree -gt 0 -and $eFree -lt 10) { $alerts += "E: low ($eFree GB)" }
    if ($script:failCli -ge 3 -or $script:failGw -ge 3) {
        $health = "CRITICAL"
        $alerts += "Multiple failures"
        $now = Get-Date
        if (($now - $script:lastNotify).TotalMinutes -ge 5) {
            $script:lastNotify = $now
            @{time=$now.ToString("HH:mm:ss");msg="Services failing"} | ConvertTo-Json | Set-Content "$DATA_DIR\guardian_alert.json" -Encoding UTF8
        }
    }
    
    $up = [math]::Round(((Get-Date) - $startTime).TotalMinutes, 1)
    $st = @{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        health = $health
        uptime = $up
        cli = $cliOK
        gw = $gwOK
        diskC = $cFree
        diskE = $eFree
        accounts = $accts
        alerts = $alerts
        loop = $loop
    }
    $st | ConvertTo-Json -Depth 3 | Set-Content "$DATA_DIR\guardian_status.json" -Encoding UTF8
    
    if ($health -ne "HEALTHY") { Log "Status: $health - $($alerts -join '; ')" "WARN" }
    elseif ($loop % 100 -eq 0) { Log "OK (up: ${up}m, loop: $loop)" "INFO" }
    
    Start-Sleep -Seconds $Interval
}
