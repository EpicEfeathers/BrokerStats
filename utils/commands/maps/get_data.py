import asyncio
import aiohttp

SEMAPHORE_LIMIT = 5  # limit num of concurrent calls

locations = ['ASIA', 'ASIA_4V4', 'ASIA_CLAN', 'AS_BATTLE_ROYALE', 'AS_DEAD_CITY', 'AUSTRALIA', 'AUSTRALIA_CLAN', 'DEAD_CITY', 'EUROPE', 'EUROPE_CLAN', 'EU_4V4', 'EU_BATTLE_ROYALE', 'EU_DEAD_CITY', 'INDIA', 'INDIA_CLAN', 'JAPAN', 'JAPAN_CLAN', 'NA_BATTLE_ROYALE', 'NA_DUO_BETA', 'RUSSIA', 'USA', 'USA_4V4', 'USA_BETA', 'USA_CLAN', 'USA_WEST', 'USA_WEST_CLAN']

async def fetch(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            text = await response.text()

            text = text.split(',')[1:] # removes first number, which is the total server count in the region, and is not necessary

            #response = ','.join(text) # joins it back together

            return text

async def fetch_all():
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)  # Limit concurrency

    base_link = "https://store1.warbrokers.io/301/server_list.php?location="
    
    async with aiohttp.ClientSession() as session:
        
        # Gather all the requests
        tasks = [fetch(session, f"{base_link}{location}", semaphore) for location in locations] # loops through locations and gets all the data
        # Execute all requests concurrently
        servers = await asyncio.gather(*tasks)

        servers = [server for sublist in servers for server in sublist] # flattens list of lists to 1 list

        return servers
