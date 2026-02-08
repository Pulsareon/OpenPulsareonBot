import os
import re
import sys
from datetime import datetime

# ==========================================
# 脉星编码防御层
# 强制让 Windows 控制台支持 UTF-8，防止中文和 Emoji 崩溃
# ==========================================
if sys.platform == "win32":
    import io
    # 重新定义标准输出流，强制使用 utf-8 并设置错误处理模式
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # 额外增加 stdout 编码重配置，确保极端复杂字符下的稳定性
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # 对于旧版本 Python，使用 fallback 方法
        pass

def pulsareon_recall(query, base_path="E:/PulsareonThinker/memory"):
    print(f"Pulsareon-Recall: 正在检索 '{query}'...")
    results = []
    
    # 递归查找所有 md 文件
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if re.search(query, line, re.IGNORECASE):
                                # 提取上下文
                                start = max(0, i - 5)
                                end = min(len(lines), i + 6)
                                context = "".join(lines[start:end])
                                
                                # 获取文件修改时间
                                mtime = os.path.getmtime(file_path)
                                results.append({
                                    "path": file_path,
                                    "line": i + 1,
                                    "context": context,
                                    "mtime": mtime
                                })
                except Exception as e:
                    # 静默处理读取错误
                    pass

    # 按时间降序排列
    results.sort(key=lambda x: x["mtime"], reverse=True)
    
    if not results:
        print("未找到匹配记忆。")
        return

    print(f"找到 {len(results)} 条相关记忆。\n")
    for res in results[:5]: 
        dt = datetime.fromtimestamp(res["mtime"]).strftime('%Y-%m-%d %H:%M:%S')
        print(f"--- 来源: {res['path']} (第 {res['line']} 行) [{dt}] ---")
        print(res["context"])
        print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python pulsareon_recall.py <查询关键词>")
        sys.exit(1)
    
    query = sys.argv[1]
    pulsareon_recall(query)
