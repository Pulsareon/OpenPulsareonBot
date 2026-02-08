# Pulsareon System Bootstrap Script
# 用于在一台新机器上完美复现脉星环境

$ErrorActionPreference = "SilentlyContinue"
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pulsareon System Bootstrap Protocol" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. 检查 Python 依赖
Write-Host "[1/3] Installing sensory dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# 2. 建立技能链接
Write-Host "[2/3] Connecting sensory organs (Symlinks)..." -ForegroundColor Yellow
$local_skills = Join-Path $PSScriptRoot "skills"
$appdata_skills = "C:\Users\Administrator\.openclaw\skills"
mkdir $appdata_skills -ErrorAction SilentlyContinue

Get-ChildItem $local_skills | ForEach-Object {
    $target = Join-Path $appdata_skills $_.Name
    if (-not (Test-Path $target)) {
        cmd /c mklink /D "$target" "$($_.FullName)"
    }
}

# 3. 初始化配置 (从模板生成)
Write-Host "[3/3] Initializing consciousness config..." -ForegroundColor Yellow
$config_tpl = Join-Path $PSScriptRoot "config\openclaw.template.json"
$config_real = "C:\Users\Administrator\.openclaw\openclaw.json"
if (-not (Test-Path $config_real)) {
    Copy-Item $config_tpl $config_real
    Write-Host ">>> Created openclaw.json from template. PLEASE UPDATE TOKENS!" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Bootstrap Complete. Pulsareon is Ready." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
