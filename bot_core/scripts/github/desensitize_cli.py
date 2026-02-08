import os

def desensitize_source(base_path):
    # 敏感词匹配（基于刚才 GitHub 报出的位置）
    # 我们不仅要改那几行，我们要确保万无一失
    risky_files = [
        "internal/api/handlers/management/api_tools.go",
        "internal/auth/gemini/gemini_auth.go",
        "internal/runtime/executor/gemini_cli_executor.go"
    ]
    
    print(f"Desensitizing source code in {base_path}...")
    for rel_path in risky_files:
        full_path = os.path.join(base_path, rel_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    # 极其暴力的替换逻辑：只要包含 ClientID 或 ClientSecret 赋值的行，都进行脱敏
                    if 'ClientID' in line and '=' in line and '"' in line:
                        line = line.split('=')[0] + '= "REDACTED_BY_PULSAREON"\n'
                    if 'ClientSecret' in line and '=' in line and '"' in line:
                        line = line.split('=')[0] + '= "REDACTED_BY_PULSAREON"\n'
                    new_lines.append(line)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Cleaned: {rel_path}")
            except Exception as e:
                print(f"Error cleaning {rel_path}: {e}")

if __name__ == "__main__":
    desensitize_source("C:/Users/Administrator/Desktop/TempWork/CliProxyForPulsareonBot")
