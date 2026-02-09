# ============================================================
# Pulsareon Startup Script
# 启动所有核心服务
# ============================================================

$ErrorActionPreference = "SilentlyContinue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pulsareon System Startup" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 路径配置
$WORKSPACE = "E:\PulsareonThinker"
$CLI_DIR = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64"
$CLI_EXE = "$CLI_DIR\cli-proxy-api.exe"
$GUARDIAN = "$WORKSPACE\scripts\guardian\safety_guardian.ps1"

# 1. 启动 CLI Proxy API
Write-Host "[1/3] Starting CLI Proxy API..." -ForegroundColor Yellow
$cliProc = Get-Process -Name "cli-proxy-api" -ErrorAction SilentlyContinue
if (-not $cliProc) {
    Start-Process -FilePath $CLI_EXE -WorkingDirectory $CLI_DIR -WindowStyle Minimized
    Write-Host "      CLI Proxy API started" -ForegroundColor Green
} else {
    Write-Host "      CLI Proxy API already running (PID: $($cliProc.Id))" -ForegroundColor Gray
}
Start-Sleep -Seconds 3

# 2. 启动 OpenClaw Gateway
Write-Host "[2/3] Starting OpenClaw Gateway..." -ForegroundColor Yellow
$gwPort = Get-NetTCPConnection -LocalPort 18789 -State Listen -ErrorAction SilentlyContinue
if (-not $gwPort) {
    Start-Process "cmd.exe" -ArgumentList "/c openclaw gateway start" -WindowStyle Minimized
    Write-Host "      OpenClaw Gateway starting..." -ForegroundColor Green
    Start-Sleep -Seconds 8
} else {
    Write-Host "      OpenClaw Gateway already running" -ForegroundColor Gray
}

# 3. 启动 Safety Guardian
Write-Host "[3/3] Starting Safety Guardian..." -ForegroundColor Yellow
# 检查是否已有 guardian 运行
$guardianProc = Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Where-Object {
    $_.MainWindowTitle -like "*safety_guardian*" -or $_.CommandLine -like "*safety_guardian*"
}
if (-not $guardianProc) {
    Start-Process "powershell.exe" -ArgumentList "-ExecutionPolicy Bypass -File `"$GUARDIAN`"" -WindowStyle Minimized
    Write-Host "      Safety Guardian started" -ForegroundColor Green
} else {
    Write-Host "      Safety Guardian may already be running" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Startup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services:" -ForegroundColor White
Write-Host "  - CLI Proxy API:    http://127.0.0.1:8317" -ForegroundColor Gray
Write-Host "  - OpenClaw Gateway: http://127.0.0.1:18789" -ForegroundColor Gray
Write-Host "  - Dashboard:        http://127.0.0.1:18789/" -ForegroundColor Gray
Write-Host ""
Write-Host "Logs:" -ForegroundColor White
Write-Host "  - Guardian:         $WORKSPACE\logs\safety_guardian.log" -ForegroundColor Gray
Write-Host "  - OpenClaw:         \tmp\openclaw\openclaw-*.log" -ForegroundColor Gray
Write-Host ""

# 验证服务
Write-Host "Verifying services..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

$cliOK = Test-NetConnection -ComputerName 127.0.0.1 -Port 8317 -WarningAction SilentlyContinue
$gwOK = Test-NetConnection -ComputerName 127.0.0.1 -Port 18789 -WarningAction SilentlyContinue

if ($cliOK.TcpTestSucceeded) {
    Write-Host "  [OK] CLI Proxy API" -ForegroundColor Green
} else {
    Write-Host "  [!!] CLI Proxy API not responding" -ForegroundColor Red
}

if ($gwOK.TcpTestSucceeded) {
    Write-Host "  [OK] OpenClaw Gateway" -ForegroundColor Green
} else {
    Write-Host "  [!!] OpenClaw Gateway not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
