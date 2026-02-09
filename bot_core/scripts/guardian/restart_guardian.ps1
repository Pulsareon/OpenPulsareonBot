# Restart Guardian Script
Get-Process powershell -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.MainWindowTitle -notlike "*openclaw*" -and $_.Id -ne $PID) {
        Write-Host "Stopping PID $($_.Id)"
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File E:\PulsareonThinker\scripts\guardian\safety_guardian.ps1" -WindowStyle Minimized
Write-Host "Guardian v3.0 started"
