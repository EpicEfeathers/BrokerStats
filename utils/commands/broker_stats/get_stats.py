from datetime import datetime

from utils.database_stuff import functions


async def get_stats(bot):
    total_users, user_ids = functions.total_users()
    users = ''.join([f"\n{await bot.fetch_user(user[0])} ({user[0]}): {functions.fetch_message_count_by_uid(user[0])}" for user in user_ids])
    server_count = len(bot.guilds)
    guild_ids = bot.guilds
    total_messages = functions.message_count()
    total_yearly_messages = functions.message_count(datetime.now().year)


    stats = {
        "server_count": server_count,
        "guilds": guild_ids,
        "total_messages": total_messages,
        "total_yearly_messages": total_yearly_messages,
        "total_users": total_users,
        "user_ids": user_ids,
        "users": users,
    }

    return stats