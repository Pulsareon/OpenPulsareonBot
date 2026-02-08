import requests
import os

def download_from_hf():
    # 这是一个确认有效的 HF 地址
    url = "https://huggingface.co/csukuangfj/sherpa-ncnn-streaming-zipformer-zh-14-2023-02-23/resolve/main/sherpa-ncnn-streaming-zipformer-zh-14-2023-02-23.tar.bz2"
    target_path = "skills/voice-system/models/zipformer_hf.tar.bz2"
    
    print(f"Downloading from HF: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Success!")
    else:
        print(f"Failed: {response.status_code}")

if __name__ == "__main__":
    download_from_hf()
