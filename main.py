import requests
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

load_dotenv()

endpoint = "https://api.wartezeiten.app/v1/waitingtimes"

header = {
    "language":"de",
    "park":"europapark"
}

req = requests.get(url = endpoint, params = header)

result = req.json()

webhookUrl = os.getenv('DISCORD_WEBHOOK')

webhook = DiscordWebhook(url=webhookUrl, content=result)
response = webhook.execute()
