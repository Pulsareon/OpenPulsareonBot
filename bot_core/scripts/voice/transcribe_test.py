import requests
import sys

def transcribe(file_path):
    url = "http://127.0.0.1:8317/v1/audio/transcriptions"
    files = {'file': open(file_path, 'rb')}
    data = {'model': 'whisper-1'}
    headers = {'Authorization': 'Bearer cli-proxy'}
    
    try:
        response = requests.post(url, files=files, data=data, headers=headers)
        if response.status_code == 200:
            print(response.json().get('text', 'No text found'))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <file_path>")
        sys.exit(1)
    transcribe(sys.argv[1])
