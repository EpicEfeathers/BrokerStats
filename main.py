# Discord imports
import discord
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional
import requests
import math


import commands
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

intents = discord.Intents.default()
client = MyClient(intents=intents,activity=activity)

# When bot boots
@client.event
async def on_ready():
    try:
        client.get_squads.start()
    except: # if running already
        pass
    print(f"Successfully logged in as \033[1m{client.user}\033[0m")

class BaseView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
        
        # Common button shared across all views
        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/squads"))
        self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/squads"))
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))
        
class first_view(BaseView):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Show users', style=discord.ButtonStyle.green)
    async def new_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        users = {'Ph1LzA': '649228fcbfea718124fe50c7', 'Technoblade': '61314465bfea711a3f11ef16', 'Imagine Dying': '65b99682d142af8101fc7025', 'im_high_asffrn': '65594e76fe3c7ab303fbd6d5', 'EpicEfeathers': '609aa68ed142afe952202c5c', 'Froggy': '6484dbc3d142af01608f2bdf', 'KKillzStorm': '5c7f004dd142afa86e682d2a', 'sick-o': '61bd49e9bfea714a1efe82fc', 'DaintyAlmond': '5c89d3fdbfea71667133ecb8'}
        await interaction.response.edit_message(view=second_view(users, 180))

class SquadDropdown(discord.ui.Select):
    def __init__(self, users:list, num):
        user_items = list(users.items())
        options = [discord.SelectOption(label=username, value=uid) for username, uid in user_items[(num-1)*25:num*25]]

        super().__init__(placeholder=f'See the stats of a squad member (pg. {num}/{math.ceil(len(users)/25)})', min_values=1, max_values=1, options=options, row=1)

    async def callback(self, interaction: discord.Interaction):
        #await stats.stats_command(interaction, uid=self.values[0], username=None)
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')

class second_view(BaseView):
    def __init__(self, users:list, timeout):
        super().__init__(timeout=timeout)
        self.num = 1
        self.users = users
        
        # Adds the dropdown to our view object.
        self.dropdown = SquadDropdown(users, self.num)
        self.add_item(self.dropdown)

        self.right.disabled = len(users) <= 25

        self.response = None

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.url is None:
                item.disabled = True
            elif not isinstance(item, discord.ui.Button):
                item.disabled = True
                

        if self.response:
            self.dropdown.placeholder = 'This command has timed out!'
            await self.response.edit(view=self)

    @discord.ui.button(label='Hide users', style=discord.ButtonStyle.red)
    async def new_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=first_view(self.users))

    @discord.ui.button(emoji="<:left_arrow:1301174573051416618>", style=discord.ButtonStyle.blurple, row=2, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num > 1:
            self.num -=1

        await self.update(interaction)


    @discord.ui.button(emoji="<:right_arrow:1301174594581037088>", style=discord.ButtonStyle.blurple, row=2)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num < math.ceil(len(self.users)/25):
            self.num +=1

        await self.update(interaction)

    async def update(self, interaction):
        self.dropdown.options = [discord.SelectOption(label=user) for user in self.users[(self.num - 1) * 25:(self.num * 25)]]
        self.dropdown.placeholder = f'See the stats of a squad member (pg. {self.num}/{math.ceil(len(self.users)/25)})'

        self.left.disabled = self.num == 1
        self.right.disabled = self.num == math.ceil((len(self.users)/25))

        await interaction.response.edit_message(view=self)

    

# Test command
@client.tree.command()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Example", view=first_view())
    #await interaction.response.send_message(f"{interaction.user.mention}, bot is up and running!", view=Counter(), ephemeral=True)'''

commands.stats(client)
commands.linkstats(client)
commands.squad(client)

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