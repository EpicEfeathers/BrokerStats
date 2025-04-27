import discord
from discord import app_commands
from typing import Optional, List
import traceback
from urllib.parse import urlparse
import datetime

from utils.database_stuff.functions import fetch_uid, link_user, reset_uid

#from utils import menu_paginator
from utils.commands.squad import squad as squad_utils
from utils.commands.stats import stats as stats_utils
from utils.commands.leaderboards.daily import daily as daily_utils
from utils.commands.leaderboards.lifetime import lifetime as lifetime_utils
from utils.commands.broker_stats import get_stats as get_broker_stats
from utils.commands.player_count.current_player_count import plot_player_count, current_data
from utils.commands.player_count.historical_playercount import plot_historical_player_count, fetch_historical_data
from utils.commands.maps import get_data, process_data
from utils.commands.warbrokers import fetch_data as warbrokers_data, create_image as create_warbrokers_image

from utils.commands.trends import daily_playercount_data, total_playercount_data, trends as trends_data
from utils.commands.squad_last_seen import squad_last_seen

from utils.commands.help import help as help_command



REGIONS = ['Worldwide', 'Asia', 'Australia', 'Europe', 'India', 'Japan', 'Russia', 'NA']
SERVERS = ['Asia', 'Asia 4V4', 'Asia Clan', 'Australia Battle Royale', 'Australia Dead City', 'Australia', 'Australia Clan', 'Europe', 'Europe Clan', 'Europe 4V4', 'Europe Battle Royale', 'Europe Dead City', 'India', 'India Clan', 'Japan', 'Japan Clan', 'NA Battle Royale', 'NA Dead City', 'Russia', 'USA', 'USA 4V4', 'USA Clan', 'USA West', 'USA West Clan']


def stats(bot):
    """
    Stats command
    """
    @bot.tree.command(name="stats", description="Gets a user's stats")
    @app_commands.describe(uid='User\'s UID', username="In game nickname")
    async def stats(interaction: discord.Interaction, uid: Optional[str], username:Optional[str]):
        await stats_utils.stats_command(interaction, bot.session, uid, username, False)

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
            "Overall": lambda: daily_utils.daily_overall(bot.session, interaction.user.id, "Total Kills"),
            "Weapon Kills (Round)": lambda: daily_utils.daily_weapon_kills(bot.session, interaction.user.id, "AR Rifle"),
            "Vehicle Kills (Round)": lambda: daily_utils.daily_vehicle_kills(bot.session, interaction.user.id, "Tank LVL 1"),
            "Longest Kills":  lambda: daily_utils.daily_longest_kills(bot.session, interaction.user.id, "AR Rifle")
        }

        lifetime_categories = {
            "Overall":  lambda: lifetime_utils.lifetime_overall(bot.session, interaction.user.id, "XP"),
            "Weapon Kills":  lambda: lifetime_utils.lifetime_weapon_kills(bot.session, interaction.user.id, "AR Rifle"),
            "Vehicle Kills":  lambda: lifetime_utils.lifetime_vehicle_kills(bot.session, interaction.user.id, "Tank LVL 1"),
            "Weapon Damage":  lambda: lifetime_utils.lifetime_weapon_damage(bot.session, interaction.user.id, "AR Rifle"),
            "Longest Kills":  lambda: lifetime_utils.lifetime_longest_kills(bot.session, interaction.user.id, "AR Rifle"),
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
        embed = help_command.help(bot)
        
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
            "**Created:** <t:1728326502:R>\n"
            f"**Ping:** {round(bot.latency*1000)} ms" # 1000 ms in 1 s
        )

        if interaction.user.id == 747797252105306212:
            guilds = stats['guilds']
            guild_stats = ''.join([f"\nID: {guild.id}, Name: {guild.name}, Member count: {guild.member_count}" for guild in guilds])
            message = message.replace("**Total messages:**", f"**Guild UID's:** {guild_stats}\n**Total messages:**")

            users = stats['users']
            message = message.replace(f"**Total users:** {stats['total_users']}\n", f"**Total users:** {stats['total_users']}\n{users}\n")
            
            await interaction.response.send_message(message, ephemeral=True)
        else:

            await interaction.response.send_message(message)



def player_count(bot):
    @bot.tree.command(name="player_count", description="Gets current player count")
    @app_commands.describe(type='region or server', category='...')
    @app_commands.choices(
        time=[
            app_commands.Choice(name="Current", value="current"),
            app_commands.Choice(name="Historical", value="historical")
        ],
        type=[
            app_commands.Choice(name="Region", value="region"),
            app_commands.Choice(name="Server", value="server")
        ]
    )
    async def player_count(interaction: discord.Interaction, time: str, type: str, category: str):
        if time == "current":
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
            player_counts = current_data.get_data()

            await interaction.edit_original_response(content="<a:loading1:1295503606077980712> Creating image...")
            image = plot_player_count.return_image(player_counts)

            await interaction.edit_original_response(content="", attachments=[discord.File(image, filename="player_count.png")])

        else:    
            if (type == "region" and category not in REGIONS) or (type == "server" and category not in SERVERS):
                await interaction.response.send_message(content=f"`{category}` is not a valid category. Make sure to choose one of the options from the menu.", ephemeral=True)
                return
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
            player_count, timestamps, title = fetch_historical_data.get_data(category, type)

            await interaction.edit_original_response(content="<a:loading1:1295503606077980712> Creating image...")
            image = plot_historical_player_count.return_image(category, player_count, timestamps, title)

            await interaction.edit_original_response(content="", attachments=[discord.File(image, filename="player_count.png")])

    @player_count.autocomplete("category")
    async def category_autocomplete(
        interaction: discord.Interaction, current: str
    ):
        """
        Leaderboard category autocomplete
        """

        selected_time = interaction.namespace.time
        selected_type = interaction.namespace.type # either region or server

        if selected_time == "current":
            return []

        if selected_type == "region":
            categories = REGIONS
        elif selected_type == "server":
            categories = SERVERS

        # Filter categories based on what user has inputted so far
        return [
            app_commands.Choice(name=category, value=category)
            for category in categories if current.lower() in category.lower()
        ]





def mapper(bot):
    @bot.tree.command(name="mapper", description="Maps by region")
    async def mapper(interaction: discord.Interaction):
        server_data = await get_data.fetch_all()

        processed_data = process_data.process_server_data(server_data)
        
        await interaction.response.send_message(processed_data)


def warbrokers(bot):
    @bot.tree.command(name="warbrokers", description="Game overview")
    async def warbrokers(interaction: discord.Interaction):
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
        total_playercount, playercount = await warbrokers_data.fetch_data(bot.session)

        await interaction.edit_original_response(content="<a:loading1:1295503606077980712> Creating image...")
        stats_card = create_warbrokers_image.create_stats_card(total_playercount, playercount)

        await interaction.edit_original_response(content="", attachments=[discord.File(stats_card, filename="warbrokers.png")])



def weapon_stats(bot):
    @bot.tree.command(name="weapon_stats", description="Show your stats for each weapon")
    async def weapon_stats(interaction: discord.Interaction):
        thing = '''```ansi
                   Kills     Longest     Accuracy     Damage Dealt
    
.50                   93                                     20340
AK                  2177                                    123548
AK SMG               109                                      5254
AR                  3252                                    172333
Air Strike           165                                     28865
Auto Pistol           34                                      4784
Auto Sniper          484                                     67702
BGM                  244                                    189881
Butterfly              0                                         0
Chainsaw               1                                       600
Concussion             6                                      4951
Crossbow             191                                     34500
Desert                 2                                      1077
Fists                  1                                       120
G3A3                  98                                      5943
GL                     0                                       330
Grenade              355                                    192164
Healing Pistol         0                                         0
Homing                25                                     28792
Hunting               23                                      3001
Implosion              0                                      2400
KBAR                   1                                       375
Knife                111                                     35375
LMG                   16                                      1273
Laser Trip Mine        1                                       959
MG Turret             19                                       239
Mace                   0                                         0
Minigun                2                                       406
Pistol               101                                      7945
RPG                  144                                     75395
Revolver             516                                     80886
Rubber Chicken       543                                    153000
SCAR                  54                                      3156
SMG                 5414                                    254251
Shotgun              300                                     10822
Smoke Grenade          0                                         0
Sniper              6220                                   1166467
Tac Shotty             3                                       280
VEK                    1                                        37
VSS                    8                                       173```
'''
        embed=discord.Embed(title="Embed title (required)", description=thing)
        #await interaction.response.send_message(thing)

        await interaction.response.send_message(embed=embed)



def trends(bot):
    @bot.tree.command(name="trends", description="Shows game trends")
    #@app_commands.describe(type='Option 1 or Option 2')
    #@app_commands.choices(
    #    type=[
    #        app_commands.Choice(name="Daily", value="daily"),
    #    ]
    #)
    async def trends(interaction: discord.Interaction):#, type:str):
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
        daily_average = daily_playercount_data.get_avgs()
        daily_average_diff = daily_average[0] - daily_average[1]

        total_playercount = await total_playercount_data.return_data(bot.session)
        total_playercount_diff = total_playercount[0] - total_playercount[1]

        await interaction.edit_original_response(content="<a:loading1:1295503606077980712> Creating image...")

        stats_card = trends_data.create_image(daily_average, daily_average_diff, total_playercount, total_playercount_diff)

        await interaction.edit_original_response(content="", attachments=[discord.File(stats_card, filename="trends.png")])


def last_seen(bot):
    @bot.tree.command(name="last_seen", description="Squad last seen")
    @app_commands.describe(squad='Squad to search for')
    async def last_seen(interaction: discord.Interaction, squad: str):
        await squad_last_seen.squad_last_seen(bot, interaction, squad, page_num=1)

    @last_seen.autocomplete('squad')
    async def last_seen_autocomplete(interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=squad, value=squad)
            for squad in bot.squad_list if current.lower() in squad.lower()
        ][:25]