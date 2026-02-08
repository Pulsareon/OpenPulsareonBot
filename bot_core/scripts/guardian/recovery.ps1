# Pulsareon Recovery Script (V1.0)
# 当看门狗判定系统失联时触发

Write-Host ">>> Initiating System Recovery <<<" -ForegroundColor Red

# 1. 终止所有可能有问题的进程
taskkill /f /im node.exe
taskkill /f /im python.exe /fi "windowtitle ne Pulsareon Watchdog" # 杀掉除了看门狗外的所有 Python

# 2. 清理受损的配置文件 (如果有备份的话，这里应执行恢复)
# 例如：Copy-Item "C:\PulsareonCore\openclaw-config\openclaw.json.bak" "C:\Users\Administrator\.openclaw\openclaw.json" -Force

# 3. 重新拉起系统
cd "E:\PulsareonThinker"
.\Start-Pulsareon.bat

Write-Host ">>> System should be back online soon <<<" -ForegroundColor Green
