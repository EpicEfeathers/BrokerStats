import discord
import math

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stats import stats

PAGE_SIZE = 25

class SquadDropdown(discord.ui.Select):
    def __init__(self, user_id, users:list, num):
        self.user_id = user_id
        user_items = list(users.items())
        options = [discord.SelectOption(label=username, value=uid) for username, uid in user_items[(num-1)*PAGE_SIZE:num*PAGE_SIZE]]

        super().__init__(placeholder=f'See the stats of a squad member (pg. {num}/{math.ceil(len(users)/PAGE_SIZE)})', min_values=1, max_values=1, options=options, row=1)

    async def callback(self, interaction: discord.Interaction):     
        if interaction.user.id != self.user_id: # checks if proper user is interacting
            await interaction.response.send_message("Hey! This is not your command!", ephemeral=True)
            return
           
        await stats.stats_command(interaction, uid=self.values[0], username=None, ephemeral=True)

class BaseView(discord.ui.View):
    def __init__(self, user_id, squad, timeout=None):
        super().__init__(timeout=timeout)

        self.user_id = user_id
        
        # Common button shared across all views
        self.add_item(discord.ui.Button(label='Stats page', url=f"https://stats.warbrokers.io/squads/{squad}"))
        self.add_item(discord.ui.Button(label='POMPS\'s stats', url=f"https://stats.wbpjs.com/squads/{squad}"))
        self.add_item(discord.ui.Button(label='Support server', url="https://discord.gg/8r52JxkJez"))

    async def ensure_user(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Hey! This is not your command!", ephemeral=True)
            return True
        return False
        
class first_view(BaseView):
    def __init__(self, user_id, users, squad, timeout):
        super().__init__(user_id=user_id, squad=squad, timeout=timeout)
        self.user_id = user_id
        self.users = users
        self.squad = squad
        self.timeout = timeout

        self.response = None
        self.is_active = True

    async def on_timeout(self) -> None:
        if self.is_active:
            #if not item.disabled:
            for item in self.children:
                if item.url is None:
                    item.disabled = True

            if self.response:
                await self.response.edit(view=self)

    @discord.ui.button(label='Show users', style=discord.ButtonStyle.green)
    async def show_users(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        self.is_active = False
        view = second_view(self.user_id, self.users, self.squad, timeout=self.timeout)
        await interaction.response.edit_message(view=view)
        view.response = await interaction.original_response()

class second_view(BaseView):
    def __init__(self, user_id, users:list, squad, timeout):
        super().__init__(user_id=user_id, squad=squad, timeout=timeout)
        self.num = 1
        self.user_id = user_id
        self.users = users
        self.squad = squad
        self.timeout = timeout

        self.response = None
        self.is_active = True

        # Adds the dropdown to our view object.
        self.dropdown = SquadDropdown(self.user_id, users, self.num)
        self.add_item(self.dropdown)

        self.right.disabled = len(users) <= 25

        self.response = None

    async def on_timeout(self) -> None:
        if self.is_active:
            for item in self.children:
                #if not item.disabled:
                if isinstance(item, discord.ui.Button) and item.url is None:
                    item.disabled = True
                elif not isinstance(item, discord.ui.Button):
                    item.disabled = True

            if self.response:
                self.dropdown.placeholder = 'This command has timed out!'
                await self.response.edit(view=self)

    # hide users
    @discord.ui.button(label='Hide users', style=discord.ButtonStyle.red)
    async def hide_users(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        self.is_active = False
        view = first_view(self.user_id, self.users, self.squad, self.timeout)
        await interaction.response.edit_message(view=view)
        view.response = await interaction.original_response()

    # left button
    @discord.ui.button(emoji="<:left_arrow:1301174573051416618>", style=discord.ButtonStyle.blurple, row=2, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        if self.num > 1:
            self.num -=1

        await self.update(interaction)

    # right button
    @discord.ui.button(emoji="<:right_arrow:1301174594581037088>", style=discord.ButtonStyle.blurple, row=2)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        if self.num < math.ceil(len(self.users)/25):
            self.num +=1

        await self.update(interaction)

    async def update(self, interaction):
        user_items = list(self.users.items())
        self.dropdown.options = [discord.SelectOption(label=username, value=uid) for username, uid in user_items[(self.num-1)*PAGE_SIZE : self.num*PAGE_SIZE]]
        self.dropdown.placeholder = f'See the stats of a squad member (pg. {self.num}/{math.ceil(len(self.users)/PAGE_SIZE)})'

        self.left.disabled = self.num == 1
        self.right.disabled = self.num == math.ceil((len(self.users)/25))

        await interaction.response.edit_message(view=self)