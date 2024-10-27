import requests
from bs4 import BeautifulSoup
import time
import aiohttp
import asyncio
from discord import app_commands
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

    info = {
        "squad": squad_name,
        "member_count": member_count,
        "kdr": kdr,
        "kpm": kpm,
        "level": squad_stats["average_level"],
        "xp": squad_stats["xp"],
        "kills": kills,
        "deaths": deaths,
        "classic wins": classic_wins,
        "br wins": br_wins,
        "kills_elo": kills_elo,
        "games_elo": games_elo
    }

    return info


# async API call
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
    
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
            tasks.append(scrape(session, uid))
        
        # Execute all requests concurrently
        api_stats = await asyncio.gather(*tasks)
        
        return api_stats
    
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


'''async def username_autocomplete(current):
    if len(current) == 0:
        users = {'SAUNA MAKKARA': '5a4d14e9bfea71227e1fc4bf', 'TheyTookMyChat': '610dc399fd3c7a560e43287a', 'DEEBS': '5f2f9ee9bfea71685aa1e3f2', 'Walrus': '5fc9142ad142af9d623787a1', 'redrum': '5c382ee5d142af341a8053b2', 'Froggy': '6484dbc3d142af01608f2bdf', 'Grenade Bot': '61674a4efe3c7aff128efa73', 'geedolphin': '606c7b9dd142af4c188d9439', 'Nachtfalke': '5fe46c35fd3c7ac26198cf0c', 'Milan Kundera': '60a6a302d142af1f1d389c83', 'Y_Not!': '60006e69fd3c7ae8191e0cb4', 'Doki Doki': '5fb961e0d142af8b4885c87d', 'Tekker': '5f3d25e6fe3c7a43054828fa', 'Milan': '5aeba7b4fd3c7a805dbbd69d', 'Norw12': '647457c7bfea71f84a834ba2', 'Pandalorian': '5f5ac5bebfea715955d07e20', 'Alex140': '623f320bbfea718964e5b257', 'Nhat Huy': '6288fb09fe3c7a1319592978', 'BerzerkinG': '5d988fa4fe3c7a484cbe8cba', 'EncryptR_': '5e57527efe3c7acc73342809', 'ZZBeany': '5f2c63f1bfea71b305e60c98', 'Slayer': '61b18818fd3c7aa31f0e4aee', 'Nandy': '5d0fb3a0bfea71355fef4595', 'Guest1': '5db1f95fbfea71c96e8b4592', 'Guest97977': '5d45f84bfd3c7a8e36f1e671'}
        return [
            app_commands.Choice(name=user, value=users[user]) 
            for user in users
        ] 
    elif len(current) < 2:
        return [
                app_commands.Choice(name="Enter more than 1 character to search!", value="too_short")
            ]
    
    usernames = await get_autocomplete(current)
    return [
        app_commands.Choice(name=username, value=usernames[username]) 
        for username in usernames
    ]'''


'''squad_data = asyncio.run(fetch_squad('UMS'))
print(squad_data)
user_stats = asyncio.run(fetch_squad_users(squad_data))

info = parse_data(user_stats, squad_data, squad_name)

print(info)'''