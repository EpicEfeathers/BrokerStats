# Discord imports
import discord
from discord import app_commands
from discord.ext import commands

import logging

from user_commands import user



#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

activity = discord.Activity(name = "my activity", type = discord.ActivityType.custom, state = "Shooting bots")

#bot = commands.Bot(command_prefix="",intents=intents,activity=activity)

MY_GUILD = discord.Object(id=915714438273826858)

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
    await interaction.response.send_message(f"{interaction.user.mention}, bot is up and running!", ephemeral=True)

user.user(client)

# error handling
'''@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandInvokeError):
        print(f"\033[91m{error}\033[0m")
        await interaction.response.send_message(":exclamation: An error occured while processing the request. If this error continues, please report it through the support server.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)'''

# CHANGE SECRET ON RELEASE
