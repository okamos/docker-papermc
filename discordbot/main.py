import compute

import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("mc start"):
        try:
            start_instance(os.getenv("GCP_PROJECT"), os.getenv("GCP_ZONE"), os.getenv("GCP_MC_INSTANCE"))
        except:
            await message.channel.send("起動に失敗しました”)
            return
        await message.channel.send("起動しました")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
