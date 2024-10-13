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
                try:
                    response = requests.post(url=endpoint, headers=header, data=message)
                except Exception as error:
                    raise Exception(f"Got an error while sending the notification: {error}")
            else:
                try:
                    response = requests.post(url=endpoint, data=message)
                except Exception as error:
                    raise Exception(f"Got an error while sending the notification: {error}")
            return response
        case "discord" | _:
            endpoint = os.getenv('DISCORD_WEBHOOK')
            data = {
                "content": message,
            }
            try:
                response = requests.post(url=endpoint, json=data)
                return response
            except Exception as error:
                raise Exception(f"Got an error while sending the notification: {error}")

# Check for the current waiting times
def checkTimes(subscribedAttractions, themepark):
    try:
        endpoint = "https://api.wartezeiten.app/v1/waitingtimes"

        header = {
            "language":"de",
            "park":themepark
        }

        req = requests.get(url=endpoint, headers=header)
    except:
        raise Exception(f"API Request to endpoint {endpoint} failed.")
    try:
        result = req.json()
    except:
        raise Exception("Format of API response is invalid. (JSON expected)")
    try:
        attractions = result
        for attraction in attractions:
            if isinstance(attraction, dict) and "code" in attraction:
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
            else:
                print(f"Info: Attraction was skipped because it has an invalid data structure. Affected attraction: {attraction}")
    except Exception as error:
        raise Exception(f"Got an error while checking for differences since the last API call. Error: {error}")

# Main Loop
# Checks every 30 seconds for changes in the waiting times of the subscribed attractions
# If some attractions are closed the check will only be executed every 180 seconds
if __name__ == '__main__':
    print("Themepark Wait Time Alerts")
    print("By Michi von Ah")
    print("Big thanks to the wartezeiten.app API!")
    while True:
        try:
            checkTimes(subscribedAttractions, themepark)
            print(f"Checked for updates at {time.strftime('%H:%M:%S', time.localtime())}")
        except Exception as error:
            raise Exception(error)
        time.sleep(refreshTime)

