import requests
import tarfile
import os

def download_model():
    url = "https://github.com/k2-fsa/sherpa-ncnn/releases/download/models/sherpa-ncnn-streaming-zipformer-zh-14-2023-02-23.tar.bz2"
    target_dir = "skills/voice-system/models"
    target_file = os.path.join(target_dir, "model.tar.bz2")
    
    print(f"Downloading model from {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete. Extracting...")
        # 注意：tarfile 需要处理 bz2
        import subprocess
        # Windows 自带 tar 命令通常可以处理大部分格式，或者直接用 Python 解压
        os.system(f'tar -xf "{target_file}" -C "{target_dir}"')
        print("Extraction complete!")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    download_model()
