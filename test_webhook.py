
import requests

url = 'http://127.0.0.1:5001/webhook/review'
data = {
    "customer_name": "John Doe",
    "review_text": "The waffles were amazing and service was excellent!",
    "rating": 5
}

response = requests.post(url, json=data)
print(response.json())
