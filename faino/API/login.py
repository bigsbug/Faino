import requests

url = 'http://127.0.0.1:8000/api/token/'
username = 'nova'
password = 'novaman'
payload = {"username": username, "password": password}

data = requests.post(url, payload).json()
print()
print(data['access'])
print()
