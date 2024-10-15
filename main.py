# Discord imports
import discord
from discord import app_commands
from discord.ext import commands
from io import BytesIO

import logging

from image_creation.main_stats.main_stat_page import create_stat_card
from image_creation.main_stats.functions import convert_to_discord
from image_creation.get_stats.user import fetch_all

#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

activity = discord.Activity(name = "my activity", type = discord.ActivityType.custom, state = "Shooting bots")

#bot = commands.Bot(command_prefix="",intents=intents,activity=activity)

MY_GUILD = discord.Object(id=1295425214020194304)

# MyClient class
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, activity: discord.Activity):
        super().__init__(intents=intents,activity=activity)

        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents,activity=activity)

# When bot boots
@client.event
async def on_ready():
    print(f"Successfully logged in as \033[1m{client.user}\033[0m")


# Test command
@client.tree.command()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"<a:loading1:1295503606077980712> bot is thinking...")
    #await interaction.response.send_message(f"{interaction.user.mention}, bot is up and running!", ephemeral=True)

@client.tree.command()
async def stats(interaction: discord.Interaction):
    '''await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("<a:loading1:1295503606077980712>  Grabbing information...", ephemeral=True)
    uid = "609aa68ed142afe952202c5c"
    stats = await fetch_all(uid)

    await interaction.followup.send("<a:loading1:1295503606077980712>  Creating stat card...", ephemeral=True)
    im = convert_to_discord(create_stat_card(stats))
    
    await interaction.followup.send(file=im)'''
    try:
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
        uid = "609aa68ed142afe952202c5c"
        stats = await fetch_all(uid)

        await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
        im = convert_to_discord(create_stat_card(stats))

        await interaction.edit_original_response(content="", attachments=[im])
    except Exception as e:
        print(e)


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