from utils.commands.squad.get_squad_stats import fetch_squad, fetch_squad_users, parse_data
from utils.commands.squad import squad_image, menu_paginator


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import functions

async def squad_command(client, squad, interaction):
    if squad in client.squad_list:
        try:
            # getting info
            await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information... This could take a few seconds, so please be patient!")
            squad_data = await fetch_squad(squad)
            user_data = await fetch_squad_users(squad_data)
            stats = parse_data(user_data, squad_data, squad)

            # creating stat
            await interaction.edit_original_response(content="<a:loading1:1295503606077980712>  Creating stat card...")
            stat_card = functions.convert_to_discord(squad_image.create_stat_card(stats=stats, profile_image=None))

            #adding view and sending message
            view = menu_paginator.first_view(stats["users"], squad, 180)
            await interaction.edit_original_response(content="", attachments=[stat_card], view=view)
            view.response = await interaction.original_response()
        except Exception as e:
            print(e)
            await interaction.edit_original_response(content="Uhoh, an error occured!")
    else:
        await interaction.response.send_message(f"\"{squad}\" is not a valid squad!", ephemeral=True)