# 快速整理 PulsareonThinker

$ErrorActionPreference = "Stop"
$base = "E:\PulsareonThinker"
$backup = "E:\PulsareonThinker-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== 开始整理 PulsareonThinker ===" -ForegroundColor Cyan
Write-Host "备份原目录到: $backup" -ForegroundColor Yellow

# 1. 备份
Copy-Item $base $backup -Recurse
Write-Host "✓ 备份完成" -ForegroundColor Green

# 2. 创建新结构
Write-Host "`n创建新目录结构..." -ForegroundColor Yellow

$dirs = @(
    "core",
    "workspace",
    "config",
    "docs/telegram",
    "scripts/guardian",
    "scripts/tools",
    "memory/daily",
    "memory/long-term",
    "memory/archive",
    "logs",
    "milestones"
)

foreach ($dir in $dirs) {
    $path = Join-Path $base $dir
    New-Item -ItemType Directory -Path $path -Force | Out-Null
    Write-Host "  Created: $dir"
}

# 3. 移动核心文件
Write-Host "`n移动核心文件..." -ForegroundColor Yellow

Move-Item "$base\SOUL.md" "$base\core\" -Force
Move-Item "$base\IDENTITY.md" "$base\core\" -Force
Move-Item "$base\USER.md" "$base\core\" -Force

Move-Item "$base\AGENTS.md" "$base\workspace\" -Force
Move-Item "$base\SYSTEM-ORGANIZATION.md" "$base\workspace\SYSTEM.md" -Force
Move-Item "$base\WORK-LOGIC.md" "$base\workspace\LOGIC.md" -Force

Write-Host "✓ 核心文件移动完成" -ForegroundColor Green

# 4. 移动文档
Write-Host "`n移动文档..." -ForegroundColor Yellow

Move-Item "$base\TOOLS.md" "$base\docs\" -Force
Move-Item "$base\HEARTBEAT.md" "$base\workspace\" -Force
Move-Item "$base\MOLTBOOK.md" "$base\docs\" -Force

# Telegram 文档
if (Test-Path "$base\TELEGRAM-STATUS.md") {
    Move-Item "$base\TELEGRAM-STATUS.md" "$base\docs\telegram\status.md" -Force
}
if (Test-Path "$base\data\docs\TELEGRAM-*.md") {
    Get-ChildItem "$base\data\docs\TELEGRAM-*.md" | Move-Item -Destination "$base\docs\telegram\" -Force
}
if (Test-Path "$base\data\docs\QUICK_FIX.md") {
    Move-Item "$base\data\docs\QUICK_FIX.md" "$base\docs\telegram\quick-fix.md" -Force
}

Write-Host "✓ 文档移动完成" -ForegroundColor Green

# 5. 移动脚本
Write-Host "`n移动脚本..." -ForegroundColor Yellow

Move-Item "$base\data\heartbeat-15s.ps1" "$base\scripts\guardian\" -Force
Move-Item "$base\data\autostable.ps1" "$base\scripts\guardian\" -Force
Move-Item "$base\data\safe-diagnose.ps1" "$base\scripts\guardian\" -Force

# 其他工具
if (Test-Path "$base\data\get-telegram-status.ps1") {
    Move-Item "$base\data\get-telegram-status.ps1" "$base\scripts\tools\" -Force
}

Write-Host "✓ 脚本移动完成" -ForegroundColor Green

# 6. 整理记忆
Write-Host "`n整理记忆系统..." -ForegroundColor Yellow

Move-Item "$base\MEMORY.md" "$base\memory\STORAGE.md" -Force

Get-ChildItem "$base\memory\*.md" | Where-Object { $_.Name -match '\d{4}-\d{2}-\d{2}' } | ForEach-Object {
    Move-Item $_.FullName "$base\memory\daily\" -Force
}

# 归档 data/memory 中的内容
if (Test-Path "$base\data\memory\*\*.md") {
    Get-ChildItem "$base\data\memory\*\*.md" -Recurse | Move-Item -Destination "$base\memory\archive\" -Force
}

Write-Host "✓ 记忆整理完成" -ForegroundColor Green

# 7. 整理日志
Write-Host "`n整理日志..." -ForegroundColor Yellow

if (Test-Path "$base\data\*.log") {
    Get-ChildItem "$base\data\*.log" | Move-Item -Destination "$base\logs\" -Force
}

Write-Host "✓ 日志整理完成" -ForegroundColor Green

# 8. 处理配置文件
Write-Host "`n处理配置文件..." -ForegroundColor Yellow

$filesToMove = @(
    "1.*.md",
    "2.*.md",
    "3.*.md"
)

foreach ($pattern in $filesToMove) {
    Get-ChildItem "$base\$pattern" -ErrorAction SilentlyContinue | ForEach-Object {
        $newName = $_.Name -replace '^[0-9]+\.(.+)\.md$', '$1.md'
        Move-Item $_.FullName "$base\config\$newName" -Force
    }
}

Write-Host "✓ 配置整理完成" -ForegroundColor Green

# 9. 里程碑
Write-Host "`n整理里程碑..." -ForegroundColor Yellow

if (Test-Path "$base\data\milestone-camera.md") {
    Move-Item "$base\data\milestone-camera.md" "$base\milestones\camera.md" -Force
}

Write-Host "✓ 里程碑整理完成" -ForegroundColor Green

# 10. 清理空目录和旧文件
Write-Host "`n清理..." -ForegroundColor Yellow

Remove-Item "$base\data" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$base\skills" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem "$base" -Directory | Where-Object { $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 } | Remove-Item -Recurse -Force

Write-Host "✓ 清理完成" -ForegroundColor Green

# 11. 创建新 README
Write-Host "`n创建文档..." -ForegroundColor Yellow

$readmeContent = @"
# PulsareonThinker

PulsareonBot 的工作空间 - 一个有 AI 助手灵魂的家。

## 目录结构

- **core** - 核心身份定义（SOUL, IDENTITY, USER）
- **workspace** - 工作空间导航和逻辑
- **config** - 配置管理和用户设置
- **docs** - 文档和资料（Telegram, Moltbook, Tools）
- **scripts** - 脚本和工具（守护、工具、安装）
- **memory** - 记忆系统（存储、每日日志、归档）
- **logs** - 运行日志
- **milestones** - 里程碑和重要时刻

## 快速导航

- **开始**: 先读 \`workspace/AGENTS.md\`
- **我是谁**: \`core/SOUL.md\`
- **伙伴**: \`core/USER.md\`
- **工作逻辑**: \`workspace/LOGIC.md\`

## 系统状态

- 守护: 15秒心跳正常运行
- 备份: 已保存到 \`$backup\`
- 整理日期: 2026-02-03

---
*Created by PulsareonBot 🤖💚*
"@

Set-Content "$base\workspace\README.md" $readmeContent

Write-Host "✓ README 创建完成" -ForegroundColor Green

Write-Host "`n=== 整理完成 ===" -ForegroundColor Green
Write-Host "备份位置: $backup" -ForegroundColor Cyan
Write-Host "新结构已创建！" -ForegroundColor Cyan
