import discord
from discord import app_commands
import traceback
from utils.database_stuff.functions import fetch_uid
from utils.commands.stats import get_user, user_image
import aiohttp

TIMEOUT = 180

class user_stats_view(discord.ui.View):
    """
    Buttons
    """
    def __init__(self, username:str, uid:str):
        super().__init__(timeout=TIMEOUT)
        self.username = username
        self.uid = uid
        self.response = None

        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/players/i/{uid}"))
        self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/players/{uid}"))
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))

    @discord.ui.button(label='Copy UID', style=discord.ButtonStyle.primary)
    async def copy_uid(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{self.username}\'s UID:```{self.uid}```', ephemeral=True)

    async def on_timeout(self) -> None:
        if self.response:
            self.copy_uid.disabled = True

            await self.response.edit(view=self)

async def stats_command(interaction, session, uid, username, ephemeral:bool):
    """
    Check if input is valid
    """
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
            stats = await get_user.fetch_all(session, uid)
        except:
            await interaction.response.send_message(content="Uhoh... something went wrong. Please try again!", ephemeral=True)

        
        await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
        stat_card = discord.File(fp=user_image.create_stats_card(stats=stats), filename="stat_card.png")

        view = user_stats_view(stats["nick"], uid)
        await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
        view.response = await interaction.original_response()
        #await view.wait()
    except Exception:
        print(traceback.format_exc())
        await interaction.edit_original_response(content=f"\"{uid}\" is not a valid WarBrokers uid!\n\n**Note:** sometimes uid's need to be loaded into the system. If you are 100% sure this is a real uid, please try again.")
        #await interaction.edit_original_response(content=f"\"{uid}\" is not a valid WarBrokers uid!")


async def get_autocomplete(query):
    """
    Get results for autocompletion when typing command
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://wbapi.wbpjs.com/players/searchByName?query={query}') as resp:
            if resp.status == 200:
                users = await resp.json()  # Assuming the API returns JSON

            else:
                users = []

    return users

async def username_autocomplete(current):
    """
    Adds username autocompletion to the command
    """
    if len(current) == 0:
        #users = [{'SAUNA MAKKARA': '5a4d14e9bfea71227e1fc4bf', 'TheyTookMyChat': '610dc399fd3c7a560e43287a', 'DEEBS': '5f2f9ee9bfea71685aa1e3f2', 'Walrus': '5fc9142ad142af9d623787a1', 'redrum': '5c382ee5d142af341a8053b2', 'Froggy': '6484dbc3d142af01608f2bdf', 'Grenade Bot': '61674a4efe3c7aff128efa73', 'geedolphin': '606c7b9dd142af4c188d9439', 'Nachtfalke': '5fe46c35fd3c7ac26198cf0c', 'Milan Kundera': '60a6a302d142af1f1d389c83', 'Y_Not!': '60006e69fd3c7ae8191e0cb4', 'Doki Doki': '5fb961e0d142af8b4885c87d', 'Tekker': '5f3d25e6fe3c7a43054828fa', 'Milan': '5aeba7b4fd3c7a805dbbd69d', 'Norw12': '647457c7bfea71f84a834ba2', 'Pandalorian': '5f5ac5bebfea715955d07e20', 'Alex140': '623f320bbfea718964e5b257', 'Nhat Huy': '6288fb09fe3c7a1319592978', 'BerzerkinG': '5d988fa4fe3c7a484cbe8cba', 'EncryptR_': '5e57527efe3c7acc73342809', 'ZZBeany': '5f2c63f1bfea71b305e60c98', 'Slayer': '61b18818fd3c7aa31f0e4aee', 'Nandy': '5d0fb3a0bfea71355fef4595', 'Guest1': '5db1f95fbfea71c96e8b4592', 'Guest97977': '5d45f84bfd3c7a8e36f1e671'}]
        usernames = [{'nick': 'SAUNA MAKKARA', 'uid': '5a4d14e9bfea71227e1fc4bf'}, {'nick': 'TheyTookMyChat', 'uid': '610dc399fd3c7a560e43287a'}, {'nick': 'DEEBS', 'uid': '5f2f9ee9bfea71685aa1e3f2'}, {'nick': 'Walrus', 'uid': '5fc9142ad142af9d623787a1'}, {'nick': 'redrum', 'uid': '5c382ee5d142af341a8053b2'}, {'nick': 'Froggy', 'uid': '6484dbc3d142af01608f2bdf'}, {'nick': 'Grenade Bot', 'uid': '61674a4efe3c7aff128efa73'}, {'nick': 'geedolphin', 'uid': '606c7b9dd142af4c188d9439'}, {'nick': 'Nachtfalke', 'uid': '5fe46c35fd3c7ac26198cf0c'}, {'nick': 'Milan Kundera', 'uid': '60a6a302d142af1f1d389c83'}, {'nick': 'Y_Not!', 'uid': '60006e69fd3c7ae8191e0cb4'}, {'nick': 'Doki Doki', 'uid': '5fb961e0d142af8b4885c87d'}, {'nick': 'Tekker', 'uid': '5f3d25e6fe3c7a43054828fa'}, {'nick': 'Milan', 'uid': '5aeba7b4fd3c7a805dbbd69d'}, {'nick': 'Norw12', 'uid': '647457c7bfea71f84a834ba2'}, {'nick': 'Pandalorian', 'uid': '5f5ac5bebfea715955d07e20'}, {'nick': 'Alex140', 'uid': '623f320bbfea718964e5b257'}, {'nick': 'Nhat Huy', 'uid': '6288fb09fe3c7a1319592978'}, {'nick': 'BerzerkinG', 'uid': '5d988fa4fe3c7a484cbe8cba'}, {'nick': 'EncryptR_', 'uid': '5e57527efe3c7acc73342809'}, {'nick': 'ZZBeany', 'uid': '5f2c63f1bfea71b305e60c98'}, {'nick': 'Slayer', 'uid': '61b18818fd3c7aa31f0e4aee'}, {'nick': 'Nandy', 'uid': '5d0fb3a0bfea71355fef4595'}, {'nick': 'Guest1', 'uid': '5db1f95fbfea71c96e8b4592'}, {'nick': 'Guest97977', 'uid': '5d45f84bfd3c7a8e36f1e671'}]
        '''return [
            app_commands.Choice(name=user['nick'], value=user['uid']) 
            for user in users
        ]''' 
    elif len(current) < 2:
        return [
                app_commands.Choice(name="Enter more than 1 character to search!", value="too_short")
            ]
    
    else:
        usernames = await get_autocomplete(current)

    return [
        app_commands.Choice(name=f"{username['nick']} (UID: {username['uid']})", value=username['uid']) 
        for username in usernames
    ]