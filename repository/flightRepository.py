import requests

API_KEY = '68bfd888cfda82e2270a0042'  # replace with your key
origin = 'MAD'
destination = 'LON'
departure_date = '2025-10-01'
adults = 1
children = 0
infants = 0
cabin_class = 'Economy'
currency = 'EUR'

url = (
    f"https://api.flightapi.io/onewaytrip/"
    f"{API_KEY}/{origin}/{destination}/"
    f"{departure_date}/{adults}/{children}/{infants}/{cabin_class}/{currency}"
)

response = requests.get(url)
print(response.status_code)
data = response.json()
print(data)