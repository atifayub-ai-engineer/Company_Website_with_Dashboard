import requests


data = requests.get('http://127.0.0.1:8000/sdata/')
showall = data.text
print(showall)