import discord
from discord import app_commands
import traceback
import functions
from image_creation.database_stuff.functions import fetch_uid
from utils.commands.stats import get_user, user_image
import aiohttp
import requests
import time


class user_stats_view(discord.ui.View):
    def __init__(self, username:str, uid:str):
        super().__init__()
        self.username = username
        self.uid = uid

        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/players/i/{uid}"))
        self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/players/{uid}"))
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))

    @discord.ui.button(label='Copy UID', style=discord.ButtonStyle.primary)
    async def copy_uid(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{self.username}\'s UID:```{self.uid}```', ephemeral=True)

# check if they inputted the 1 character description option thing
async def stats_command(interaction, uid, username, ephemeral:bool):
    start = time.time()
    if username == "too_short":
        await interaction.response.send_message(f"You need to enter at least 2 characters to search!", ephemeral=True)
        return

    if username:
        uid = username
    if uid:
        if len(uid) != 24 or not uid.isalnum():
            return await interaction.response.send_message(f"\"{uid}\" is not a valid WarBrokers uid!", ephemeral=True)
    else:
        try:
            uid = fetch_uid(interaction.user.id)
        except:
            return await interaction.response.send_message(content="You have not linked your stats yet. Use </linkstats:1296119982429831168> to do so!")
        
    try:
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...", ephemeral=ephemeral)
        try:
            stats = await get_user.fetch_all(uid)
        except:
            await interaction.response.send_message(content="Uhoh... something went wrong. Please try again!", ephemeral=True)

        print(time.time() - start)
        
        await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
        start = time.time()
        stat_card = discord.File(fp=user_image.create_stats_card(stats=stats), filename="stat_card.png")
        #stat_card = user_image.create_stats_card(stats=stats)
        print(time.time() - start)

        view = user_stats_view(stats["nick"], uid)
        await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
        await view.wait()
    except Exception:
        print(traceback.format_exc())
        await interaction.edit_original_response(content=f"\"{uid}\" is not a valid WarBrokers uid!")

def get_autocompletion(query):
    response = requests.get(f"https://wbapi.wbpjs.com/players/searchByName?query={query}").json()

    nicks = []
    for entry in response:
        nicks.append(entry["nick"])

    if "PleaseChangeNick" in nicks:
        nicks.remove("PleaseChangeNick")

    def thing(x):
        return (not x.lower().startswith("hit"), x)
    
    nicks = sorted(nicks, key=thing)

    return nicks

async def get_autocomplete(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://wbapi.wbpjs.com/players/searchByName?query={query}') as resp:
            if resp.status == 200:
                data = await resp.json()  # Assuming the API returns JSON
        
                # turns list of dictionaries into 1 dict
                users = {}
                for datum in data:
                    users[datum["nick"]] = datum["uid"]

                #removes banned / changes nicknames from the list
                users.pop("PleaseChangeNick", None)
                # sorts with anything starting with the query first
                def thing(x):
                    return (not x[0].lower().startswith(query), x[0])
                sorted_ = sorted(users.items(), key=thing)

                users = {}
                for user in sorted_:
                    users[user[0]] = user[1]

            else:
                users = []

    return users

async def username_autocomplete(current):
    if len(current) == 0:
        users = {'SAUNA MAKKARA': '5a4d14e9bfea71227e1fc4bf', 'TheyTookMyChat': '610dc399fd3c7a560e43287a', 'DEEBS': '5f2f9ee9bfea71685aa1e3f2', 'Walrus': '5fc9142ad142af9d623787a1', 'redrum': '5c382ee5d142af341a8053b2', 'Froggy': '6484dbc3d142af01608f2bdf', 'Grenade Bot': '61674a4efe3c7aff128efa73', 'geedolphin': '606c7b9dd142af4c188d9439', 'Nachtfalke': '5fe46c35fd3c7ac26198cf0c', 'Milan Kundera': '60a6a302d142af1f1d389c83', 'Y_Not!': '60006e69fd3c7ae8191e0cb4', 'Doki Doki': '5fb961e0d142af8b4885c87d', 'Tekker': '5f3d25e6fe3c7a43054828fa', 'Milan': '5aeba7b4fd3c7a805dbbd69d', 'Norw12': '647457c7bfea71f84a834ba2', 'Pandalorian': '5f5ac5bebfea715955d07e20', 'Alex140': '623f320bbfea718964e5b257', 'Nhat Huy': '6288fb09fe3c7a1319592978', 'BerzerkinG': '5d988fa4fe3c7a484cbe8cba', 'EncryptR_': '5e57527efe3c7acc73342809', 'ZZBeany': '5f2c63f1bfea71b305e60c98', 'Slayer': '61b18818fd3c7aa31f0e4aee', 'Nandy': '5d0fb3a0bfea71355fef4595', 'Guest1': '5db1f95fbfea71c96e8b4592', 'Guest97977': '5d45f84bfd3c7a8e36f1e671'}
        return [
            app_commands.Choice(name=user, value=users[user]) 
            for user in users
        ] 
    elif len(current) < 2:
        return [
                app_commands.Choice(name="Enter more than 1 character to search!", value="too_short")
            ]
    
    usernames = await get_autocomplete(current)
    return [
        app_commands.Choice(name=username, value=usernames[username]) 
        for username in usernames
    ]