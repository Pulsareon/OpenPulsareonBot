Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run "powershell -NoProfile -ExecutionPolicy Bypass -File E:\PulsareonThinker\scripts\guardian\guardian.ps1", 0
Set WshShell = Nothing
