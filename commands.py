import discord
from discord import app_commands
from typing import Optional, List
import traceback

import functions
from image_creation.database_stuff.functions import fetch_uid
from image_creation.get_stats import user
from image_creation.main_stats import main_stat_page


def stats(client):
    @client.tree.command(name="stats", description="Gets a user's stats")
    @app_commands.describe(uid='User\'s UID', username="In game nickname")
    async def stats(interaction: discord.Interaction, uid: Optional[str], username:Optional[str]):
        if username:
            uid = username
        if uid:
            if len(uid) != 24 or not uid.isalnum():
                await interaction.response.send_message(f"You must enter a valid uid.\n{uid} is not a valid WarBrokers uid.")
                return
        else:
            try:
                uid = fetch_uid(interaction.user.id)
            except Exception as e:
                await interaction.response.send_message(content="You have not linked your stats yet. Use </linkstats:1296119982429831168> to do so!")
                return
        try:
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")
            stats = await user.fetch_all(uid)

            await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
            im = functions.convert_to_discord(main_stat_page.create_stat_card(stats=stats, profile_image=None))

            await interaction.edit_original_response(content="", attachments=[im])
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await interaction.edit_original_response(content=f"\"{uid}\" is not a valid WarBrokers uid!")

    @stats.autocomplete('username')
    async def stats_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        return await user.username_autocomplete(current)