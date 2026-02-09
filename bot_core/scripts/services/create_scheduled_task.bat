@echo off
echo Creating scheduled task for OAuth token refresh...

REM 创建计划任务，每小时运行一次
schtasks /create /tn "CLIProxyOAuthRefresher" /tr "python E:\PulsareonThinker\scripts\services\oauth_refresher.py once" /sc hourly /mo 1 /ru SYSTEM

echo Scheduled task created successfully!
echo Task will run every hour to refresh OAuth tokens.