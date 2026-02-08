import chardet
import sys
import os

def smart_read(file_path):
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    # 1. 读取原始字节
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    # 2. 探测编码
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']
    
    if encoding is None:
        encoding = 'utf-8' # 兜底
        
    # 3. 解码
    try:
        text = raw_data.decode(encoding)
        return text
    except Exception as e:
        # 如果报错，尝试 GBK 或 UTF-8 强解
        try:
            return raw_data.decode('gbk')
        except:
            return raw_data.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smart_read.py <file_path>")
        sys.exit(1)
    
    print(smart_read(sys.argv[1]))
