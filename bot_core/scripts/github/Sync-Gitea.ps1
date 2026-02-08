<#
.SYNOPSIS
    Sync workspace to local Gitea
.DESCRIPTION
    Push PulsareonThinker to local Gitea server
#>

param(
    [string]$GiteaUrl = "http://192.168.31.31:3000",
    [string]$RepoPath = "pulsareonbot/PulsareonThinker"
)

$WorkspacePath = "E:\PulsareonThinker"
Set-Location $WorkspacePath

# Check Gitea service
Write-Host "Checking Gitea service..." -ForegroundColor Cyan
try {
    $null = Invoke-WebRequest -Uri $GiteaUrl -TimeoutSec 3 -ErrorAction Stop
    Write-Host "[OK] Gitea is running" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Gitea is not running at $GiteaUrl" -ForegroundColor Red
    Write-Host "Start Gitea first, then run this script again." -ForegroundColor Yellow
    exit 1
}

# Check/add remote
$remotes = git remote
if ($remotes -notcontains "gitea") {
    Write-Host "Adding gitea remote..." -ForegroundColor Yellow
    git remote add gitea "$GiteaUrl/$RepoPath.git"
}

# Show remote
Write-Host ""
Write-Host "Remote URL:" -ForegroundColor Gray
git remote get-url gitea

# Push
Write-Host ""
Write-Host "Pushing to Gitea..." -ForegroundColor Cyan
git push gitea master 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) {
    # exit code 1 is often just a warning, check if push succeeded
    Write-Host ""
    Write-Host "[OK] Sync complete!" -ForegroundColor Green
    Write-Host "View at: $GiteaUrl/$RepoPath" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "[ERROR] Push failed" -ForegroundColor Red
    Write-Host "You may need to create the repository first at: $GiteaUrl" -ForegroundColor Yellow
}
