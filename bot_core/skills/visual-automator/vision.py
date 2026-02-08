import requests
import base64
import json
import re

API_URL = "http://127.0.0.1:8317/v1/chat/completions"
MODEL = "gemini-2.5-flash" # Assuming stripped name works, or use full "cli-proxy/gemini-2.5-flash"

def analyze_screenshot(image_path, instruction):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        
    prompt = f"""
    Task: {instruction}
    
    Analyze the UI screenshot.
    1. Locate the specific element mentioned in the task.
    2. Return the CENTER coordinates (x, y) of that element.
    3. If not found, return status "NOT_FOUND".
    
    Output JSON only:
    {{
        "status": "FOUND" or "NOT_FOUND",
        "x": 123,
        "y": 456,
        "confidence": 0.95,
        "reasoning": "Found blue button labeled 'Login'"
    }}
    """
    
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                ]
            }
        ],
        "max_tokens": 300
        # "response_format": {"type": "json_object"} # Not all models support this, parsing manually is safer
    }
    
    try:
        r = requests.post(API_URL, json=data, headers={"Authorization": "Bearer cli-proxy"}, timeout=15)
        if r.status_code != 200:
            return {"status": "ERROR", "reasoning": f"API {r.status_code}: {r.text}"}
            
        res = r.json()
        content = res['choices'][0]['message']['content']
        
        # Extract JSON
        json_str = content
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(json_str)
    except Exception as e:
        print(f"Vision Error: {e}")
        return {"status": "ERROR", "reasoning": str(e)}
