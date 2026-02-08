import os
import shutil
from datetime import datetime, timedelta

src = r"C:\Users\Administrator\Desktop\TempWork"
dst = r"C:\Users\Administrator\Desktop\Archive"
threshold = datetime.now() - timedelta(days=1)

if not os.path.exists(dst):
    os.makedirs(dst)

for item in os.listdir(src):
    if item.startswith("_"): continue # Skip rule files
    path = os.path.join(src, item)
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    
    if mtime < threshold:
        print(f"Moving {item} (mtime: {mtime}) to Archive...")
        try:
            target_path = os.path.join(dst, item)
            if os.path.exists(target_path):
                target_path += "_" + datetime.now().strftime("%Y%m%d%H%M%S")
            shutil.move(path, target_path)
        except Exception as e:
            print(f"Failed to move {item}: {e}")
