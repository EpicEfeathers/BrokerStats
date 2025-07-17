from bs4 import BeautifulSoup
import aiohttp
import asyncio
from discord import app_commands
import config

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

async def fetch_all(session, uid):
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
    api_stats["killsEloPercentile"] = round((100 - kills_elo), 1) # top x% = (100 - percentile). E.g. 95th percentile = Top 5%
    api_stats["gamesEloPercentile"] = round((100 - games_elo), 1) # top x% = (100 - percentile). E.g. 95th percentile = Top 5%
    api_stats["xpPercentile"] = round((100 - xp_percentile), 1) # top x% = (100 - percentile). E.g. 95th percentile = Top 5%

    api_stats.update(scraped_data)
    kills_per_vehicle = api_stats.get("kills_per_vehicle", {}) or {} # if value is null (if player has no kills) then return empty dict instead of breaking
    kills_per_weapon = api_stats.get("kills_per_weapon", {}) or {}
    self_destructs = api_stats.get("self_destructs", {}) or {}

    # calculate kills (vehicle kills (minus the player vechile) + weapon kills)
    api_stats["kills"] = sum(value for key, value in kills_per_vehicle.items() if key != "v30")
    filtered_kills_per_weapon = {key: value for key, value in kills_per_weapon.items() if key not in config.vehicle_weapons}
    api_stats["kills"] += sum(filtered_kills_per_weapon.values())

    # calculate deaths (weapon deaths + self-destructs)
    api_stats["deaths"] = sum(deaths_per_weapon.values())
    api_stats["deaths"] += sum(self_destructs.values())

    # calculate kdr
    api_stats["kills / death"] = api_stats["kills"] / api_stats["deaths"]
    
    return api_stats