import whisper
import sys
import os

# 全局模型缓存，避免重复加载
_model_cache = None

def get_model():
    global _model_cache
    if _model_cache is None:
        print("Loading Whisper model (base)...")
        _model_cache = whisper.load_model("base")
    return _model_cache

def transcribe(file_path):
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    try:
        model = get_model()
        result = model.transcribe(file_path)
        return result["text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(transcribe(sys.argv[1]))
