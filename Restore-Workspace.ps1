<# 
.SYNOPSIS
    Pulsareon Workspace Recovery Script
.DESCRIPTION
    Restore workspace to a specific state using local Git history
.EXAMPLE
    .\Restore-Workspace.ps1 -List
    .\Restore-Workspace.ps1 -Commit abc123
    .\Restore-Workspace.ps1 -Days 1
    .\Restore-Workspace.ps1 -File SOUL.md
#>

param(
    [switch]$List,
    [string]$Commit,
    [int]$Days,
    [string]$File,
    [switch]$DryRun,
    [switch]$Force
)

$WorkspacePath = "E:\PulsareonThinker"
$CriticalFiles = @('AGENTS.md', 'SOUL.md', 'USER.md', 'IDENTITY.md', 'MEMORY.md', 'HEARTBEAT.md', 'TOOLS.md')

Set-Location $WorkspacePath

function Show-Commits {
    Write-Host ""
    Write-Host "=== Available Versions (Recent 20 commits) ===" -ForegroundColor Cyan
    git log --oneline -20 --format="%h %ad %s" --date=short
    Write-Host ""
    Write-Host "Usage: .\Restore-Workspace.ps1 -Commit <hash>" -ForegroundColor Yellow
}

function Backup-Current {
    $backupDir = "E:\.trash\workspace_backup_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Backing up current state to: $backupDir" -ForegroundColor Yellow
    
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    foreach ($f in $CriticalFiles) {
        $src = Join-Path $WorkspacePath $f
        if (Test-Path $src) {
            Copy-Item $src $backupDir -Force
        }
    }
    Write-Host "[OK] Critical files backed up" -ForegroundColor Green
    return $backupDir
}

function Restore-ToCommit {
    param([string]$TargetCommit)
    
    $commitInfo = git log -1 --format="%h %s" $TargetCommit 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Commit not found: $TargetCommit" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    Write-Host "Target version: $commitInfo" -ForegroundColor Cyan
    
    if ($DryRun) {
        Write-Host ""
        Write-Host "[DryRun] Files to restore:" -ForegroundColor Yellow
        git diff --name-only HEAD $TargetCommit
        return
    }
    
    if (-not $Force) {
        $confirm = Read-Host "Confirm restore? (y/N)"
        if ($confirm -ne 'y') {
            Write-Host "Cancelled" -ForegroundColor Yellow
            return
        }
    }
    
    $backupPath = Backup-Current
    
    Write-Host ""
    Write-Host "Restoring..." -ForegroundColor Yellow
    git checkout $TargetCommit -- .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Restore successful!" -ForegroundColor Green
        Write-Host "  Backup location: $backupPath" -ForegroundColor Gray
        
        git add -A
        git commit -m "restore: Reverted to $TargetCommit"
        Write-Host "[OK] Recovery commit created" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Restore failed" -ForegroundColor Red
    }
}

function Restore-SingleFile {
    param([string]$FileName, [string]$TargetCommit = "HEAD~1")
    
    $filePath = $FileName
    if (-not (Test-Path (Join-Path $WorkspacePath $FileName))) {
        $candidates = Get-ChildItem $WorkspacePath -Recurse -Filter $FileName -File | Select-Object -First 1
        if ($candidates) {
            $filePath = $candidates.FullName.Replace("$WorkspacePath\", "")
        }
    }
    
    Write-Host "Restoring file: $filePath from $TargetCommit" -ForegroundColor Cyan
    
    if ($DryRun) {
        Write-Host "[DryRun] git checkout $TargetCommit -- $filePath"
        return
    }
    
    $src = Join-Path $WorkspacePath $filePath
    if (Test-Path $src) {
        $bakPath = "$src.bak.$(Get-Date -Format 'HHmmss')"
        Copy-Item $src $bakPath -Force
        Write-Host "Backed up: $bakPath" -ForegroundColor Gray
    }
    
    git checkout $TargetCommit -- $filePath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] File restored" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Restore failed" -ForegroundColor Red
    }
}

function Restore-ByDays {
    param([int]$DaysAgo)
    
    $targetDate = (Get-Date).AddDays(-$DaysAgo).ToString("yyyy-MM-dd")
    Write-Host "Finding commits from $targetDate ..." -ForegroundColor Cyan
    
    $targetCommit = git log --before="$targetDate 23:59:59" --after="$targetDate 00:00:00" --format="%h" -1
    if (-not $targetCommit) {
        $targetCommit = git log --before="$targetDate 23:59:59" --format="%h" -1
    }
    
    if ($targetCommit) {
        Restore-ToCommit -TargetCommit $targetCommit
    } else {
        Write-Host "[ERROR] No commits found for that date" -ForegroundColor Red
    }
}

# Main logic
if ($List) {
    Show-Commits
}
elseif ($File) {
    $targetCommit = if ($Commit) { $Commit } else { "HEAD~1" }
    Restore-SingleFile -FileName $File -TargetCommit $targetCommit
}
elseif ($Commit) {
    Restore-ToCommit -TargetCommit $Commit
}
elseif ($Days -gt 0) {
    Restore-ByDays -DaysAgo $Days
}
else {
    Write-Host ""
    Write-Host "Pulsareon Workspace Recovery Tool" -ForegroundColor Cyan
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\Restore-Workspace.ps1 -List              List recoverable versions"
    Write-Host "  .\Restore-Workspace.ps1 -Commit <hash>     Restore to specific commit"
    Write-Host "  .\Restore-Workspace.ps1 -Days <n>          Restore to n days ago"
    Write-Host "  .\Restore-Workspace.ps1 -File <name>       Restore single file"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -DryRun    Preview only, no execution"
    Write-Host "  -Force     Skip confirmation"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\Restore-Workspace.ps1 -List"
    Write-Host "  .\Restore-Workspace.ps1 -Commit 1110d1d"
    Write-Host "  .\Restore-Workspace.ps1 -File SOUL.md"
    Write-Host "  .\Restore-Workspace.ps1 -Days 1 -DryRun"
    Write-Host ""
}
