import asyncio
import edge_tts
import sys
import os
import winsound
import time

async def generate_and_play_wav(text):
    VOICE = "zh-CN-XiaoxiaoNeural"
    # 使用 WAV 格式，winsound 对 WAV 的支持最完美
    output_file = os.path.abspath("scripts/voice/stable_voice.wav")
    
    # 1. 生成语音并直接保存为 WAV (edge-tts 虽然默认是 mp3, 
    # 但我们可以在这里让它生成后用 ffmpeg 转一下，或者直接试试能不能生成 wav)
    # 既然有 ffmpeg 了，我们先生成 mp3 再转 wav
    temp_mp3 = os.path.abspath("scripts/voice/temp.mp3")
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(temp_mp3)
    
    # 2. 使用 ffmpeg 转 wav
    os.system(f'ffmpeg -y -i "{temp_mp3}" "{output_file}" -loglevel quiet')
    
    # 3. 使用 winsound 播放（同步阻塞）
    print(f"Playing with winsound...")
    winsound.PlaySound(output_file, winsound.SND_FILENAME)
    print("Playback finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python voice_stable.py <text>")
        sys.exit(1)
    
    text = sys.argv[1]
    asyncio.run(generate_and_play_wav(text))
