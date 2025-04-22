import discord
import math

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stats import stats

PAGE_SIZE = 25

class BaseView(discord.ui.View):
    def __init__(self, user_id, squad, timeout=None):
        super().__init__(timeout=timeout)

        self.user_id = user_id

    async def ensure_user(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Hey! This is not your command!", ephemeral=True)
            return True
        return False

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

        self.left.disabled = self.num == 1
        self.right.disabled = self.num == math.ceil((len(self.users)/25))

        await interaction.response.edit_message(view=self)