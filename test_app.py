import requests

print(requests.get("http://127.0.0.1:8000/trades").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?sort=true").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?page=2&page_size=10").json(), '\n')


print(requests.get("http://127.0.0.1:8000/?search=bob").json(), '\n')
print(requests.get("http://127.0.0.1:8000/?search=henry").json(), '\n')
