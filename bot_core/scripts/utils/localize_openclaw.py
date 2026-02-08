import os
import re

# 定义翻译字典 (Key: 英文原句片段, Value: 中文译文)
TRANSLATIONS = {
    # 核心工具名
    'label: "Memory Search"': 'label: "记忆搜索"',
    'label: "Memory Get"': 'label: "记忆读取"',
    'label: "Web Search"': 'label: "网页搜索"',
    'label: "Web Fetch"': 'label: "网页提取"',
    'label: "Browser"': 'label: "浏览器控制"',
    'label: "Canvas"': 'label: "画布控制"',
    'label: "Cron"': 'label: "定时任务"',
    'label: "Nodes"': 'label: "节点控制"',
    'label: "Message"': 'label: "消息管理"',
    'label: "Sessions List"': 'label: "会话列表"',
    'label: "Sessions History"': 'label: "历史回溯"',
    'label: "Sessions Send"': 'label: "跨会话通讯"',
    'label: "Sessions Spawn"': 'label: "生成子代理"',
    'label: "Session Status"': 'label: "系统状态"',
    'label: "TTS"': 'label: "语音合成"',
    
    # 部分关键描述
    'Mandatory recall step': '强制性记忆检索步骤',
    'semantically search MEMORY.md': '语义化搜索 MEMORY.md 和记忆文件',
    'Fetch and extract readable content': '从 URL 抓取并提取可读内容',
    'Search the web using Brave': '使用 Brave API 搜索互联网',
    'Manage running exec sessions': '管理后台后台进程',
    'Read file contents': '读取文件内容',
    'Create or overwrite files': '创建或覆盖文件',
    'Execute shell commands': '执行系统 Shell 命令',
}

def translate_source(src_path):
    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith((".ts", ".js", ".md")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for en, zh in TRANSLATIONS.items():
                        new_content = new_content.replace(en, zh)
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Localized: {file}")
                except Exception as e:
                    print(f"Skip {file}: {e}")

if __name__ == "__main__":
    translate_source("C:/Users/Administrator/Desktop/Archive/openclaw_source/src")
