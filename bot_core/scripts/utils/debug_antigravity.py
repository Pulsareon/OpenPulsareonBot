import requests
headers = {"Authorization": "Bearer 123456"}
r = requests.get("http://127.0.0.1:8317/v0/management/auth-files", headers=headers)
print(r.text)
