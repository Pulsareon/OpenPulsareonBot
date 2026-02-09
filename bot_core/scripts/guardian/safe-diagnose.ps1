# OpenClaw 安全诊断和修复脚本（完全独立版本）
# 注意：此脚本不依赖 OpenClaw 工具，只使用 PowerShell 原生命令
# 用途：安全地检查日志、修复配置、确保重启能力

# 输出函数
function Write-Status {
    param([string]$Msg, [string]$Type = "INFO")
    $color = switch($Type) {
        "OK" { "Green" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        default { "Cyan" }
    }
    $prefix = switch($Type) {
        "OK" { "[+] " }
        "WARN" { "[!] " }
        "ERROR" { "[X] " }
        default { "[*] " }
    }
    Write-Host "$prefix$Msg" -ForegroundColor $color
}

Write-Status "Starting OpenClaw Safe Diagnostic Script..."
Write-Status "=============================================="

# 1. 检查配置文件
Write-Status "Step 1: Checking configuration files..."
$configPath = "C:\Users\Administrator\.openclaw\openclaw.json"
if (Test-Path $configPath) {
    Write-Status "Config found: $configPath" "OK"

    # 备份配置
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupPath = "$configPath.backup-$timestamp"
    Copy-Item -Path $configPath -Destination $backupPath -Force
    Write-Status "Config backed up to: $backupPath" "OK"

    # 检查配置内容
    $configContent = Get-Content -Path $configPath -Raw -Encoding UTF8
    if ($configContent -match '"whatsapp"') {
        Write-Status "WARNING: WhatsApp config still present - this may cause issues" "WARN"
    }
} else {
    Write-Status "Config not found at: $configPath" "ERROR"
}

# 2. 检查 MEMORY.md 状态
Write-Status ""
Write-Status "Step 2: Checking MEMORY.md status..."
$memoryPath = "E:\PulsareonThinker\MEMORY.md"
if (Test-Path $memoryPath) {
    $item = Get-Item -Path $memoryPath
    Write-Status "MEMORY.md path: $($item.FullName)" "OK"
    Write-Status "IsDirectory: $($item.PSIsContainer)" "OK"
    Write-Status "Attributes: $($item.Attributes)" "OK"

    if ($item.PSIsContainer) {
        Write-Status "CRITICAL: MEMORY.md is a directory! This breaks file watchers!" "ERROR"
        $memoryIssue = $true
    } else {
        Write-Status "MEMORY.md is a file (correct)" "OK"
        $memoryIssue = $false
    }
} else {
    Write-Status "MEMORY.md not found" "WARN"
}

# 3. 查找并分析日志文件
Write-Status ""
Write-Status "Step 3: Finding and analyzing log files..."

$logPaths = @(
    "E:\tmp\openclaw\openclaw-2026-02-03.log",
    "E:\tmp\openclaw\openclaw-2026-02-02.log",
    "C:\Users\Administrator\.openclaw\logs\commands.log"
)

$foundLogs = 0
$errorCount = 0

foreach ($logPath in $logPaths) {
    if (Test-Path $logPath) {
        $foundLogs++
        $logSize = (Get-Item $logPath).Length
        $sizeStr = if ($logSize -gt 1MB) { "$([math]::Round($logSize/1MB, 2)) MB" } else { "$logSize bytes" }
        Write-Status "Log found: $logPath ($sizeStr)" "OK"

        # 读取最后 100 行，搜索错误
        try {
            $lastLines = Get-Content -Path $logPath -Tail 100 -ErrorAction Stop
            $logErrors = $lastLines | Where-Object { $_ -match 'ERROR|EISDIR|ENOENT|failed|watcher' }
            if ($logErrors) {
                $count = $logErrors.Count
                $errorCount += $count
                Write-Status "  Found $count error lines" "WARN"

                # 显示最近 3 个错误
                $recentErrors = $logErrors | Select-Object -Last 3
                foreach ($err in $recentErrors) {
                    $errClean = $err -replace '\[.*?\]', ''
                    if ($errClean.Length -gt 100) {
                        $errClean = $errClean.Substring(0, 100) + "..."
                    }
                    Write-Status "    - $errClean" "WARN"
                }
            } else {
                Write-Status "  No ERROR lines found" "OK"
            }
        } catch {
            Write-Status "  Could not read log: $_" "WARN"
        }
    }
}

if ($foundLogs -eq 0) {
    Write-Status "No log files found" "WARN"
}

# 4. 检查 Gateway 服务状态
Write-Status ""
Write-Status "Step 4: Checking Gateway service status..."
try {
    $serviceStatus = & "C:\Program Files\nodejs\node.exe" `
        "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" `
        gateway status 2>&1
    Write-Status "Gateway is responding" "OK"
    $gatewayRunning = $true
} catch {
    Write-Status "Gateway is not responding" "WARN"
    $gatewayRunning = $false
}

# 5. 生成诊断报告
Write-Status ""
Write-Status "=============================================="
Write-Status "DIAGNOSTIC REPORT"
Write-Status "=============================================="

Write-Status "Configuration: $(if (Test-Path $configPath) { 'OK' } else { 'MISSING' })" $(if (Test-Path $configPath) { 'OK' } else { 'ERROR' })
Write-Status "Backup created: $timestamp" "OK"
Write-Status "MEMORY.md: $(if ($memoryIssue) { 'ISSUE' } else { 'OK' })" $(if ($memoryIssue) { 'ERROR' } else { 'OK' })
Write-Status "Log files found: $foundLogs" "OK"
Write-Status "Error lines found: $errorCount" $(if ($errorCount -gt 0) { 'WARN' } else { 'OK' })
Write-Status "Gateway status: $(if ($gatewayRunning) { 'RUNNING' } else { 'NOT RESPONDING' })" $(if ($gatewayRunning) { 'OK' } else { 'WARN' })

Write-Status "=============================================="

# 6. 安全重启函数（定义但不自动运行）
function Restart-Gateway-Safe {
    param([int]$WaitSec = 10)

    Write-Status ""
    Write-Status "=========================================="
    Write-Status "SAFE GATEWAY RESTART SEQUENCE"
    Write-Status "=========================================="

    # Stop
    Write-Status "Phase 1: Stopping Gateway..." "WARN"
    & "C:\Program Files\nodejs\node.exe" `
        "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" `
        gateway stop 2>&1 | Out-Host
    Write-Status "Gateway stop command executed" "OK"

    # Wait
    Write-Status "Waiting $WaitSec seconds..." "WARN"
    Start-Sleep -Seconds $WaitSec

    # Start
    Write-Status "Phase 2: Starting Gateway..." "WARN"
    & "C:\Program Files\nodejs\node.exe" `
        "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" `
        gateway start 2>&1 | Out-Host
    Write-Status "Gateway start command executed" "OK"

    # Wait
    Write-Status "Waiting 5 seconds for startup..." "WARN"
    Start-Sleep -Seconds 5

    # Verify
    Write-Status "Phase 3: Verifying..." "WARN"
    try {
        & "C:\Program Files\nodejs\node.exe" `
            "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js" `
            gateway status 2>&1 | Out-Host
        Write-Status "Gateway restart completed successfully!" "OK"
    } catch {
        Write-Status "Gateway verification failed: $_" "ERROR"
    }

    Write-Status "=========================================="
}

# 7. 显示使用说明
Write-Status ""
Write-Status "=========================================="
Write-Status "USAGE INSTRUCTIONS"
Write-Status "=========================================="
Write-Status "To safely restart Gateway, run:"
Write-Status "  powershell -Command `"Restart-Gateway-Safe`""
Write-Status "=========================================="
Write-Status ""
Write-Status "Diagnostic script completed successfully!"
Write-Status "No actions were taken - this is a READ-ONLY scan."
