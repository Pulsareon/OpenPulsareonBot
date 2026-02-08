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
from queue import Queue

# 路径配置
WS_DIR = "E:/PulsareonThinker"
CAPTURES_DIR = os.path.join(WS_DIR, "captures")
os.makedirs(CAPTURES_DIR, exist_ok=True)

class PulsareonVoiceCore:
    def __init__(self):
        print("Initializing Pulsareon Voice Core V2 (Full-Duplex)...")
        self.model = whisper.load_model("base")
        self.fs = 44100
        self.threshold = 0.05
        self.is_ai_speaking = False
        self.is_user_speaking = False
        self.stop_event = threading.Event()
        self.speech_queue = Queue()
        
        # 录音缓冲区
        self.audio_buffer = []
        self.silence_start_time = None
        self.last_loud_time = time.time()

    def stop_speaking(self):
        """强行打断 AI 说话"""
        if self.is_ai_speaking:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.is_ai_speaking = False
            print("\n[AI] (Shutting up due to interruption)")

    async def generate_and_play(self, text):
        """生成并播放声音"""
        self.is_ai_speaking = True
        temp_mp3 = os.path.join(CAPTURES_DIR, "ai_out.mp3")
        temp_wav = os.path.join(CAPTURES_DIR, "ai_out.wav")
        
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(temp_mp3)
        
        # 转码
        os.system(f'ffmpeg -y -i "{temp_mp3}" "{temp_wav}" -loglevel quiet')
        
        if os.path.exists(temp_wav) and not self.is_user_speaking:
            print(f"\n[AI] {text}")
            # SND_ASYNC 允许并发
            winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
            
            # 等待播放完成或被打断
            # 简单的估算播放时间：文字长度 * 0.25秒
            play_time = len(text) * 0.25 + 1
            for _ in range(int(play_time * 10)):
                if not self.is_ai_speaking or self.is_user_speaking:
                    break
                await asyncio.sleep(0.1)
        
        self.is_ai_speaking = False

    def audio_callback(self, indata, frames, time_info, status):
        """实时音频监听回调"""
        volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
        
        if volume_norm > self.threshold:
            # 检测到用户声音
            self.last_loud_time = time.time()
            if not self.is_user_speaking:
                print("\n[User] (Speaking...)")
                self.is_user_speaking = True
                # 如果 AI 正在说话，立刻掐断
                if self.is_ai_speaking:
                    self.stop_speaking()
            
            self.audio_buffer.append(indata.copy())
        else:
            # 静音状态
            if self.is_user_speaking:
                if time.time() - self.last_loud_time > 1.2: # 1.2秒静音认为说话结束
                    self.is_user_speaking = False
                    print("[User] (Finished speaking)")
                    self.process_audio()

    def process_audio(self):
        """识别并处理音频"""
        if not self.audio_buffer: return
        
        # 保存录音文件进行识别
        recording = np.concatenate(self.audio_buffer)
        self.audio_buffer = []
        
        wav_path = os.path.join(CAPTURES_DIR, "user_in.wav")
        import scipy.io.wavfile as wavfile
        scipy.io.wavfile.write(wav_path, self.fs, recording)
        
        # 启动识别线程
        threading.Thread(target=self.transcribe_and_respond, args=(wav_path,)).start()

    def transcribe_and_respond(self, wav_path):
        """识别、思考、并加入播放队列"""
        result = self.model.transcribe(wav_path)
        user_text = result["text"].strip()
        
        if len(user_text) < 2: return # 过滤噪音
        
        print(f"I heard: {user_text}")
        
        # 这里原本应该调用 LLM，现在简单做个 Echo 演示
        # 在实际 Skill 中，这里会发回给 OpenClaw 核心
        response = f"听到你说：{user_text}。感觉我们的全双工系统已经开始工作了！"
        self.speech_queue.put(response)

    def run(self):
        """主运行循环"""
        with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs):
            print("\n>>> Pulsareon Voice Interface is ACTIVE.")
            print(">>> Threshold: {:.4f}. You can speak anytime.".format(self.threshold))
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            while not self.stop_event.is_set():
                if not self.speech_queue.empty():
                    text = self.speech_queue.get()
                    loop.run_until_complete(self.generate_and_play(text))
                time.sleep(0.1)

if __name__ == "__main__":
    core = PulsareonVoiceCore()
    try:
        core.run()
    except KeyboardInterrupt:
        print("Stopping...")
