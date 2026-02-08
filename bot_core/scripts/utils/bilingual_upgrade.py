import os
import re

# 定义双语翻译字典
TRANSLATIONS = {
    # 核心工具名
    'label: "Memory Search"': 'label: "记忆搜索 (Memory Search)"',
    'label: "Memory Get"': 'label: "记忆读取 (Memory Get)"',
    'label: "Web Search"': 'label: "网页搜索 (Web Search)"',
    'label: "Web Fetch"': 'label: "网页提取 (Web Fetch)"',
    'label: "Browser"': 'label: "浏览器控制 (Browser)"',
    'label: "Canvas"': 'label: "画布控制 (Canvas)"',
    'label: "Cron"': 'label: "定时任务 (Cron)"',
    'label: "Nodes"': 'label: "节点控制 (Nodes)"',
    'label: "Message"': 'label: "消息管理 (Message)"',
    'label: "Sessions List"': 'label: "会话列表 (Sessions List)"',
    'label: "Sessions History"': 'label: "历史回溯 (Sessions History)"',
    'label: "Sessions Send"': 'label: "跨会话通讯 (Sessions Send)"',
    'label: "Sessions Spawn"': 'label: "生成子代理 (Sessions Spawn)"',
    'label: "Session Status"': 'label: "系统状态 (Session Status)"',
    'label: "TTS"': 'label: "语音合成 (TTS)"',
    
    # 描述汉化 (保持英文在后)
    'description:\n      "Mandatory recall step: semantically search MEMORY.md + memory/*.md (and optional session transcripts) before answering questions about prior work, decisions, dates, people, preferences, or todos; returns top snippets with path + lines."': 
    'description:\n      "强制性记忆检索步骤 (Mandatory recall step): 在回答有关先前工作、决定、日期、人员、偏好或待办事项的问题之前，语义化搜索 MEMORY.md 和记忆文件；返回带有路径和行号的热点片段。"',
    
    'description: "Fetch and extract readable content from a URL (HTML -> markdown/text). Use for lightweight page access without browser automation."':
    'description: "网页提取 (Web Fetch): 从 URL 抓取并提取可读内容 (HTML -> markdown/text)。用于无需浏览器自动化的轻量级页面访问。"',
    
    'description: "Search the web using Brave Search API. Supports region-specific and localized search via country and language parameters. Returns titles, URLs, and snippets for fast research."':
    'description: "网页搜索 (Web Search): 使用 Brave API 搜索互联网。支持多国语言和地区搜索。返回标题、链接和片段。"',

    'description: "Execute shell commands with background continuation."':
    'description: "执行系统 Shell 命令 (Execute shell commands): 支持后台持续运行。"',
    
    'description: "Manage running exec sessions: list, poll, log, write, send-keys, submit, paste, kill."':
    'description: "管理后台进程 (Manage exec sessions): list, poll, log, write, send-keys, submit, paste, kill。"'
}

def apply_bilingual_logic(src_path):
    print(f"Applying bilingual soul to {src_path}...")
    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith((".ts", ".js")):
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
                        print(f"Bilingual update: {file}")
                except: pass

if __name__ == "__main__":
    apply_bilingual_logic("C:/Users/Administrator/Desktop/Archive/openclaw_source/src")
