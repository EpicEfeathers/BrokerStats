import time


async def get_playercount(session):
    link = "https://raw.githubusercontent.com/EpicEfeathers/wb/main/data/total_playercount.csv"
    async with session.get(link) as resp:
        results = await resp.text()

    results = results.split("\n")
    results = results[-49] # Value from 1 day ago (48 half hours)

    return results


async def return_data(session): # SPEED THIS UP
    start = time.time()
    data = get_playercount()
    print(time.time() -start)

    start = time.time()

    link = "https://wbapi.wbpjs.com/status/playerCoun"
    async with session.get(link) as resp:
        current = int(await resp.text())
    print(time.time() - start)
    yesterday = int(data.replace("\r", "").split(",")[1]) # don't get timestamp

    return current, yesterday
