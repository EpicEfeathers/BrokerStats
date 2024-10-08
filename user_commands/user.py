import discord
import datetime

from user_commands import user_stats

def user(client):
    @client.tree.command()
    async def user(interaction: discord.Interaction):

        await interaction.response.defer(thinking=True)
        user = user_stats.get_user("609aa68ed142afe952202c5c")
        user_name = user["name"]

        embed=discord.Embed(title=f"{user_name}'s stats", description=f"UID: `609aa68ed142afe952202c5c`", timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Level", value=f"{user["level"]}\n{user["progressPercentage"]}", inline=False)
        embed.add_field(name="Kills", value=user["kills"], inline=True)
        embed.add_field(name="Death", value=user["deaths"], inline=True)
        embed.add_field(name="KDR", value=(round(int(user["kills"])/int(user["deaths"]), 2)), inline=True)
        embed.add_field(name="KPM", value=user["kills / min"], inline=True)
        await interaction.followup.send(embed=embed)

        print(user)