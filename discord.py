import os
from dotenv import load_dotenv
import discord

load_dotenv()

discordToken = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(discordToken)

