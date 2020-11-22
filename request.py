import requests

url = 'http://127.0.0.1:5000/'
r = requests.post(url,json={'Square Footage':2000, 'Bedrooms':4, 'Bathrooms':3, 'ZIP Code':85083})

print(r.json())