import asyncio
import edge_tts
import os
import winsound
import time
import subprocess

# 全局播放标志
_current_process = None

async def generate_and_play_async(text, voice="zh-CN-XiaoxiaoNeural"):
    global _current_process
    temp_mp3 = os.path.abspath("scripts/voice/duplex_temp.mp3")
    temp_wav = os.path.abspath("scripts/voice/duplex_temp.wav")
    
    # 1. 合成
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(temp_mp3)
    
    # 2. 转码
    os.system(f'ffmpeg -y -i "{temp_mp3}" "{temp_wav}" -loglevel quiet')
    
    # 3. 异步播放
    if os.path.exists(temp_wav):
        print(f"AI Speaking: {text}")
        # 使用 winsound 的异步标志 SND_ASYNC (1)
        # 这样 Python 脚本会立即继续执行，不会等待播完
        winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)

def stop_speaking():
    # 播放一段静音或传入 None 来停止当前异步播放
    winsound.PlaySound(None, winsound.SND_PURGE)
    print("AI Interrupted.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        asyncio.run(generate_and_play_async(sys.argv[1]))
        # 模拟 2 秒后突然被打断
        # time.sleep(2)
        # stop_speaking()
