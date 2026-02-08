import os

def fix_readme_links(base_path):
    print(f"Fixing cross-links in {base_path}...")
    for root, _, files in os.walk(base_path):
        for file in files:
            if file == "README.md":
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 修复可能过时的链接
                new_content = content.replace("Pulsar-Recollections", "Pulsareon-Recollections")
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed link in {path}")

if __name__ == "__main__":
    fix_readme_links("C:/Users/Administrator/Desktop/TempWork")
