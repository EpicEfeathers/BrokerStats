import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from datetime import datetime, timezone

import json


def parse_data(user_data, squad_stats, squad_name):
    member_count = squad_stats['member_count']
    kills = sum(int(user["kills"].replace(',',"")) for user in user_data)
    deaths = sum(int(user["deaths"].replace(',',"")) for user in user_data)
    kdr = round(kills/deaths, 1)
    kpm = round(sum(float(user["kills / min"].replace(',',"")) for user in user_data) / member_count, 1)

    br_wins = sum(int(user["battle royale wins"].replace(',',"")) for user in user_data)
    classic_wins = sum(int(user["classic mode wins"].replace(',',"")) for user in user_data)

    kills_elo = round(sum(int(user["killsELO"]) for user in squad_stats['members']) / member_count, 1)
    games_elo = round(sum(int(user["gamesELO"]) for user in squad_stats['members']) / member_count, 1)

    active_players = 0
    for user in user_data:
        if datetime.now(timezone.utc).timestamp() - user["time"] < 604800: # 604800s = 1 week
            active_players += 1

    users = [user['nick'] for user in squad_stats['members']]

    info = {
        "squad": squad_name,
        "member_count": member_count,
        "active_players": active_players,
        "kdr": kdr,
        "kpm": kpm,
        "level": squad_stats["average_level"],
        "xp": squad_stats["xp"],
        "kills": kills,
        "deaths": deaths,
        "classic wins": classic_wins,
        "br wins": br_wins,
        "kills_elo": kills_elo,
        "games_elo": games_elo,
        "users": users
    }

    return info


# async API call
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_time(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data.get("time")
    
async def scrape(session, uid):
    URL = f"https://stats.warbrokers.io/players/i/{uid}"
    async with session.get(URL) as page:
        content = await page.text()
        soup = BeautifulSoup(content, "html.parser")
        
        player_stats = {}
        stats = soup.find_all('div', class_='player-details-number-box-grid')

        for stat in stats:
            header = stat.find('div', class_='player-details-number-box-header').get_text(strip=True).lower()
            value = stat.find('div', class_='player-details-number-box-value').get_text(strip=True)
            player_stats[header] = value

        return player_stats

async def fetch_squad(squad):
    async with aiohttp.ClientSession() as session:
        # Prepare all the URLs
        api_url = f"https://wbapi.wbpjs.com/squad/getSquadMembers?squadName={squad}"
        
        api_stats = await asyncio.gather(fetch(session, api_url))

        db_data = api_stats[0]
        squad_member_count = len(db_data)
        total_level = sum(user["level"] for user in db_data)
        total_xp = sum(user["xp"] for user in db_data)
        average_level = round(total_level/squad_member_count, 1)
        
        squad_data = {
            "member_count": squad_member_count, 
            "level": total_level,
            "average_level": average_level,
            "xp": total_xp,
            "members": db_data
        }
        return squad_data
    
async def fetch_squad_users(squad_stats):
    uids = [member['uid'] for member in squad_stats["members"]]
    async with aiohttp.ClientSession() as session:

        tasks = []
        for uid in uids:
            tasks.append(fetch_time(session, f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}"))
            tasks.append(scrape(session, uid))
        
        # Execute all requests concurrently
        api_stats = await asyncio.gather(*tasks)
        #print(json.dumps(api_stats, sort_keys=True, indent=4))

        new_list = []
        for i in range(len(api_stats)):
            if i % 2 == 0:
                api_stats[i+1]["time"] = api_stats[i]
                new_list.append(api_stats[i+1])
        #print(json.dumps(new_list, sort_keys=True, indent=4))

        return new_list
        
    
def get_autocompletion(query):
    response = requests.get(f"https://wbapi.wbpjs.com/players/searchByName?query={query}").json()

    nicks = []
    for entry in response:
        nicks.append(entry["nick"])

    if "PleaseChangeNick" in nicks:
        nicks.remove("PleaseChangeNick")

    def thing(x):
        return (not x.lower().startswith("hit"), x)
    
    nicks = sorted(nicks, key=thing)

    return nicks

async def get_autocomplete(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://wbapi.wbpjs.com/players/searchByName?query={query}') as resp:
            if resp.status == 200:
                data = await resp.json()  # Assuming the API returns JSON
        
                # turns list of dictionaries into 1 dict
                users = {}
                for datum in data:
                    users[datum["nick"]] = datum["uid"]

                #removes banned / changes nicknames from the list
                users.pop("PleaseChangeNick", None)
                # sorts with anything starting with the query first
                def thing(x):
                    return (not x[0].lower().startswith(query), x[0])
                sorted_ = sorted(users.items(), key=thing)

                users = {}
                for user in sorted_:
                    users[user[0]] = user[1]

            else:
                users = []

    return users


'''squad_data = asyncio.run(fetch_squad('UMS'))
user_stats = asyncio.run(fetch_squad_users(squad_data))
info = parse_data(user_stats, squad_data, "UMS")

print(info)'''