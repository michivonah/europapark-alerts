import requests
import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook
import time

load_dotenv()

# Global defintions
subscribedAttractions = ["383533", "383530", "323530", "323030", "353030", "393030"]
currentTimes = {}

# Functions
def sendMessage(message):
    webhookUrl = os.getenv('DISCORD_WEBHOOK')
    webhook = DiscordWebhook(url=webhookUrl, content=message)
    response = webhook.execute()

def checkTimes(subscribedAttractions):
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
            if attraction["status"] == "opened":
                if not attraction["code"] in currentTimes: currentTimes[attraction["code"]] = attraction["waitingtime"];
                if currentTimes[attraction["code"]] > attraction["waitingtime"]:
                    sendMessage(f"Waiting time of {attraction['name']} sank to {attraction['waitingtime']} Minutes!")
                elif currentTimes[attraction["code"]] < attraction["waitingtime"]:
                    sendMessage(f"Waiting time for {attraction['name']} increased to {attraction['waitingtime']} Minutes!")
                currentTimes[attraction["code"]] = attraction["waitingtime"]

# Main
if __name__ == '__main__':
    while True:
        checkTimes(subscribedAttractions)
        print(f"Checked for updates at {time.strftime('%H:%M:%S', time.localtime())}")
        time.sleep(30)

