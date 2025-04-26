from datetime import datetime

from utils.database_stuff import functions


async def get_stats(bot):
    total_users, user_ids = functions.total_users()

    user_data = [[await bot.fetch_user(user[0]), user[0], functions.fetch_message_count_by_uid(user[0])] # get all specific user information, allows for easier sorting
                 for user in user_ids]
    
    sorted_user_data = sorted(user_data, key= lambda x: x[2], reverse=True) # sorting the list by user message count

    formatted_users = '\n'.join(f"{user[0]} ({user[1]}): {user[2]}" for user in sorted_user_data) # format and join

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
        "users": formatted_users,
    }

    return stats