
import os
import sys
import subprocess
from datetime import datetime

def handle_hook(event):
    # 获取消息文本
    message = event.get('message', {}).get('text', '')
    
    if message.strip().lower() == '/snap':
        # 1. 执行截图/拍照脚本
        snap_script = r"E:\PulsareonThinker\scripts\vision\take_photo.py"
        try:
            # 运行截图并捕获输出路径
            result = subprocess.check_output(['python', snap_script], creationflags=0x08000000).decode('utf-8').strip()
            
            # 如果输出不是有效文件路径，可能出错了
            if not os.path.exists(result):
                return {"intercept": True, "reply": f"拍摄失败，未找到输出文件: {result}"}

            # 2. 发送回 Telegram
            subprocess.run([
                'openclaw', 'message', 'send', 
                '--to', '5836581389', 
                '--filePath', result, 
                '--message', f'📸 [Pulsareon Snap] Captured at {datetime.now().strftime("%H:%M:%S")}'
            ], creationflags=0x08000000)
            
            return {"intercept": True, "reply": "正在调用视觉神经...⚡️"}
        except Exception as e:
            return {"intercept": True, "reply": f"视觉系统异常: {str(e)}"}
            
    return {"intercept": False}

if __name__ == "__main__":
    pass
