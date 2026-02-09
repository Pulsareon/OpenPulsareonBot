# Quick Reorganize PulsareonThinker

$ErrorActionPreference = "Stop"
$base = "E:\PulsareonThinker"
$backup = "E:\PulsareonThinker-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Starting Reorganization ===" -ForegroundColor Cyan
Write-Host "Backup: $backup" -ForegroundColor Yellow

# 1. Backup
Write-Host "`nStep 1: Backup..." -ForegroundColor Yellow
Copy-Item $base $backup -Recurse
Write-Host "Backup complete" -ForegroundColor Green

# 2. Create directories
Write-Host "`nStep 2: Create directories..." -ForegroundColor Yellow

$dirs = @("core","workspace","config","docs/telegram","scripts/guardian","scripts/tools","memory/daily","memory/long-term","memory/archive","logs","milestones")

foreach ($dir in $dirs) {
    $path = Join-Path $base $dir
    New-Item -ItemType Directory -Path $path -Force | Out-Null
    Write-Host "  Created: $dir"
}

# 3. Move core files
Write-Host "`nStep 3: Move core files..." -ForegroundColor Yellow

Move-Item "$base\SOUL.md" "$base\core\" -Force
Move-Item "$base\IDENTITY.md" "$base\core\" -Force
Move-Item "$base\USER.md" "$base\core\" -Force

Move-Item "$base\AGENTS.md" "$base\workspace\" -Force
Move-Item "$base\SYSTEM-ORGANIZATION.md" "$base\workspace\SYSTEM.md" -Force
Move-Item "$base\WORK-LOGIC.md" "$base\workspace\LOGIC.md" -Force
Move-Item "$base\HEARTBEAT.md" "$base\workspace\" -Force

Write-Host "Core files moved" -ForegroundColor Green

# 4. Move docs
Write-Host "`nStep 4: Move docs..." -ForegroundColor Yellow

Move-Item "$base\TOOLS.md" "$base\docs\" -Force
Move-Item "$base\MOLTBOOK.md" "$base\docs\" -Force

if (Test-Path "$base\TELEGRAM-STATUS.md") {
    Move-Item "$base\TELEGRAM-STATUS.md" "$base\docs\telegram\status.md" -Force
}

if (Test-Path "$base\data\docs") {
    Get-ChildItem "$base\data\docs" -Filter "*.md" | Move-Item -Destination "$base\docs\telegram\" -Force
}

Write-Host "Docs moved" -ForegroundColor Green

# 5. Move scripts
Write-Host "`nStep 5: Move scripts..." -ForegroundColor Yellow

$scriptFiles = @("heartbeat-15s.ps1","autostable.ps1","safe-diagnose.ps1")
foreach ($script in $scriptFiles) {
    if (Test-Path "$base\data\$script") {
        Move-Item "$base\data\$script" "$base\scripts\guardian\" -Force
    }
}

if (Test-Path "$base\data\get-telegram-status.ps1") {
    Move-Item "$base\data\get-telegram-status.ps1" "$base\scripts\tools\" -Force
}

Write-Host "Scripts moved" -ForegroundColor Green

# 6. Organize memory
Write-Host "`nStep 6: Organize memory..." -ForegroundColor Yellow

if (Test-Path "$base\MEMORY.md") {
    Move-Item "$base\MEMORY.md" "$base\memory\STORAGE.md" -Force
}

Get-ChildItem "$base\memory\*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '\d{4}-\d{2}-\d{2}' } | ForEach-Object {
    Move-Item $_.FullName "$base\memory\daily\" -Force
}

Write-Host "Memory organized" -ForegroundColor Green

# 7. Move logs
Write-Host "`nStep 7: Move logs..." -ForegroundColor Yellow

if (Test-Path "$base\data\*.log") {
    Get-ChildItem "$base\data\*.log" | Move-Item -Destination "$base\logs\" -Force
}

Write-Host "Logs moved" -ForegroundColor Green

# 8. Clean config files
Write-Host "`nStep 8: Clean config files..." -ForegroundColor Yellow

Get-ChildItem "$base\*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+\.' } | ForEach-Object {
    $newName = $_.Name -replace '^\d+\.', ''
    Move-Item $_.FullName "$base\config\$newName" -Force
}

Write-Host "Config files cleaned" -ForegroundColor Green

# 9. Clean up
Write-Host "`nStep 9: Clean up..." -ForegroundColor Yellow

Remove-Item "$base\data" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$base\skills" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Cleanup complete" -ForegroundColor Green

Write-Host "`n=== Reorganization Complete ===" -ForegroundColor Green
Write-Host "Backup: $backup" -ForegroundColor Cyan
Write-Host "New structure created!" -ForegroundColor Cyan
