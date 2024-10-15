import requests
from bs4 import BeautifulSoup
import time
import aiohttp
import asyncio

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
        
        # Process the results
        api_stats["killsEloPercentile"] = round(kills_elo, 1)
        api_stats["gamesEloPercentile"] = round(games_elo, 1)
        api_stats["xpPercentile"] = round(xp_percentile, 1)

        api_stats.update(scraped_data)
        
        return api_stats
