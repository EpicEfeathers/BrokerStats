import discord
import math
from utils.commands.squad_last_seen import get_data

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stats import stats

PAGE_SIZE = 24

class Dropdown(discord.ui.Select):
    def __init__(self, user_id:int, paginator_view):
        self.user_id = user_id
        self.paginator_view = paginator_view

        options = [ # sets correct item to selected, adds rest to dropdown
            discord.SelectOption(label="Sort by Username (A-Z)", value="sort_asc", default=True),
            discord.SelectOption(label="Sort by Username (Z-A)", value="sort_desc"),
            discord.SelectOption(label="Sort by Time Last Seen (Recent first)", value="sort_recent"),
            discord.SelectOption(label="Sort by Time Last Seen (Oldest first)", value="sort_oldest"),
        ]

        super().__init__(min_values=1, max_values=1, options=options, row=1) # select min and max 1 value (only select one thing), custom options, row is 1

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Hey! This is not your command!", ephemeral=True)
            return
        
        for option in self.options: # sets which one is selected
            option.default = (option.value == self.values[0])

        
        data = get_data.sort_data(self.values[0], self.paginator_view.data) # get sorted data

        self.paginator_view.data = data # update paginator view's data to be sorted correctly
        self.paginator_view.page_num = 0 # reset page num so shows from beginning

        # Refresh button states
        self.paginator_view.left.disabled = True
        self.paginator_view.right.disabled = (len(data) <= PAGE_SIZE)

        # create code block
        code_block = get_data.create_code_block(data, start_index=self.paginator_view.page_num * PAGE_SIZE, end_index=self.paginator_view.page_num * PAGE_SIZE + PAGE_SIZE)

        await interaction.response.edit_message(content=code_block, view=self.paginator_view)

class Paginator(discord.ui.View):
    def __init__(self, user_id, data, timeout):
        super().__init__(timeout=timeout)
        self.page_num = 0
        self.user_id = user_id
        self.timeout = timeout

        self.data = data

        self.is_active = True

        self.add_item(Dropdown(self.user_id, self))

        self.right.disabled = (len(data) <= PAGE_SIZE)

    async def on_timeout(self) -> None:
        if self.is_active:
            for item in self.children:
                item.disabled = True

    async def ensure_user(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Hey! This is not your command!", ephemeral=True)
            return True
        return False

    # left button
    @discord.ui.button(emoji="<:left_arrow:1301174573051416618>", style=discord.ButtonStyle.blurple, row=2, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        if self.page_num > 0:
            self.page_num -=1

        await self.update(interaction)

    # right button
    @discord.ui.button(emoji="<:right_arrow:1301174594581037088>", style=discord.ButtonStyle.blurple, row=2)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if await self.ensure_user(interaction): # checks if proper user is interacting
            return
        
        if self.page_num < math.ceil(len(self.data)/PAGE_SIZE) - 1:
            self.page_num +=1

        await self.update(interaction)

    # on update
    async def update(self, interaction):

        self.left.disabled = (self.page_num == 0)
        self.right.disabled = (self.page_num == math.ceil((len(self.data)/PAGE_SIZE)) - 1)


        code_block = get_data.create_code_block(self.data, start_index=self.page_num * PAGE_SIZE, end_index=self.page_num * PAGE_SIZE + PAGE_SIZE)
        print(self.page_num)
        await interaction.response.edit_message(content=code_block, view=self)
