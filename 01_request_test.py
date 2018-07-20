import json
import requests

url = "http://localhost:3001/booking/1"

headers = {
    'cache-control': "no-cache",
    }

response = requests.request("GET", url, headers=headers)

print(response.text)
#EOF
