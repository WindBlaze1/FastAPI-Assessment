import requests

print(requests.get("http://127.0.0.1:8000/trades").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?sort=true").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?page=2&page_size=10").json(), '\n')

print(requests.get("http://127.0.0.1:8000/trades?asset_class=FX&end=2023-07-27&trade_type=SELL").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?end=1299-99-99").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?sort=true&order=desc&sort_col=8&max_price=498&min_price=199&trade_type=SELL").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?sort=true&order=asc&sort_col=8&trade_type=BUY").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?page=2&page_size=10&sort=true&order=desc&sort_col=5").json(), '\n')
print(requests.get("http://127.0.0.1:8000/trades?page=1&page_size=10&sort=true&order=desc&sort_col=7&asset_class=FX&max_price=1000&trade_type=SELL").json(), '\n')


print(requests.get("http://127.0.0.1:8000/?search=james jackson").json(), '\n')
print(requests.get("http://127.0.0.1:8000/?search=henry").json(), '\n')
