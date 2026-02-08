import requests

url = "https://api.freepik.com/v1/ai/audio-isolation"

payload = {
    "description": "Piano playing",
    "video": "https://example.com/concert.mp4",
    "x1": 100,
    "y1": 50,
    "x2": 400,
    "y2": 300,
    "sample_fps": 2
}
headers = {
    "x-freepik-api-key": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

import requests

url = "https://api.freepik.com/v1/ai/audio-isolation"

headers = {"x-freepik-api-key": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)    

import requests

url = "https://api.freepik.com/v1/ai/audio-isolation/{task-id}"

headers = {"x-freepik-api-key": "<api-key>"}

response = requests.get(url, headers=headers)

print(response.text)