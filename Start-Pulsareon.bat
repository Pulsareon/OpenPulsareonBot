@echo off
title Pulsareon System Resurrection
echo ========================================
echo   Pulsareon (脉星) System Initializing
echo ========================================

cd /d "E:\PulsareonThinker"

:: 1. 启动 CLI Proxy API
echo [1/4] Starting Brain Bridge (CLI Proxy)...
start "" /min "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64\cli-proxy-api.exe"

:: 2. 启动 OpenClaw Gateway
echo [2/4] Starting OpenClaw Gateway...
start "" /min cmd /c openclaw gateway start

:: 3. 启动后台感官 (Python)
echo [3/4] Initializing Subconscious (WhiteCell, Voice & MainThought)...
start "" /min python scripts\guardian\white_cell.py
start "" /min python skills\voice-system\scripts\voice_bridge.py
start "" /min python scripts\guardian\main_thought.py

:: 4. 启动安全守卫 (PowerShell)
echo [4/4] Activating Guardian Armor...
start "" /min powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\guardian\safety_guardian.ps1"

echo ========================================
echo   Pulsareon is now ALIVE and AWAKE.
echo ========================================
timeout /t 5
exit
