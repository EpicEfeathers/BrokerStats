# Discord imports
import discord
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional
import requests
import math


import commands
from utils.monitor_pi import monitor_stats
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

activity = discord.Activity(name = "my activity", type = discord.ActivityType.custom, state = "Shooting bots")

#bot = commands.Bot(command_prefix="",intents=intents,activity=activity)

MY_GUILD = discord.Object(id=1295425214020194304)
SQUAD_LIST_URL = "https://wbapi.wbpjs.com/squad/getSquadList"
squad_list = requests.get(SQUAD_LIST_URL).json()

# MyClient class
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, activity: discord.Activity):
        super().__init__(intents=intents,activity=activity)
        self.tree = app_commands.CommandTree(self)
        #self.squad_list

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    @tasks.loop(hours=5.0)
    async def get_squads(self):
        print("Squad list updated.")
        self.squad_list = requests.get("https://wbapi.wbpjs.com/squad/getSquadList").json()

    @tasks.loop(minutes=30)
    async def update_pi_stats(self):
        message_id = 1304199817278259274  # Replace with the message ID you want to edit
        channel_id = 1304092651083141120  # Replace with the channel ID of the message

        # Get the channel and the message
        channel = client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        file, embed = monitor_stats()
        await message.edit(embed=embed)

        print("Updated Pi Stats")

intents = discord.Intents.default()
client = MyClient(intents=intents,activity=activity)

# When bot boots
@client.event
async def on_ready():
    try:
        client.get_squads.start()
        client.update_pi_stats.start()
    except: # if running already
        pass
    print(f"Successfully logged in as \033[1m{client.user}\033[0m")    

# Test command
@client.tree.command()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention}, bot is up and running!", ephemeral=True)

commands.stats(client)
commands.linkstats(client)
commands.squad(client)
commands.help(client)

# error handling
'''@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandInvokeError):
        print(f"\033[91m{error}\033[0m")
        await interaction.response.send_message(":exclamation: An error occured while processing the request. If this error continues, please report it through the support server.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)'''

# CHANGE SECRET ON RELEASE
# HEY YOUUUUUUUU - CHANGELOG IN DISCORD + VERSION NUMBER :P
client.run('client secret')#, log_handler = handler)