import discord
from discord import app_commands
from typing import Optional, List
import traceback
from urllib.parse import urlparse
import datetime

import functions
from utils.database_stuff.functions import fetch_uid, link_user, reset_uid

#from utils import menu_paginator
from utils.commands.squad import squad as squad_utils
from utils.commands.stats import stats as stats_utils

class squad_stats_view(discord.ui.View):
    def __init__(self, squad_name:str):
        super().__init__()

        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/squads/{squad_name}"))
        self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/squads/{squad_name}"))
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))


def stats(client):
    @client.tree.command(name="stats", description="Gets a user's stats")
    @app_commands.describe(uid='User\'s UID', username="In game nickname")
    async def stats(interaction: discord.Interaction, uid: Optional[str], username:Optional[str]):
        await stats_utils.stats_command(interaction, uid, username, False)

    @stats.autocomplete('username')
    async def stats_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return await stats_utils.username_autocomplete(current)
    

def linkstats(client):
    @client.tree.command(name="linkstats", description="Link your stats to your discord account.")
    @app_commands.describe(link='Your stat\'s page link', uid='Your UID', username="In game nickname")
    async def linkstats(interaction: discord.Interaction, link: Optional[str], uid: Optional[str], username: Optional[str]):
        if username == "too_short":
            await interaction.response.send_message(f"You need to enter at least 2 characters to search!", ephemeral=True)
            return
        
        user_id = interaction.user.id
        if username:
            uid = username

        if link:
            if link.startswith("https://stats.warbrokers.io/players/i/"):
                parsed_url = urlparse(link)
                uid = parsed_url.path.split('/')[-1]
            else:
                return await interaction.response.send_message(f"`{link}` is not a valid WarBrokers link!", ephemeral=True)
        
        # if user did not input link, uid, or username
        if not uid:
            return await interaction.response.send_message(f":exclamation: You must input either a stats page link, UID, or username to link your stats.", ephemeral=True)

        # try to link their stats
        try:
            link_user(user_id, uid)
            await interaction.response.send_message("Success! Your accounts have been linked! Use </stats:1295437878654144515> to try it out now!")
        except Exception as e:
            if link:
                await interaction.response.send_message(f"`{link}` does not contain a valid WarBrokers uid!", ephemeral=True)
            elif username:
                await interaction.response.send_message(f"`{username}` is not a valid WarBrokers player name.\nPlease wait for the options to show up and click on of those.", ephemeral=True)
            else:
                await interaction.response.send_message(f"`{uid}` is not a valid WarBrokers uid!", ephemeral=True)


    @linkstats.autocomplete('username')
    async def linkstats_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return await stats_utils.username_autocomplete(current)
    

def squad(client):
    @client.tree.command(name="squad", description="Gets a squad's stats")
    @app_commands.describe(squad='Squad to search for')
    async def squad(interaction: discord.Interaction, squad:str):
        await squad_utils.squad_command(client, squad, interaction)

    @squad.autocomplete('squad')
    async def squad_autocomplete(interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=squad, value=squad)
            for squad in client.squad_list if current.lower() in squad.lower()
        ][:25]


def help(client):
    @client.tree.command(name="help", description="Get help for Broker Stats")
    async def help(interaction: discord.Interaction):
        embed=discord.Embed(title="**Help**", color=0xfa3b06, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name="Broker Stats", icon_url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')
        
        stats = client.tree.get_command("stats")
        embed.add_field(name="</stats:1295437878654144515>", value=f":chart_with_upwards_trend: {stats.description}\nLink your own stats using </linkstats:1296119982429831168>.", inline=False)
        
        linkstats = client.tree.get_command("linkstats")
        embed.add_field(name="</linkstats:1296119982429831168>", value=f":link: {linkstats.description}\nUse this command to link your stats page to the bot.", inline=False)
        
        squad = client.tree.get_command("squad")
        embed.add_field(name="</squad:1299897695854395453>", value=f":bar_chart: {squad.description}\nSee a detailed overview of a squad.", inline=False)
        
        await interaction.response.send_message(embed=embed)