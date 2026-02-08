# OpenClaw Auto-Stabilizer - Simplified Version
# Safe for Windows, no complex PowerShell features

# Configuration
$ConfigDir = "C:\Users\Administrator\.openclaw"
$WorkDir = "E:\PulsareonThinker"
$LogFile = "$WorkDir\logs\autostable.log"

# Test if Gateway is running
function Test-GatewayRunning {
    $nodePath = "C:\Program Files\nodejs\node.exe"
    $openclawPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js"
    
    $result = & $nodePath $openclawPath gateway status 2>&1
    return ($LASTEXITCODE -eq 0)
}

# Backup configuration
function Backup-Config {
    $configPath = "$ConfigDir\openclaw.json"
    if (Test-Path $configPath) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupPath = "$configPath.auto-backup-$timestamp"
        Copy-Item -Path $configPath -Destination $backupPath -Force
        
        # Keep last 10
        $backups = Get-ChildItem -Path $ConfigDir -Filter "openclaw.json.auto-backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -Skip 10
        if ($backups) {
            $backups | Remove-Item -Force
        }
        
        return $backupPath
    }
    return $null
}

# Restart Gateway safely
function Restart-Gateway {
    $nodePath = "C:\Program Files\nodejs\node.exe"
    $openclawPath = "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js"
    
    # Stop
    & $nodePath $openclawPath gateway stop 2>&1 | Out-Null
    Start-Sleep -Seconds 15
    
    # Start
    & $nodePath $openclawPath gateway start 2>&1 | Out-Null
    Start-Sleep -Seconds 10
    
    # Verify
    return Test-GatewayRunning
}

# Clean temp files
function Clean-Temp {
    $temps = @(
        "$WorkDir\diagnose-openclaw.ps1",
        "$WorkDir\safe-diagnose.ps1.bak"
    )
    
    foreach ($t in $temps) {
        if (Test-Path $t) {
            Remove-Item $t -Force -ErrorAction SilentlyContinue
        }
    }
}

# Check critical files
function Test-Critical-Files {
    $files = @(
        "$ConfigDir\openclaw.json",
        "$WorkDir\memory\STORAGE.md",
        "$WorkDir\core\SOUL.md"
    )
    
    foreach ($f in $files) {
        if (-not (Test-Path $f)) {
            return $false
        }
    }
    return $true
}

# Log to file
function Write-Log {
    param([string]$msg)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] $msg"
    
    # Create log directory if needed
    $logDir = Split-Path -Parent $LogFile
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    Add-Content -Path $LogFile -Value $entry -ErrorAction SilentlyContinue
    Write-Host $entry
}

# Health check
function Check-Health {
    $issues = 0
    
    Write-Log "=== Health Check ==="
    
    # Gateway
    if (Test-GatewayRunning) {
        Write-Log "[OK] Gateway running"
    } else {
        Write-Log "[ERROR] Gateway not running"
        $issues++
    }
    
    # Config
    $backup = Backup-Config
    if ($backup) {
        Write-Log "[OK] Config backed to $backup"
    } else {
        Write-Log "[WARN] Config backup failed"
        $issues++
    }
    
    # Critical files
    if (Test-Critical-Files) {
        Write-Log "[OK] Critical files present"
    } else {
        Write-Log "[ERROR] Missing critical files"
        $issues++
    }
    
    # Memory.md type check
    if (Test-Path "$WorkDir\memory\STORAGE.md" -PathType Leaf) {
        Write-Log "[OK] STORAGE.md is a file"
    } else {
        Write-Log "[ERROR] STORAGE.md problem"
        $issues++
    }
    
    # Clean temp
    Clean-Temp
    Write-Log "[OK] Temp files cleaned"
    
    return $issues -eq 0
}

# Auto-fix
function Auto-Fix {
    Write-Log "=== Auto Fix Mode ==="
    
    # Check Gateway
    if (-not (Test-GatewayRunning)) {
        Write-Log "[FIX] Restarting Gateway..."
        
        if (Restart-Gateway) {
            Write-Log "[OK] Gateway restarted successfully"
        } else {
            Write-Log "[CRITICAL] Gateway restart failed"
            return $false
        }
    }
    
    # Backup config
    Backup-Config
    
    return $true
}

# Main
if ($args -contains "-Continuous") {
    # Continuous mode
    while ($true) {
        $healthy = Check-Health
        
        if (-not $healthy) {
            Write-Log "[WARN] Health issues found, attempting fix..."
            Auto-Fix
        }
        
        Write-Log "[INFO] Waiting 5 minutes..."
        Start-Sleep -Seconds 300
    }
} else {
    # Single run
    $healthy = Check-Health
    
    if (-not $healthy -or $args -contains "-AutoFix") {
        Auto-Fix
    }
    
    Write-Log "[INFO] Check completed. Status: $(if ($healthy) { 'HEALTHY' } else { 'NEEDS ATTENTION' })"
}
