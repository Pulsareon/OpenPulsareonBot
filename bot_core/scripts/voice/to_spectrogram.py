import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def create_spectrogram(audio_path, output_path):
    print(f"Loading {audio_path}...")
    y, sr = librosa.load(audio_path)
    
    # 计算梅尔语谱图
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # 绘图
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    
    plt.savefig(output_path)
    print(f"Spectrogram saved to {output_path}")

if __name__ == "__main__":
    audio = "E:/PulsareonThinker/captures/user_in.wav"
    output = "E:/PulsareonThinker/captures/user_voice_vision.png"
    create_spectrogram(audio, output)
