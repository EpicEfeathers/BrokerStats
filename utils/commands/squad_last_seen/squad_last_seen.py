from utils.commands.squad_last_seen import get_data

async def squad_last_seen(bot, interaction, view, data, squad):
    if squad in bot.squad_list:
        code_block = get_data.create_code_block(data, start_index=0, end_index=24)

        await interaction.edit_original_response(content=code_block, view=view)
    else:
        await interaction.response.send_message(f"'{squad}' is not a valid squad.", ephemeral=True)