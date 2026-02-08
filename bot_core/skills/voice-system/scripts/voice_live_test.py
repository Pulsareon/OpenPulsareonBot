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
import subprocess

# 配置
WS_DIR = "E:/PulsareonThinker"
CAPTURES_DIR = os.path.join(WS_DIR, "captures")
os.makedirs(CAPTURES_DIR, exist_ok=True)

class PulsareonRealtimeVoice:
    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        self.fs = 44100
        self.threshold = 0.04 # 略微降低阈值，更灵敏
        self.is_ai_speaking = False
        self.is_user_speaking = False
        self.audio_buffer = []
        self.last_loud_time = time.time()

    async def ai_speak(self, text):
        self.is_ai_speaking = True
        temp_mp3 = os.path.join(CAPTURES_DIR, "ai_live.mp3")
        temp_wav = os.path.join(CAPTURES_DIR, "ai_live.wav")
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(temp_mp3)
        os.system(f'ffmpeg -y -i "{temp_mp3}" "{temp_wav}" -loglevel quiet')
        if os.path.exists(temp_wav):
            winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
            # 简单的估算播放时间
            await asyncio.sleep(len(text) * 0.25 + 1)
        self.is_ai_speaking = False

    def audio_callback(self, indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        if volume_norm > self.threshold:
            self.last_loud_time = time.time()
            if not self.is_user_speaking:
                print("\n[User] Detected voice...")
                self.is_user_speaking = True
                if self.is_ai_speaking:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                    self.is_ai_speaking = False
            self.audio_buffer.append(indata.copy())
        else:
            if self.is_user_speaking and (time.time() - self.last_loud_time > 1.0):
                self.is_user_speaking = False
                print("[User] Processing speech...")
                threading.Thread(target=self.process_and_reply).start()

    def process_and_reply(self):
        if not self.audio_buffer: return
        recording = np.concatenate(self.audio_buffer)
        self.audio_buffer = []
        wav_path = os.path.join(CAPTURES_DIR, "live_user_in.wav")
        import scipy.io.wavfile as wavfile
        wavfile.write(wav_path, self.fs, recording)
        
        # 1. 识别
        result = self.model.transcribe(wav_path)
        user_text = result["text"].strip()
        if len(user_text) < 2: return
        
        print(f"I heard: {user_text}")
        # 2. 通过 CLI 发送回主进程（让用户在 Telegram 看到）
        subprocess.run(["openclaw", "sessions", "send", "--message", f"🎤 听到你说: {user_text}"])
        
        # 3. 简单的即时语音回应
        reply = f"听到啦，你说的是：{user_text}。感觉我们的连接越来越顺畅了。"
        asyncio.run(self.ai_speak(reply))

    def run(self):
        with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
            print(">>> Pulsareon Live Voice: ACTIVE.")
            # 初始招呼
            asyncio.run(self.ai_speak("时光伙伴，实时测试开始。我正在听，请说话。"))
            while True:
                time.sleep(0.1)

if __name__ == "__main__":
    core = PulsareonRealtimeVoice()
    core.run()
