import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from discord import app_commands

# async API call
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
    
async def scrape(session, uid):
    URL = f"https://stats.warbrokers.io/players/i/{uid}"
    async with session.get(URL) as page:
        content = await page.text()
        soup = BeautifulSoup(content, "html.parser")

        div = soup.find("div", class_= "determinate")
        progress_percentage = div.find('span', class_='progressPercentage').get_text()
        player_stats = {"progressPercentage": progress_percentage}

        stats = soup.find_all('div', class_='player-details-number-box-grid')

        for stat in stats:
            header = stat.find('div', class_='player-details-number-box-header').get_text(strip=True).lower()
            value = stat.find('div', class_='player-details-number-box-value').get_text(strip=True)
            player_stats[header] = value

        return player_stats

async def fetch_all(uid):
    async with aiohttp.ClientSession() as session:
        # Prepare all the URLs
        api_url = f"https://wbapi.wbpjs.com/players/getPlayer?uid={uid}"
        kills_url = f"https://wbapi.wbpjs.com/players/percentile/killsElo?uid={uid}"
        games_url = f"https://wbapi.wbpjs.com/players/percentile/gamesElo?uid={uid}"
        xp_percentile_url = f"https://wbapi.wbpjs.com/players/percentile/xp?uid={uid}"
        
        # Gather all the requests
        tasks = [
            fetch(session, api_url),
            fetch(session, kills_url),
            fetch(session, games_url),
            fetch(session, xp_percentile_url),
            scrape(session, uid)
        ]
        
        # Execute all requests concurrently
        api_stats, kills_elo, games_elo, xp_percentile, scraped_data = await asyncio.gather(*tasks)
        
        deaths_per_weapon = api_stats["deaths"]
        # Process the results
        api_stats["killsEloPercentile"] = round(kills_elo, 1)
        api_stats["gamesEloPercentile"] = round(games_elo, 1)
        api_stats["xpPercentile"] = round(xp_percentile, 1)

        api_stats.update(scraped_data)
        api_stats["kills"] = str(sum(api_stats["kills_per_weapon"].values()))
        api_stats["deaths"] = str(sum(deaths_per_weapon.values()))
        api_stats["kills / death"] = int(api_stats["kills"]) / int(api_stats["deaths"])
        
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


async def username_autocomplete(current):
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
    ]