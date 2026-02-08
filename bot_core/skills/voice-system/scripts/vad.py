"""
Voice Activity Detector (VAD) - 基于能量的静音检测
用于在发送音频给 STT 引擎前过滤掉静音片段，节省 Token 和带宽。

原理：
计算音频帧的 RMS (均方根) 能量，如果连续 N 帧超过阈值，则认为有人说话。
"""

import sys
import wave
import struct
import math
import os

def calculate_rms(data):
    """计算音频数据的 RMS 能量"""
    count = len(data) / 2
    format = "%dh" % count
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n
    return math.sqrt(sum_squares / count)

def is_speech(wav_file, threshold=0.01, min_duration=0.5):
    """
    判断 WAV 文件是否包含语音
    :param wav_file: 路径
    :param threshold: 能量阈值 (0.0 - 1.0)
    :param min_duration: 最小语音持续时间 (秒)
    :return: True/False
    """
    if not os.path.exists(wav_file):
        return False
        
    try:
        wf = wave.open(wav_file, 'rb')
        chunk_size = 1024
        sample_rate = wf.getframerate()
        
        speech_frames = 0
        total_frames = 0
        
        while True:
            data = wf.readframes(chunk_size)
            if not data or len(data) < chunk_size * 2:
                break
                
            rms = calculate_rms(data)
            if rms > threshold:
                speech_frames += 1
            
            total_frames += 1
            
        wf.close()
        
        # 计算语音持续时间
        chunk_duration = chunk_size / sample_rate
        speech_duration = speech_frames * chunk_duration
        
        print(f"DEBUG: Speech Duration: {speech_duration:.2f}s (Threshold: {threshold})")
        
        return speech_duration >= min_duration
        
    except Exception as e:
        print(f"VAD Error: {e}")
        return True # 出错默认放行，避免阻塞

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vad.py <wav_file> [threshold]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    thresh = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
    
    if is_speech(file_path, thresh):
        print("SPEECH_DETECTED")
        sys.exit(0)
    else:
        print("SILENCE")
        sys.exit(1)
