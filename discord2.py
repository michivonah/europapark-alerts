import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook

load_dotenv()

webhookUrl = os.getenv('DISCORD_WEBHOOK')

webhook = DiscordWebhook(url=webhookUrl, content="Test")
response = webhook.execute()