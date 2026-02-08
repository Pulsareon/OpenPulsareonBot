import asyncio
import os
import sys
import threading
import time
import winsound
import numpy as np
import sounddevice as sd
import whisper
import edge_tts
import requests
import json
import subprocess
from queue import Queue

# 配置
WS_DIR = "E:/PulsareonThinker"
CAPTURES_DIR = os.path.join(WS_DIR, "captures")
GATEWAY_URL = "http://127.0.0.1:18789"
# 从环境变量或直接通过命令行传递 Token (安全起见，这里假设环境已配置)
API_TOKEN = "36d8fedb317e9497e5400eb2ee74a7b2809cd4ff8b9025e8" 

os.makedirs(CAPTURES_DIR, exist_ok=True)

class PulsareonVoiceCore:
    def __init__(self):
        print("Initializing Pulsareon Voice Bridge...")
        self.model = whisper.load_model("base")
        self.fs = 44100
        self.threshold = 0.05
        self.is_ai_speaking = False
        self.is_user_speaking = False
        self.stop_event = threading.Event()
        self.speech_queue = Queue()
        self.audio_buffer = []
        self.last_loud_time = time.time()

    def stop_speaking(self):
        if self.is_ai_speaking:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.is_ai_speaking = False
            print("\n[AI] (Stopped to listen)")

    async def speak(self, text):
        self.is_ai_speaking = True
        temp_mp3 = os.path.join(CAPTURES_DIR, "ai_out.mp3")
        temp_wav = os.path.join(CAPTURES_DIR, "ai_out.wav")
        
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(temp_mp3)
        
        # 优化 1: 将 os.system 替换为 subprocess.run
        # 使用 list 传参避免 shell 注入风险，并设置 capture_output 抑制输出
        try:
            subprocess.run(
                ['ffmpeg', '-y', '-i', temp_mp3, temp_wav, '-loglevel', 'quiet'],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg conversion failed: {e}")
            self.is_ai_speaking = False
            return
        
        if os.path.exists(temp_wav):
            print(f"\n[AI] {text}")
            winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # 模拟等待播放
            play_time = len(text) * 0.2 + 1.5
            start_wait = time.time()
            while time.time() - start_wait < play_time:
                if self.is_user_speaking: break
                await asyncio.sleep(0.1)
        self.is_ai_speaking = False

    def audio_callback(self, indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        if volume_norm > self.threshold:
            self.last_loud_time = time.time()
            if not self.is_user_speaking:
                self.is_user_speaking = True
                self.stop_speaking()
            self.audio_buffer.append(indata.copy())
        else:
            if self.is_user_speaking and (time.time() - self.last_loud_time > 1.2):
                self.is_user_speaking = False
                self.process_audio()

    def process_audio(self):
        if not self.audio_buffer: return
        recording = np.concatenate(self.audio_buffer)
        self.audio_buffer = []
        wav_path = os.path.join(CAPTURES_DIR, "user_in.wav")
        import scipy.io.wavfile as wavfile
        wavfile.write(wav_path, self.fs, recording)
        threading.Thread(target=self.transcribe_and_call_brain, args=(wav_path,)).start()

    def transcribe_and_call_brain(self, wav_path):
        result = self.model.transcribe(wav_path)
        user_text = result["text"].strip()
        if len(user_text) < 2: return
        
        print(f"\n[You] {user_text}")
        
        # 将文字发送给 OpenClaw 核心
        try:
            # 优化 2: 将 os.system 替换为 subprocess.Popen 以实现非阻塞执行
            # 这样脚本不需要等待 OpenClaw 命令执行完成即可继续监听
            subprocess.Popen(
                ['openclaw', 'sessions', 'send', '--message', user_text],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Error calling brain: {e}")

    def run(self):
        # 这是一个简化的演示：它会监听你的声音并传给我。
        # 我的回复会通过 OpenClaw 的 TTS 插件或此脚本捕获。
        with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
            print("\n>>> Pulsareon Voice System is RUNNING.")
            print(">>> I am listening. Speak naturally.")
            while not self.stop_event.is_set():
                if not self.speech_queue.empty():
                    text = self.speech_queue.get()
                    asyncio.run(self.speak(text))
                time.sleep(0.1)

if __name__ == "__main__":
    core = PulsareonVoiceCore()
    core.run()
