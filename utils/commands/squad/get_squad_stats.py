from bs4 import BeautifulSoup
import asyncio
from datetime import datetime, timezone

async def get_all_data(session):
    '''
    Gets the cached data (for every squad)
    '''
    data_url = "https://raw.githubusercontent.com/EpicEfeathers/wb/refs/heads/main/squad_info/squad_data.json"

    async with session.get(data_url) as response:
        return await response.json(content_type=None) # skips checking if it's JSON, just assumes it is

def extract_squad(all_data, squad_name):
    '''
    Gets the specific squad's data from all the squad data
    '''
    try:
        return all_data[squad_name]
    except KeyError:
        print(f"KeyError. Could not find squad '{squad_name}' in the cached data.")


async def get_data(session, squad_name):
    '''
    Gets data for a specific squad
    '''
    all_data = await get_all_data(session)
    squad_data = extract_squad(all_data, squad_name)
    users = await get_squad_users(session, squad_name)

    squad_info = format_data(squad_data, users)

    return squad_info

def format_data(squad_data, users):
    squad_data['kdr'] = round(squad_data['kills'] / squad_data['deaths'], 1) # calculate kdr data
    squad_data['users'] = users
    squad_data['member_count'] = len(users)

    # find averages
    squad_data['kills_elo'] = round(squad_data['kills_elo'] / len(users), 1)
    squad_data['games_elo'] = round(squad_data['games_elo'] / len(users), 1)

    squad_data['level'] = round(squad_data['level'] / len(users))


    return squad_data


async def get_squad_users(session, squad_name):
    squad_url = f"https://wbapi.wbpjs.com/squad/getSquadMembers?squadName={squad_name}"

    async with session.get(squad_url) as response:
        squad_members = await response.json()

    users = {user['nick']: user['uid'] for user in squad_members}

    return users


'''def parse_data(user_data, squad_stats, squad_name):
    member_count = squad_stats['member_count']
    for user in user_data:
        try:
            user['kills']
        except KeyError:
            print(user)
    #kills = sum(int(user["kills"].replace(',',"")) for user in user_data)
    deaths = sum(int(user["deaths"].replace(',',"")) for user in user_data)
    kdr = round(kills/deaths, 1)
    kpm = round(sum(float(user["kills / min"].replace(',',"")) for user in user_data) / member_count, 1)

    br_wins = sum(int(user["battle royale wins"].replace(',',"")) for user in user_data)
    classic_wins = sum(int(user["classic mode wins"].replace(',',"")) for user in user_data)

    kills_elo = round(sum(int(user["killsELO"]) for user in squad_stats['members']) / member_count, 1)
    games_elo = round(sum(int(user["gamesELO"]) for user in squad_stats['members']) / member_count, 1)

    active_players = 0
    for user in user_data:
        print(user)
        if datetime.now(timezone.utc).timestamp() - user["time"] < 604800: # 604800s = 1 week
            active_players += 1

    users = {}
    for user in squad_stats['members']:
        users[user['nick']] = user['uid']
    #users = [user['nick'] for user in squad_stats['members']]

    info = {
        "squad_name": squad_name,
        "member_count": member_count,
        "active_players": active_players,
        "kdr": kdr,
        "kpm": kpm,
        "level": squad_stats["average_level"],
        "xp": squad_stats["xp"],
        "kills": kills,
        "deaths": deaths,
        "classic_wins": classic_wins,
        "br_wins": br_wins,
        "kills_elo": kills_elo,
        "games_elo": games_elo,
        "users": users
    }

    return info'''