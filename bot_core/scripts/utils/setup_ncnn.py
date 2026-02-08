import requests
import os
import subprocess

def download_file(url, local_filename):
    print(f"Downloading {url}...")
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def setup_ncnn_model():
    # 正确的 URL
    url = "https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-streaming-zipformer-zh-14-2023-02-23.tar.bz2"
    target_dir = "skills/voice-system/models"
    os.makedirs(target_dir, exist_ok=True)
    
    local_archive = os.path.join(target_dir, "zipformer_zh.tar.bz2")
    
    try:
        download_file(url, local_archive)
        print("Download finished. Extracting...")
        
        # 使用 tar 命令解压
        cmd = f'tar -xf "{local_archive}" -C "{target_dir}"'
        subprocess.run(cmd, shell=True, check=True)
        print("Model ready!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_ncnn_model()
