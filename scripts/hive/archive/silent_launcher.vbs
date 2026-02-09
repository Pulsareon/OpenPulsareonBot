Set WshShell = CreateObject("WScript.Shell")
' 0 = 隐藏窗口, False = 不等待结束
WshShell.Run "node.exe E:\PulsareonThinker\scripts\hive\node_resilience_node.js", 0, False
