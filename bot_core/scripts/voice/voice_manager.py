import asyncio
import edge_tts
import sys
import os
import subprocess
import time

async def generate_and_play(text):
    VOICE = "zh-CN-XiaoxiaoNeural"
    output_file = os.path.abspath("scripts/voice/temp_voice.mp3")
    
    # 1. 生成语音
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)
    
    # 2. 确保文件已写完
    time.sleep(0.5)
    
    # 3. 使用 PowerShell 播放（阻塞模式，直到播完）
    ps_command = f"$m = New-Object Media.MediaPlayer; $m.Open('{output_file}'); $m.Play(); while($m.Status -ne 'Stopped' -and $m.Position.TotalSeconds -lt 30) {{ Start-Sleep -Milliseconds 100 }}; $m.Close()"
    print(f"Playing with PowerShell...")
    result = subprocess.run(["powershell", "-c", ps_command], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"PS Error: {result.stderr}")
    else:
        print("Playback finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python voice_manager.py <text>")
        sys.exit(1)
    
    text = sys.argv[1]
    asyncio.run(generate_and_play(text))
