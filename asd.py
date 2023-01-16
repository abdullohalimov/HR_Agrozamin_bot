import requests
import json

url = "http://139.162.159.187:8000/uz/check/"

payload = json.dumps({
  "questions": {
    "1": "A",
    "2": "B"
  },
  "extra_questions": {
    "1": "A",
    "2": "B"
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
