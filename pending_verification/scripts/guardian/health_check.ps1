# Pulsareon Health Check Script

param([switch]$Json, [switch]$Quiet)

$ErrorActionPreference = "SilentlyContinue"

# 检查端口
function Test-Port($Port) {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $conn)
}

# 检查进程
function Test-Proc($Name) {
    $proc = Get-Process -Name $Name -ErrorAction SilentlyContinue
    return ($null -ne $proc)
}

# 收集状态
$timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
$cliProcess = Test-Proc "cli-proxy-api"
$cliPort = Test-Port 8317
$gwPort = Test-Port 18789

$issues = @()
$overall = "HEALTHY"

if (-not $cliProcess) {
    $issues += "CLI Proxy API process not running"
    $overall = "CRITICAL"
}
if (-not $cliPort) {
    $issues += "CLI Proxy API port 8317 not listening"
    $overall = "CRITICAL"
}
if (-not $gwPort) {
    $issues += "OpenClaw Gateway port 18789 not listening"
    $overall = "CRITICAL"
}

# 磁盘检查
$diskInfo = ""
$eDrive = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='E:'" -ErrorAction SilentlyContinue
if ($eDrive) {
    $freeGB = [math]::Round($eDrive.FreeSpace / 1GB, 1)
    $diskInfo = "$freeGB GB free"
    if ($freeGB -lt 5) {
        $issues += "E: drive critically low ($freeGB GB)"
        if ($overall -ne "CRITICAL") { $overall = "WARNING" }
    }
}

# 输出
if ($Json) {
    $result = @{
        timestamp = $timestamp
        overall = $overall
        cliProcess = $cliProcess
        cliPort = $cliPort
        gwPort = $gwPort
        diskE = $diskInfo
        issues = $issues
    }
    $result | ConvertTo-Json
} elseif (-not $Quiet) {
    Write-Host ""
    Write-Host "=== Pulsareon Health Check ===" -ForegroundColor Cyan
    Write-Host "Time: $timestamp" -ForegroundColor Gray
    Write-Host ""
    
    $cliStatus = "DOWN"; $gwStatus = "DOWN"
    if ($cliProcess -and $cliPort) { $cliStatus = "OK" }
    if ($gwPort) { $gwStatus = "OK" }
    
    $cliColor = "Red"; $gwColor = "Red"
    if ($cliStatus -eq "OK") { $cliColor = "Green" }
    if ($gwStatus -eq "OK") { $gwColor = "Green" }
    
    Write-Host "Services:" -ForegroundColor White
    Write-Host "  CLI Proxy API:    [$cliStatus]" -ForegroundColor $cliColor
    Write-Host "  OpenClaw Gateway: [$gwStatus]" -ForegroundColor $gwColor
    Write-Host ""
    
    if ($diskInfo) {
        Write-Host "Disk E: $diskInfo" -ForegroundColor Gray
        Write-Host ""
    }
    
    $overallColor = "White"
    if ($overall -eq "HEALTHY") { $overallColor = "Green" }
    if ($overall -eq "WARNING") { $overallColor = "Yellow" }
    if ($overall -eq "CRITICAL") { $overallColor = "Red" }
    
    Write-Host "Overall: $overall" -ForegroundColor $overallColor
    
    if ($issues.Count -gt 0) {
        Write-Host ""
        Write-Host "Issues:" -ForegroundColor Red
        $issues | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    }
    Write-Host ""
}

# 退出码
if ($overall -eq "HEALTHY") { exit 0 }
elseif ($overall -eq "WARNING") { exit 1 }
else { exit 2 }
