import os
import sys
import json
import whisper
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import time

def omni_process(audio_path):
    print(f"[Omni] Processing: {audio_path}")
    
    # 1. 测量时长与加载音频
    y, sr = librosa.load(audio_path)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # 2. 本地 STT
    model = whisper.load_model("base")
    stt_result = model.transcribe(audio_path)
    stt_text = stt_result["text"].strip()
    
    # 3. 生成语谱图
    img_path = audio_path.replace(".wav", ".png")
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    plt.figure(figsize=(12, 5))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.title(f"Spectrogram (Duration: {duration:.2f}s)")
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    
    # 4. 生成增强报告
    report = {
        "audio_source": audio_path,
        "duration_seconds": round(duration, 2),
        "stt_hypothesis": stt_text,
        "spectrogram_path": img_path,
        "timestamp": time.time(),
        "advice": "When sending to Vision model, emphasize the duration for rhythm calibration."
    }
    
    report_path = "E:/PulsareonThinker/data/state/latest_omni_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[Omni] Process Complete. Duration: {duration:.2f}s")
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        omni_process(sys.argv[1])
