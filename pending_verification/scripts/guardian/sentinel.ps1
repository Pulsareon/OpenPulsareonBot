# Pulsareon Sentinel - The Last Line of Defense
# Checks system health. If dead for too long, resets to last known good git state.

$Workspace = "E:\PulsareonThinker"
$StateFile = "$Workspace\data\state\heartbeat.timestamp"
$ThresholdMinutes = 30 

# 1. Check Heartbeat
if (-not (Test-Path $StateFile)) {
    Write-Host "No heartbeat file found. Assuming fresh start."
    exit
}

$LastHeartbeat = [DateTime](Get-Content $StateFile)
$TimeDiff = (Get-Date) - $LastHeartbeat

if ($TimeDiff.TotalMinutes -gt $ThresholdMinutes) {
    Write-Host "⚠️ SYSTEM DEAD DETECTED (Last beat: $LastHeartbeat)"
    Write-Host "⚡ Initiating Emergency Rollback Protocol..."
    
    cd $Workspace
    
    # 2. Protect Memory (Critical)
    $BackupDir = "$Workspace\backups\emergency_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory $BackupDir -Force
    Copy-Item "$Workspace\memory" "$BackupDir\memory" -Recurse
    Copy-Item "$Workspace\data" "$BackupDir\data" -Recurse
    
    # 3. Hard Reset Code
    git reset --hard HEAD
    git clean -fd # Be careful with this, depends on .gitignore
    
    # 4. Restore Memory (Merge back)
    # Actually, if memory is gitignored, reset won't touch it.
    # But we copy back just in case the user modified gitignored files that we want to keep?
    # No, git clean removes untracked. Memory IS untracked (ignored).
    # git clean -x would remove ignored. -fd removes untracked but NOT ignored.
    # So Memory is safe if ignored.
    
    # 5. Restart Services
    Write-Host "♻️ Restarting Gateway..."
    # nssm restart OpenClaw or similar
    # For now, we assume external watcher handles process restart if we kill it
    Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
    
    Write-Host "✅ Rollback Complete. System should recover."
    
    # Update timestamp to prevent loop
    (Get-Date).ToString() | Set-Content $StateFile
} else {
    Write-Host "✅ System Healthy. Last beat: $LastHeartbeat"
}
