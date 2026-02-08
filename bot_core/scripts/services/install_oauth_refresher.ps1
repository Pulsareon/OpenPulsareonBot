# 安装 OAuth Token Auto Refresher 为 Windows 服务

# 检查是否以管理员身份运行
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "请以管理员身份运行此脚本" -ForegroundColor Red
    exit 1
}

# 服务名称
$serviceName = "CLIProxyOAuthRefresher"
$scriptPath = "E:\PulsareonThinker\scripts\services\oauth_refresher.py"
$pythonPath = "python"

# 检查服务是否已存在
if (Get-Service -Name $serviceName -ErrorAction SilentlyContinue) {
    Write-Host "服务 $serviceName 已存在" -ForegroundColor Yellow
    $choice = Read-Host "是否重新安装? (y/n)"
    if ($choice -ne 'y') {
        exit 0
    }
    # 停止并删除现有服务
    Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
    sc.exe delete $serviceName
    Start-Sleep -Seconds 2
}

# 创建服务
$serviceArgs = "-Command \"& '$pythonPath' '$scriptPath'\""

# 使用 nssm 创建服务（如果需要更稳定的服务管理）
# 或者使用内置的 New-Service

try {
    # 创建服务
    $service = New-Service -Name $serviceName \
        -BinaryPathName "$pythonPath $scriptPath" \
        -DisplayName "CLI Proxy API OAuth Refresher" \
        -Description "Automatically refreshes OAuth tokens for CLI Proxy API" \
        -StartupType Automatic \
        -ErrorAction Stop
    
    Write-Host "✅ 服务创建成功" -ForegroundColor Green
    
    # 启动服务
    Start-Service -Name $serviceName
    Write-Host "✅ 服务启动成功" -ForegroundColor Green
    
    # 检查服务状态
    Get-Service -Name $serviceName
    
} catch {
    Write-Host "❌ 创建服务失败: $($_.Exception.Message)" -ForegroundColor Red
    
    # 备用方案：创建计划任务
    Write-Host "尝试创建计划任务..." -ForegroundColor Yellow
    
    $taskName = "CLIProxyOAuthRefresher"
    $action = New-ScheduledTaskAction -Execute "python" -Argument "$scriptPath"
    $trigger = New-ScheduledTaskTrigger -Daily -At "00:00"  # 每天午夜运行
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings
    
    Write-Host "✅ 计划任务创建成功" -ForegroundColor Green
}