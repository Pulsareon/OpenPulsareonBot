import whisper
import sys
import os

def transcribe_local(file_path):
    print(f"Loading Whisper model...")
    # 使用 base 模型，兼顾速度和准确度
    model = whisper.load_model("base")
    print(f"Transcribing {file_path}...")
    result = model.transcribe(file_path)
    print("--- RESULT START ---")
    print(result["text"])
    print("--- RESULT END ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_transcribe.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    transcribe_local(file_path)
