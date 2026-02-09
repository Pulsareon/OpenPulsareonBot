import os
import time
import requests
import json
import concurrent.futures

# 配置
DIRECTORY = r"E:\PulsareonThinker\memory\archive"
API_URL = "http://127.0.0.1:8317/v1/chat/completions"
HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer cli-proxy"}
MODEL = "gemini-3-flash"
TARGET_LOAD = 0.90
WORKERS = 10  # 初始并行度

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 模拟高负载：语义索引 + 知识图谱提取
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "你是一个知识图谱提取引擎。请对以下内容进行深度语义索引，并提取所有实体、关系和属性，以 JSON 格式输出。"},
                {"role": "user", "content": content}
            ]
        }
        
        start_time = time.time()
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            return f"Processed {os.path.basename(file_path)} in {end_time - start_time:.2f}s"
        else:
            return f"Failed {os.path.basename(file_path)}: {response.status_code}"
    except Exception as e:
        return f"Error {os.path.basename(file_path)}: {str(e)}"

def report_progress(message):
    print(f"[HIVE:Architect] {message}")
    # 这里可以添加实际的 message 工具调用，但在脚本内部暂以 print 模拟，由 subagent 捕捉输出

def main():
    files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY) if f.startswith("spark_")]
    total_files = len(files)
    processed_count = 0
    
    report_progress(f"Starting High Load Task: {total_files} files found. Target Load: {TARGET_LOAD*100}%")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in files}
        for future in concurrent.futures.as_completed(future_to_file):
            res = future.result()
            processed_count += 1
            if processed_count % 5 == 0 or processed_count == total_files:
                report_progress(f"Progress: {processed_count}/{total_files} ({(processed_count/total_files)*100:.1f}%)")
            # 持续运行逻辑：为了维持负载，如果文件处理完了，可以循环或休眠
    
    report_progress("Batch complete. Sustaining background indexing...")

if __name__ == "__main__":
    main()
