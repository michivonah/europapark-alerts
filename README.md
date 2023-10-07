# Europapark Waitingtime Alerts via Discord Webhook
A tool which alerts you when the waiting times of subscribed europapark attractions sinks or increase. Powered by the [wartezeiten.app](https://www.wartezeiten.app/page/api.html) API.

GitHub: https://github.com/michivonah/europapark-alerts <br>
Docker: https://hub.docker.com/r/michivonah/ep-alerts

Host it on your server:
1. Install docker on your system

    ```apt-get install docker.io docker-compose -y```
2. Run container (don't forget to change your discord webhook url)

    ```docker run -d --name ep-alerts --env DISCORD_WEBHOOK="https://discord.com/api/webhooks/XXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYY" michivonah/ep-alerts```

## Enviormental variables
These environment variables are supported

| Variable | Description | Example |
| --- | --- | --- |
| DISCORD_WEBHOOK | The URL of your discord webhook | ``https://discord.com/api/webhooks/XXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYY`` |
| SUBS | Your subscribed attractions with ID from wartezeiten.app API | ``383533,323530,353030`` |

> Required enviromental variables: DISCORD_WEBHOOK, SUBS