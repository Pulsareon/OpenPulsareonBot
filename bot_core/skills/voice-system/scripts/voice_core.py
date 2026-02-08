"""
Pulsareon 语音核心 V3 (Final)
最稳健的实现：SoundDevice录音 -> Numpy增益 -> SpeechRecognition识别
不依赖 PyAudio。
"""
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import numpy as np
import wave
import os
import sys
import time
from datetime import datetime

# 强制UTF-8
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_FILE = "E:/PulsareonThinker/voice_chat/input_v3.wav"
SAMPLE_RATE = 44100
CHANNELS = 1

def speak(engine, text):
    if not text: return
    print(f"🗣️ [AI] {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def normalize(audio_data):
    """把声音放大到最大音量的 80%"""
    peak = np.max(np.abs(audio_data))
    if peak == 0: return audio_data
    
    target = 26000 # ~80% of 32767
    gain = target / peak
    gain = min(gain, 20.0) # 最多放大20倍
    
    if gain > 1.2:
        # print(f"   [增益] 放大 {gain:.1f} 倍")
        return (audio_data * gain).astype(np.int16)
    return audio_data

def record_audio(duration=3, threshold=0):
    """
    强制录音模式 (调试用)
    """
    print(f"\n🔴 强制录音 {duration}s...", end="", flush=True)
    
    # 2. 正式录音
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    sd.wait()
    
    # 计算峰值看看
    peak = np.max(np.abs(recording)) * 32767
    print(f" (峰值: {int(peak)})", end="")
    
    # 3. 处理
    audio_int16 = np.int16(recording * 32767)
    audio_norm = normalize(audio_int16)
    
    # 保存
    with wave.open(OUTPUT_FILE, 'w') as f:
        f.setnchannels(CHANNELS)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_norm.tobytes())
        
    return OUTPUT_FILE

def main():
    print("=" * 60)
    print("⚡ Pulsareon 语音助手 V3 (Final)")
    print("=" * 60)

    # 初始化 TTS
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        for v in engine.getProperty('voices'):
            if 'chinese' in v.name.lower() or 'cn' in v.id.lower():
                engine.setProperty('voice', v.id)
                break
    except:
        engine = None
        print("[警告] TTS不可用")

    recognizer = sr.Recognizer()
    
    print("🎤 系统就绪。请说话...")
    
    while True:
        try:
            # 录音 (降低阈值到600)
            wav_path = record_audio(duration=4, threshold=600)
            
            if wav_path:
                # 识别
                # print("   识别中...", end="", flush=True)
                with sr.AudioFile(wav_path) as source:
                    audio = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio, language='zh-CN')
                        print(f"👤 [你] {text}")
                        
                        # 回复逻辑
                        reply = ""
                        if "你好" in text: reply = "你好呀！"
                        elif "几点" in text: reply = f"现在是{datetime.now().strftime('%H点%M分')}"
                        elif "再见" in text: 
                            speak(engine, "再见。")
                            break
                        else:
                            reply = f"收到：{text}"
                        
                        speak(engine, reply)
                        
                    except sr.UnknownValueError:
                        print("❌ (未识别)")
                    except sr.RequestError:
                        print("⚠️ (网络错误)")
            else:
                # 没听到声音，稍微休息一下避免CPU空转
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[错误] {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
