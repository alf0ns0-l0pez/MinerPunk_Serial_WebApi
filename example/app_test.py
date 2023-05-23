import requests

url = "http://localhost:9000/get_complete"

payload = {"serial_name": "COM6"}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)