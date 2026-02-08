import requests
headers = {"Authorization": "Bearer cli-proxy"}
try:
    r = requests.get("http://127.0.0.1:8317/v1/models", headers=headers)
    print(r.text)
except Exception as e:
    print(str(e))
