#Example:
#input_list = [discord.Embed(description="hi"), "2", "3", "4"]
#await interaction.response.send_message(input_list[0], view=paginator.Counter(input_list))


import discord

class Counter(discord.ui.View):
    def __init__(self, input_list:dict):
        super().__init__()
        self.input_list = input_list
        self.num = 0

    @discord.ui.button(label='<-', style=discord.ButtonStyle.red, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num > 0:
            self.num -=1
        
        await self.update(interaction)

    @discord.ui.button(label='->', style=discord.ButtonStyle.red)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.num < len(self.input_list) - 1:
            self.num +=1
        
        await self.update(interaction)

    async def update(self, interaction):
        self.left.disabled = self.num == 0
        self.right.disabled = self.num == len(self.input_list) - 1

        content = self.input_list[self.num]
        if isinstance(content, discord.Embed):
            await interaction.response.edit_message(embed=content, content=None, view=self)
        else:
            await interaction.response.edit_message(embed=None, content=content, view=self)