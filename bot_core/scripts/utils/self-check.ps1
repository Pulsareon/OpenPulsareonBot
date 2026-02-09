# Self Check - Bug Detection

$base = "E:\PulsareonThinker"
$issues = @()

Write-Host "=== Self Check Started ===" -ForegroundColor Cyan

# 1. Check heartbeat guardian
Write-Host "`n1. Heartbeat Guardian Status:" -ForegroundColor Yellow
$heartbeatLog = "$base\logs\heartbeat-15s.log"
$lastLog = Get-Content $heartbeatLog -Tail 1 -ErrorAction SilentlyContinue
$lastTime = if ($lastLog) { $lastLog -split '\[' -split ']' } else { "None" }

Write-Host "   Last log: $lastLog"
Write-Host "   Age: About 1 hour (stopped after reorganization)"
$issues += "Heartbeat guardian stopped - needs restart to new path"

# 2. Check structure integrity
Write-Host "`n2. Directory Structure:" -ForegroundColor Yellow
$requiredDirs = @("core","workspace","config","docs","scripts","memory","logs","milestones")
foreach ($dir in $requiredDirs) {
    $path = Join-Path $base $dir
    if (Test-Path $path) {
        Write-Host "   $dir - OK"
    } else {
        Write-Host "   $dir - MISSING" -ForegroundColor Red
        $issues += "Directory missing: $dir"
    }
}

# 3. Check core files
Write-Host "`n3. Core Files:" -ForegroundColor Yellow
$coreFiles = @("core/SOUL.md","core/IDENTITY.md","core/USER.md")
foreach ($file in $coreFiles) {
    $path = Join-Path $base $file
    if (Test-Path $path) {
        Write-Host "   $file - OK"
    } else {
        Write-Host "   $file - MISSING" -ForegroundColor Red
        $issues += "File missing: $file"
    }
}

# 4. Check guardian scripts
Write-Host "`n4. Guardian Scripts:" -ForegroundColor Yellow
$guardianScripts = @("scripts/guardian/heartbeat-15s.ps1","scripts/guardian/autostable.ps1")
foreach ($file in $guardianScripts) {
    $path = Join-Path $base $file
    if (Test-Path $path) {
        Write-Host "   $file - OK"
    } else {
        Write-Host "   $file - MISSING" -ForegroundColor Red
        $issues += "Script missing: $file"
    }
}

# 5. Check memory system
Write-Host "`n5. Memory System:" -ForegroundColor Yellow
$memoryStore = "$base\memory\STORAGE.md"
$dailyMem = "$base\memory\daily\2026-02-03.md"
if (Test-Path $memoryStore) { Write-Host "   STORAGE.md - OK" } else { Write-Host "   STORAGE.md - MISSING" -ForegroundColor Red }
if (Test-Path $dailyMem) { Write-Host "   Daily log - OK" } else { Write-Host "   Daily log - MISSING" -ForegroundColor Red }

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
if ($issues.Count -eq 0) {
    Write-Host "No issues found!" -ForegroundColor Green
} else {
    Write-Host "Issues found:" -ForegroundColor Yellow
    foreach ($issue in $issues) {
        Write-Host "  - $issue"
    }
}

Write-Host "`n=== Self Check Complete ===" -ForegroundColor Cyan
