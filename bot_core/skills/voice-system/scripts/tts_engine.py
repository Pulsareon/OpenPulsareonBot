import asyncio
import edge_tts
import sys
import os
import winsound
import time

async def speak(text, voice="zh-CN-XiaoxiaoNeural"):
    # 临时文件路径
    temp_mp3 = "temp_voice.mp3"
    output_wav = "temp_voice.wav"
    
    try:
        # 1. 合成
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_mp3)
        
        # 2. 转码为 WAV (winsound 最稳)
        # 假设 ffmpeg 已安装在 PATH 中
        os.system(f'ffmpeg -y -i "{temp_mp3}" "{output_wav}" -loglevel quiet')
        
        # 3. 播放
        if os.path.exists(output_wav):
            winsound.PlaySound(output_wav, winsound.SND_FILENAME)
            return True
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return False
    finally:
        # 清理
        for f in [temp_mp3, output_wav]:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        asyncio.run(speak(sys.argv[1]))
