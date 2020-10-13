import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.put(BASE + "videos/1", {"likes": 10, "name": "My video", "views": 2})
# print(response.json())


response = requests.get(BASE + "videos/2")
print(response.json())