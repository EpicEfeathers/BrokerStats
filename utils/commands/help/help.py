import discord
import datetime

def help(bot):
    embed=discord.Embed(title="**Help**", color=0xfa3b06, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_author(name="Broker Stats", icon_url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1295439550356918423/1304897010847191131/bot_logo.png?ex=67310f8b&is=672fbe0b&hm=77add4dce4676937b9fc6142ae418f9d2c4dfc87f2dda632ebb68eaedd7442aa&')

    stats = bot.tree.get_command("stats")
    embed.add_field(name="</stats:1295437878654144515>", value=f":chart_with_upwards_trend: {stats.description}\nLink your own stats using </linkstats:1296119982429831168>.", inline=False)

    linkstats = bot.tree.get_command("linkstats")
    embed.add_field(name="</linkstats:1296119982429831168>", value=f":link: {linkstats.description}\nUse this command to link your stats page to the bot.", inline=False)

    squad = bot.tree.get_command("squad")
    embed.add_field(name="</squad:1299897695854395453>", value=f":bar_chart: {squad.description}\nSee a detailed overview of a squad.", inline=False)

    leaderboard = bot.tree.get_command("leaderboard")
    embed.add_field(name="</leaderboard:1331305581587337297>", value=f":medal: {leaderboard.description}\nSee top daily or lifetime leaderboards.", inline=False)

    help = bot.tree.get_command("help")
    embed.add_field(name="</help:1316396080359018598>", value=f":question: {help.description}\nDisplays this command.", inline=False)

    broker_stats = bot.tree.get_command("broker_stats")
    embed.add_field(name="</broker_stats:1331305581587337298>", value=f":1234: {broker_stats.description}\nReturns basic stats on the bot itself.", inline=False)

    last_seen = bot.tree.get_command("last_seen")
    embed.add_field(name="</last_seen:1364015029216874627>", value=f":hourglass: {last_seen.description}\nReturns a list of all squad members most recent playtimes.", inline=False)

    trends = bot.tree.get_command("trends")
    embed.add_field(name="</trends:1363307522303201341>", value=f":plus: {trends.description}\nShows game trends (like playercount) over a specified period.", inline=False)

    warbrokers = bot.tree.get_command("warbrokers")
    embed.add_field(name="</warbrokers:1361892723744837762>", value=f":video_game: {warbrokers.description}\nShows some basic stats about the game itself.", inline=False)


    return embed