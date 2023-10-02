import requests
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

load_dotenv()

# Global defintions
subscribedAttractions = ["383533", "383530", "323530", "323030", "353030", "393030"]
waitingtimeAlert = 30

# Functions
def sendMessage(message):
    webhookUrl = os.getenv('DISCORD_WEBHOOK')
    webhook = DiscordWebhook(url=webhookUrl, content=message)
    response = webhook.execute()

def checkTimes(subscribedAttractions, alertlimit):
    endpoint = "https://api.wartezeiten.app/v1/waitingtimes"

    header = {
        "language":"de",
        "park":"europapark"
    }

    req = requests.get(url = endpoint, headers = header)
    result = req.json()
    attractions = result
    for attraction in attractions:
        if attraction["code"] in subscribedAttractions:
            if attraction["waitingtime"] < waitingtimeAlert and attraction["status"] == "opened":
                sendMessage(f"Waiting time of {attraction['name']} less than {waitingtimeAlert} Minutes!")

# Main
if __name__ == '__main__':
    checkTimes(subscribedAttractions, waitingtimeAlert)

