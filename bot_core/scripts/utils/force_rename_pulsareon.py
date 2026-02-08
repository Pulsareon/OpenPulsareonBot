import os

def rename_pulsareon_to_pulsareon(base_path):
    print(f"Renaming 'pulsareon' to 'pulsareon' in {base_path}...")
    for root, dirs, files in os.walk(base_path):
        # 1. 替换文件内容
        for file in files:
            if file.endswith((".md", ".py", ".json", ".bat", ".ps1")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 区分大小写进行替换
                    new_content = content.replace("pulsareon", "pulsareon").replace("Pulsareon", "Pulsareon")
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Replaced: {file}")
                except:
                    pass
        
        # 2. 替换文件名 (如果包含 pulsareon)
        for file in files:
            if "pulsareon" in file.lower():
                old_file_path = os.path.join(root, file)
                new_file_name = file.replace("pulsareon", "pulsareon").replace("Pulsareon", "Pulsareon")
                new_file_path = os.path.join(root, new_file_name)
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed file: {file} -> {new_file_name}")
                except:
                    pass

if __name__ == "__main__":
    rename_pulsareon_to_pulsareon("E:/PulsareonThinker")
    rename_pulsareon_to_pulsareon("C:/Users/Administrator/Desktop/TempWork/OpenPulsareonBot")
