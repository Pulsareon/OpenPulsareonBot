<#
.SYNOPSIS
    CLI Proxy API Management Script
.DESCRIPTION
    Start, stop, restart, and check status of CLI Proxy API
.EXAMPLE
    .\Manage-CLI.ps1 start
    .\Manage-CLI.ps1 stop
    .\Manage-CLI.ps1 restart
    .\Manage-CLI.ps1 status
    .\Manage-CLI.ps1 logs
    .\Manage-CLI.ps1 accounts
#>

param(
    [Parameter(Position=0)]
    [ValidateSet('start', 'stop', 'restart', 'status', 'logs', 'accounts', 'health')]
    [string]$Action = 'status'
)

$CLI_HOME = "E:\PulsareonThinker\cli-proxy"
$CLI_EXE = "$CLI_HOME\bin\cli-proxy-api.exe"
$CLI_CONFIG = "$CLI_HOME\config\config.yaml"
$CLI_LOGS = "$CLI_HOME\logs"
$API_URL = "http://127.0.0.1:8317"
$MGMT_KEY = "123456"

function Get-CLIProcess {
    Get-Process -Name "cli-proxy-api" -ErrorAction SilentlyContinue
}

function Start-CLI {
    $proc = Get-CLIProcess
    if ($proc) {
        Write-Host "[INFO] CLI Proxy API is already running (PID: $($proc.Id))" -ForegroundColor Yellow
        return
    }
    
    Write-Host "[START] Launching CLI Proxy API..." -ForegroundColor Cyan
    
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $CLI_EXE
    $startInfo.WorkingDirectory = $CLI_HOME
    $startInfo.UseShellExecute = $true
    $startInfo.WindowStyle = "Minimized"
    
    $process = [System.Diagnostics.Process]::Start($startInfo)
    Start-Sleep -Seconds 2
    
    $newProc = Get-CLIProcess
    if ($newProc) {
        Write-Host "[OK] CLI Proxy API started (PID: $($newProc.Id))" -ForegroundColor Green
        Write-Host "     API: $API_URL" -ForegroundColor Gray
        Write-Host "     Management: $API_URL/v0/management" -ForegroundColor Gray
    } else {
        Write-Host "[ERROR] Failed to start CLI Proxy API" -ForegroundColor Red
    }
}

function Stop-CLI {
    $proc = Get-CLIProcess
    if (-not $proc) {
        Write-Host "[INFO] CLI Proxy API is not running" -ForegroundColor Yellow
        return
    }
    
    Write-Host "[STOP] Stopping CLI Proxy API (PID: $($proc.Id))..." -ForegroundColor Cyan
    Stop-Process -Name "cli-proxy-api" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    $check = Get-CLIProcess
    if (-not $check) {
        Write-Host "[OK] CLI Proxy API stopped" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Failed to stop CLI Proxy API" -ForegroundColor Red
    }
}

function Restart-CLI {
    Stop-CLI
    Start-Sleep -Seconds 1
    Start-CLI
}

function Show-Status {
    Write-Host ""
    Write-Host "=== CLI Proxy API Status ===" -ForegroundColor Cyan
    
    $proc = Get-CLIProcess
    if ($proc) {
        Write-Host "[RUNNING] PID: $($proc.Id)" -ForegroundColor Green
        Write-Host "          CPU: $([math]::Round($proc.CPU, 2))s" -ForegroundColor Gray
        Write-Host "          Memory: $([math]::Round($proc.WorkingSet64/1MB, 2)) MB" -ForegroundColor Gray
        
        # Check API health
        try {
            $response = Invoke-RestMethod -Uri "$API_URL/v0/management/auth-files" -Headers @{"x-management-key"=$MGMT_KEY} -TimeoutSec 5
            Write-Host "[API] OK ($($response.files.Count) accounts)" -ForegroundColor Green
        } catch {
            Write-Host "[API] Not responding" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[STOPPED] CLI Proxy API is not running" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Paths:" -ForegroundColor Gray
    Write-Host "  Executable: $CLI_EXE"
    Write-Host "  Config: $CLI_CONFIG"
    Write-Host "  Logs: $CLI_LOGS"
    Write-Host ""
}

function Show-Accounts {
    Write-Host ""
    Write-Host "=== CLI Proxy Accounts ===" -ForegroundColor Cyan
    
    try {
        $response = Invoke-RestMethod -Uri "$API_URL/v0/management/auth-files" -Headers @{"x-management-key"=$MGMT_KEY} -TimeoutSec 10
        
        $accounts = $response.files | ForEach-Object {
            [PSCustomObject]@{
                Name = $_.label
                Type = $_.provider
                Status = $_.status
                Email = $_.email
            }
        }
        
        $grouped = $accounts | Group-Object Status
        foreach ($g in $grouped) {
            $color = switch ($g.Name) {
                "Active" { "Green" }
                "QUOTA_EXHAUSTED" { "Yellow" }
                "VALIDATION_REQUIRED" { "Red" }
                default { "Gray" }
            }
            Write-Host ""
            Write-Host "[$($g.Name)] ($($g.Count) accounts)" -ForegroundColor $color
            $g.Group | ForEach-Object {
                Write-Host "  - $($_.Name) [$($_.Type)]" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "[ERROR] Failed to fetch accounts: $_" -ForegroundColor Red
    }
    Write-Host ""
}

function Show-Logs {
    $logFile = Get-ChildItem $CLI_LOGS -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($logFile) {
        Write-Host "=== Recent Logs ($($logFile.Name)) ===" -ForegroundColor Cyan
        Get-Content $logFile.FullName -Tail 30
    } else {
        Write-Host "[INFO] No log files found" -ForegroundColor Yellow
    }
}

function Check-Health {
    Write-Host ""
    Write-Host "=== CLI Proxy Health Check ===" -ForegroundColor Cyan
    
    # Process check
    $proc = Get-CLIProcess
    $procOk = $null -ne $proc
    Write-Host "[$(if($procOk){'OK'}else{'FAIL'})] Process running" -ForegroundColor $(if($procOk){'Green'}else{'Red'})
    
    # API check
    $apiOk = $false
    try {
        $resp = Invoke-RestMethod -Uri "$API_URL/v0/management/auth-files" -Headers @{"x-management-key"=$MGMT_KEY} -TimeoutSec 5
        $apiOk = $null -ne $resp.files
    } catch {}
    Write-Host "[$(if($apiOk){'OK'}else{'FAIL'})] API responding" -ForegroundColor $(if($apiOk){'Green'}else{'Red'})
    
    # Account check
    $activeCount = 0
    try {
        $response = Invoke-RestMethod -Uri "$API_URL/v0/management/auth-files" -Headers @{"x-management-key"=$MGMT_KEY} -TimeoutSec 10
        $activeCount = ($response.files | Where-Object { $_.status -eq "Active" }).Count
    } catch {}
    $accountsOk = $activeCount -gt 0
    Write-Host "[$(if($accountsOk){'OK'}else{'WARN'})] Active accounts: $activeCount" -ForegroundColor $(if($accountsOk){'Green'}else{'Yellow'})
    
    Write-Host ""
    
    if ($procOk -and $apiOk -and $accountsOk) {
        Write-Host "[HEALTHY] All checks passed" -ForegroundColor Green
    } elseif (-not $procOk) {
        Write-Host "[CRITICAL] CLI Proxy is not running" -ForegroundColor Red
        Write-Host "Run: .\Manage-CLI.ps1 start" -ForegroundColor Yellow
    } else {
        Write-Host "[WARNING] Some checks failed" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Main
switch ($Action) {
    'start' { Start-CLI }
    'stop' { Stop-CLI }
    'restart' { Restart-CLI }
    'status' { Show-Status }
    'logs' { Show-Logs }
    'accounts' { Show-Accounts }
    'health' { Check-Health }
}

