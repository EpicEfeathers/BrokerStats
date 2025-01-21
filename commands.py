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
from utils.commands.leaderboards.daily import daily as daily_utils
from utils.commands.leaderboards.lifetime import lifetime as lifetime_utils
from utils.commands.broker_stats import get_stats as get_broker_stats


def stats(bot):
    """
    Stats command
    """
    @bot.tree.command(name="stats", description="Gets a user's stats")
    @app_commands.describe(uid='User\'s UID', username="In game nickname")
    async def stats(interaction: discord.Interaction, uid: Optional[str], username:Optional[str]):
        await stats_utils.stats_command(interaction, uid, username, False)

    @stats.autocomplete('username')
    async def stats_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return await stats_utils.username_autocomplete(current)
    

def linkstats(bot):
    """
    Linkstats command
    """
    @bot.tree.command(name="linkstats", description="Link your stats to your discord account.")
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
    

def squad(bot):
    """
    Squad command
    """
    @bot.tree.command(name="squad", description="Gets a squad's stats")
    @app_commands.describe(squad='Squad to search for')
    async def squad(interaction: discord.Interaction, squad:str):
        await squad_utils.squad_command(bot, squad, interaction)

    @squad.autocomplete('squad')
    async def squad_autocomplete(interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=squad, value=squad)
            for squad in bot.squad_list if current.lower() in squad.lower()
        ][:25]
    
def leaderboard(bot):
    """
    Leaderboard command
    """
    @bot.tree.command(name="leaderboard", description="Displays daily and lifetime leaderboards")
    @app_commands.describe(type='Daily or Lifetime', category='Daily leaderboard category')
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Daily", value="daily"),
            app_commands.Choice(name="Lifetime", value="lifetime")
        ]
    )
    async def leaderboard(interaction: discord.Interaction, type:str, category: str):
        daily_categories = {
            "Overall": lambda: daily_utils.daily_overall("Total Kills"),
            "Weapon Kills (Round)": lambda: daily_utils.daily_weapon_kills("AR Rifle"),
            "Vehicle Kills (Round)": lambda: daily_utils.daily_vehicle_kills("Tank LVL 1"),
            "Longest Kills":  lambda: daily_utils.daily_longest_kills("AR Rifle")
        }

        lifetime_categories = {
            "Overall":  lambda: lifetime_utils.lifetime_overall("XP"),
            "Weapon Kills":  lambda: lifetime_utils.lifetime_weapon_kills("AR Rifle"),
            "Vehicle Kills":  lambda: lifetime_utils.lifetime_vehicle_kills("Tank LVL 1"),
            "Weapon Damage":  lambda: lifetime_utils.lifetime_weapon_damage("AR Rifle"),
            "Longest Kills":  lambda: lifetime_utils.lifetime_longest_kills("AR Rifle"),
        }

        category_map = daily_categories if type == "daily" else lifetime_categories

        if category not in daily_categories and category not in lifetime_categories: # check if valid category (not a random string)
            await interaction.response.send_message(f"Oy! `{category}` isn't a valid category!") # if category not valid
            return
        
        if category_map[category] is None:
            await interaction.response.send_message(f"I'm sorry, but `{category}` is not complete yet!")
            return
        
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
        stat_card, view = await category_map[category]()
        await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
        view.response = await interaction.original_response()



    @leaderboard.autocomplete("category")
    async def category_autocomplete(
        interaction: discord.Interaction, current: str
    ):
        """
        Leaderboard category autocomplete
        """
        daily_categories = ["Overall", "Weapon Kills (Round)", "Vehicle Kills (Round)", "Longest Kills"]
        lifetime_categories = ["Overall", "Weapon Kills", "Vehicle Kills", "Weapon Damage", "Longest Kills"]

        selected_type = interaction.namespace.type # either daily or lifetime

        if selected_type == "daily":
            categories = daily_categories
        elif selected_type == "lifetime":
            categories = lifetime_categories

        # Filter categories based on what user has inputted so far
        return [
            app_commands.Choice(name=category, value=category)
            for category in categories if current.lower() in category.lower()
        ]

def help(bot):
    @bot.tree.command(name="help", description="Get help for Broker Stats")
    async def help(interaction: discord.Interaction):
        embed=discord.Embed(title="**Help**", color=0xfa3b06, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name="Broker Stats", icon_url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')
        
        stats = bot.tree.get_command("stats")
        embed.add_field(name="</stats:1295437878654144515>", value=f":chart_with_upwards_trend: {stats.description}\nLink your own stats using </linkstats:1296119982429831168>.", inline=False)
        
        linkstats = bot.tree.get_command("linkstats")
        embed.add_field(name="</linkstats:1296119982429831168>", value=f":link: {linkstats.description}\nUse this command to link your stats page to the bot.", inline=False)
        
        squad = bot.tree.get_command("squad")
        embed.add_field(name="</squad:1299897695854395453>", value=f":bar_chart: {squad.description}\nSee a detailed overview of a squad.", inline=False)

        leaderboard = bot.tree.get_command("leaderboard")
        embed.add_field(name="</leaderboard:1322777263506329784> UPDATE THIS", value=f":medal: {leaderboard.description}\nSee top daily or lifetime leaderboards.", inline=False)
        
        await interaction.response.send_message(embed=embed)


def broker_stats(bot):
    @bot.tree.command(name="broker_stats", description="Broker Stats overview")
    async def broker_stats(interaction: discord.Interaction):
        stats = await get_broker_stats.get_stats(bot)

        message = (
            "**Random Stats:**\n\n"
            f"**Total servers:** {stats['server_count']}\n"
            f"**Total messages:** {stats['total_messages']}\n"
            f"**Total messages this year:** {stats['total_yearly_messages']}\n"
            f"**Total users:** {stats['total_users']}\n"
            "**Created:** <t:1728326502:R>"
        )

        if interaction.user.id == 747797252105306212:
            guilds = stats['guilds']
            guild_stats = ''.join([f"\nID: {guild.id}, Name: {guild.name}, Member count: {guild.member_count}" for guild in guilds])
            message = message.replace("**Total messages:**", f"**Guild UID's:** {guild_stats}\n**Total messages:**")

            users = stats['users']
            message = message.replace(f"**Total users:** {stats['total_users']}\n", f"**Total users:** {stats['total_users']}{users}\n")
            
            await interaction.response.send_message(message, ephemeral=True)
        else:

            await interaction.response.send_message(message)