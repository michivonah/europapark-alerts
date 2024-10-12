# Themepark Wait Time Alerts
# Michi von Ah - October 2023 (Last Updated on October 2024)
# Thanks to https://www.wartezeiten.app/ for their API

import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Global defintions
subscribedAttractions = os.getenv('SUBS').split(",")
currentTimes = {}
refreshTime = int(os.getenv('CHECK_INTERVAL')) if os.getenv('CHECK_INTERVAL') else 30
notificationType = os.getenv('NOTIFICATION_TYPE') if os.getenv('NOTIFICATION_TYPE') else "discord"
themepark = os.getenv('THEMEPARK') if os.getenv('THEMEPARK') else "europapark"

# Send messagess via specified notificationType
def sendMessage(message, notificationType):
    match notificationType.lower():
        case "ntfy":
            endpoint = os.getenv('NTFY_URL')
            accessToken = os.getenv('NTFY_ACCESS_TOKEN')
            if accessToken:
                header = {
                    "Authorization":f"Bearer {accessToken}"
                }
                response = requests.post(url=endpoint, headers=header, data=message)
            else: response = requests.post(url=endpoint, data=message)
            return response
        case "discord" | _:
            endpoint = os.getenv('DISCORD_WEBHOOK')
            data = {
                "content": message,
            }
            response = requests.post(url=endpoint, json=data)
            return response

# Check for the current waiting times
def checkTimes(subscribedAttractions, themepark):
    endpoint = "https://api.wartezeiten.app/v1/waitingtimes"

    header = {
        "language":"de",
        "park":themepark
    }

    req = requests.get(url=endpoint, headers=header)
    result = req.json()
    attractions = result
    for attraction in attractions:
        if attraction["code"] in subscribedAttractions:
            if attraction["status"] == "opened":
                refreshTime = 30
                if not attraction["code"] in currentTimes: currentTimes[attraction["code"]] = attraction["waitingtime"];
                if currentTimes[attraction["code"]] > attraction["waitingtime"]:
                    sendMessage(f"Waiting time of {attraction['name']} sank to {attraction['waitingtime']} Minutes!", notificationType)
                elif currentTimes[attraction["code"]] < attraction["waitingtime"]:
                    sendMessage(f"Waiting time for {attraction['name']} increased to {attraction['waitingtime']} Minutes!", notificationType)
                currentTimes[attraction["code"]] = attraction["waitingtime"]
            else:
                refreshTime = 180

# Main Loop
# Checks every 30 seconds for changes in the waiting times of the subscribed attractions
# If some attractions are closed the check will only be executed every 180 seconds
if __name__ == '__main__':
    print("Themepark Wait Time Alerts")
    print("By Michi von Ah")
    print("Big thanks to the wartezeiten.app API!")
    while True:
        checkTimes(subscribedAttractions, themepark)
        print(f"Checked for updates at {time.strftime('%H:%M:%S', time.localtime())}")
        time.sleep(refreshTime)

