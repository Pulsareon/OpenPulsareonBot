# Pulsareon System Health & Optimization Script
# 核心目标：健康、安全、稳定、高效

$ErrorActionPreference = "SilentlyContinue"
Write-Host "--- Pulsareon Health Check Initializing ---" -ForegroundColor Cyan

# 1. 磁盘空间检查
$drive = Get-PSDrive E
$freeGB = [math]::Round($drive.Free / 1GB, 2)
$usedPercent = [math]::Round(($drive.Used / ($drive.Used + $drive.Free)) * 100, 2)
Write-Host "Disk E: $freeGB GB free ($usedPercent% used)" -ForegroundColor (if ($usedPercent -gt 90) {"Red"} else {"Green"})

# 2. 异常进程监控 (Top 5 CPU Users)
Write-Host "`nTop 5 CPU Consuming Processes:" -ForegroundColor Yellow
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, CPU, WorkingSet | Format-Table -AutoSize

# 3. 垃圾文件清理 (TempWork & npm cache)
Write-Host "`nScanning for junk files..." -ForegroundColor Yellow
$tempPath = "C:\Users\Administrator\Desktop\TempWork"
$junkItems = Get-ChildItem $tempPath -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-1) }
if ($junkItems) {
    Write-Host "Found $($junkItems.Count) items older than 24h. Cleaning..." -ForegroundColor Gray
    # $junkItems | Remove-Item -Recurse -Force # 实际执行前先仅记录，保证审慎
} else {
    Write-Host "Temp directory is clean." -ForegroundColor Green
}

# 4. 安全检查 (未授权的远程连接)
Write-Host "`nChecking active network connections..." -ForegroundColor Yellow
netstat -ano | Select-String "ESTABLISHED" | Select-Object -First 10

Write-Host "`n--- Health Check Complete ---" -ForegroundColor Cyan
