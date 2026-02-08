import asyncio
import edge_tts
import sys
import os

async def generate_voice(text, output_file):
    # 选择一个中文声音
    VOICE = "zh-CN-XiaoxiaoNeural"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python edge_tts_test.py <text> <output_path>")
        sys.exit(1)
    
    text = sys.argv[1]
    output_path = sys.argv[2]
    
    asyncio.run(generate_voice(text, output_path))
