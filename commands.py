import discord
from discord import app_commands
from typing import Optional, List
import traceback
from urllib.parse import urlparse

import functions
from image_creation.database_stuff.functions import fetch_uid, link_user, reset_uid
from image_creation.get_stats import user
from image_creation.main_stats import main_stat_page

class Stats(discord.ui.View):
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


def stats(client):
    @client.tree.command(name="stats", description="Gets a user's stats")
    @app_commands.describe(uid='User\'s UID', username="In game nickname")
    async def stats(interaction: discord.Interaction, uid: Optional[str], username:Optional[str]):
        # check if they inputted the 1 character description option thing
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
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
            stats = await user.fetch_all(uid)

            await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
            stat_card = functions.convert_to_discord(main_stat_page.create_stat_card(stats=stats, profile_image=None))

            view = Stats(stats["nick"], uid)
            await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
            await view.wait()
        except Exception:
            print(traceback.format_exc())
            await interaction.edit_original_response(content=f"\"{uid}\" is not a valid WarBrokers uid!", ephemeral=True)

    @stats.autocomplete('username')
    async def stats_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return await user.username_autocomplete(current)
    
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
        return await user.username_autocomplete(current)