import os

def fix_doubled_name(base_path):
    print(f"Fixing doubled names in {base_path}...")
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 将多出来的 'eon' 减掉
                new_content = content.replace("pulsareon", "pulsareon").replace("Pulsareon", "Pulsareon")
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed: {file}")
            except:
                pass
        
        # 修复文件名
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
    fix_doubled_name("E:/PulsareonThinker")
    fix_doubled_name("C:/Users/Administrator/Desktop/TempWork/OpenPulsareonBot")
