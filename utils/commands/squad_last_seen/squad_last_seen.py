from utils.commands.squad_last_seen import get_data, menu_paginator
import aiohttp

async def squad_last_seen(bot, interaction, squad, page_num):
    if squad in bot.squad_list:
        await interaction.response.send_message(content="<a:loading1:1295503606077980712>  Grabbing information...")

        uids = await get_data.get_squad_users(bot.session, squad)
        data = await get_data.get_all_data(bot.session, uids)

        data = get_data.sort_data("sort_asc", data)
        code_block = get_data.create_code_block(data, start_index=0, end_index=24)


        view = menu_paginator.Paginator(interaction.user.id, data, 180)
        await interaction.edit_original_response(content=code_block, view=view)
    else:
        await interaction.response.send_message(f"'{squad}' is not a valid squad.", ephemeral=True)