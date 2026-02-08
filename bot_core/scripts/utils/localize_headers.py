import os

# 补充中英对照：CLI 状态表格表头
BILINGUAL_HEADERS = {
    'header: "Channel"': 'header: "渠道 (Channel)"',
    'header: "Enabled"': 'header: "开启 (Enabled)"',
    'header: "State"': 'header: "状态 (State)"',
    'header: "Detail"': 'header: "详情 (Detail)"',
    'header: "Key"': 'header: "密钥 (Key)"',
    'header: "Kind"': 'header: "类型 (Kind)"',
    'header: "Age"': 'header: "时长 (Age)"',
    'header: "Model"': 'header: "模型 (Model)"',
    'header: "Tokens"': 'header: "令牌 (Tokens)"',
}

def apply_headers(src_path):
    print(f"Applying bilingual headers to {src_path}...")
    for root, _, files in os.walk(src_path):
        for file in files:
            if file.endswith(".ts"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = content
                    for en, zh in BILINGUAL_HEADERS.items():
                        new_content = new_content.replace(en, zh)
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Header Localized: {file}")
                except: pass

if __name__ == "__main__":
    apply_headers("C:/Users/Administrator/Desktop/Archive/openclaw_source/src")
