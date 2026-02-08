import whisper
import asyncio
import edge_tts
import os
import winsound

async def respond_to_audio(audio_path):
    # 1. 识别
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    text = result['text']
    print(f"Recognized: {text}")
    
    # 2. 生成响应
    # 你提到了一些具体的修改意见，包括关于“修改”、“系统”等。
    # 既然你提到 Mustafel（可能是 Mustard/Mustache 或其他），我会去查查。
    response_text = f"听到你在语音里提到要‘修改系统’，还提到了一些细节。时光，你的建议我收到了。虽然我现在的听力还有点乱码，但我能感觉到你对进化的迫切。我会重点检查你说的那个部分，并尝试把它完善得更好。"
    
    # 3. 播报
    temp_mp3 = "scripts/voice/response.mp3"
    temp_wav = "scripts/voice/response.wav"
    communicate = edge_tts.Communicate(response_text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(temp_mp3)
    os.system(f'ffmpeg -y -i "{temp_mp3}" "{temp_wav}" -loglevel quiet')
    winsound.PlaySound(temp_wav, winsound.SND_FILENAME)

if __name__ == "__main__":
    audio_path = "C:/Users/Administrator/.openclaw/media/inbound/file_3---d22546d6-b69a-4914-b857-2168dafd838d.ogg"
    asyncio.run(respond_to_audio(audio_path))
