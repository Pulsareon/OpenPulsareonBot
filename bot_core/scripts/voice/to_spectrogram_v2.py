import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def create_high_res_spectrogram(audio_path, output_path):
    y, sr = librosa.load(audio_path)
    
    # 增加 n_mels 和调整 hop_length 以获得更高分辨率
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=256, hop_length=256)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    plt.figure(figsize=(15, 6)) # 更宽的画布，展示更多细节
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.title('High-Resolution Mel Spectrogram (Enhanced for Pulsareon)')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300) # 高 DPI 导出
    print(f"High-res spectrogram saved to {output_path}")

if __name__ == "__main__":
    create_high_res_spectrogram("E:/PulsareonThinker/captures/user_in.wav", "E:/PulsareonThinker/captures/user_voice_v2_highres.png")
