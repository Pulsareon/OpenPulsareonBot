# Restart Heartbeat Guardian with New Path

Write-Host "Stopping old heartbeat..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.Path -like "*heartbeat*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Waiting 2 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

Write-Host "Starting heartbeat with new path..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File 'E:\PulsareonThinker\scripts\guardian\heartbeat-15s.ps1'" -WindowStyle Hidden

Write-Host "Waiting 5 seconds for startup..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "Checking heartbeat log..." -ForegroundColor Cyan
Get-Content "E:\PulsareonThinker\logs\heartbeat-15s.log" -Tail 5 -ErrorAction SilentlyContinue

Write-Host "`nHeartbeat Guardian restarted with new path!" -ForegroundColor Green
