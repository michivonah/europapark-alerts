import requests

endpoint = "https://api.wartezeiten.app/v1/waitingtimes"

header = {
    "language":"de",
    "park":"europapark"
}

req = requests.get(url = endpoint, params = header)

result = req.json()

print(result)