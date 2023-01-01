import os
import time

# internal
import compute
import mcstatus

# external
import discord
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

channel = int(os.getenv("DISCORD_CHANNEL"))
mc_client = mcstatus.Client(os.getenv("MC_HOST"), int(os.getenv("MC_PORT")), 3)
mcdown = True

@tasks.loop(seconds=20)
async def checkmc():
    global mcdown
    c = client.get_channel(channel)
    try:
        response = mc_client.get_status()
    except:
        if mcdown is False:
            await c.send(":x: マインクラフトサーバーが停止しました")
        mcdown = True

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("mc start"):
        await message.channel.send("起動しています")
        try:
            compute.start_instance(os.getenv("GCP_PROJECT"), os.getenv("GCP_ZONE"), os.getenv("GCP_MC_INSTANCE"))
        except:
            await message.channel.send("起動に失敗しました")
            return
        for i in range(30):
            response = mc_client.get_status()
            print(response)
            await message.channel.send(":white_check_mark: マインクラフトサーバーが開始しました")
            mcdown = False
            time.sleep(10)
        await message.channel.send("起動に失敗しました")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    checkmc.start()

client.run(os.getenv("DISCORD_BOT_TOKEN"))
