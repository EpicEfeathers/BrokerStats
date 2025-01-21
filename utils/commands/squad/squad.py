from utils.commands.squad.get_squad_stats import fetch_squad, fetch_squad_users, parse_data
from utils.commands.squad import squad_image, menu_paginator
import traceback

import sys
import os
import discord
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

async def squad_command(client, squad, interaction):
    if squad in client.squad_list:
        if squad == "CAESAR":
            await interaction.response.send_message("I'm sorry, but CAESAR does not currently work right now! With over 100 members, the way POMP's API is currently configured means too many requests. This should be resolved as soon as POMP has the free time to do it! Thanks for your patience :)")
            return
        try:
            # getting info
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information... This could take a few seconds, so please be patient!")
            squad_data = await fetch_squad(squad)
            user_data = await fetch_squad_users(squad_data)
            stats = parse_data(user_data, squad_data, squad)

            # creating stat
            await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
            stat_card = discord.File(fp=squad_image.create_stat_card(stats=stats), filename="stat_card.png")

            #adding view and sending message
            view = menu_paginator.first_view(stats["users"], squad, 180)
            await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
            view.response = await interaction.original_response()
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            await interaction.edit_original_response(content="Uhoh, an error occured!")
    else:
        await interaction.response.send_message(f"\"{squad}\" is not a valid squad!", ephemeral=True)