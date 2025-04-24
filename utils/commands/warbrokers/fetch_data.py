async def fetch_total_players(session):
    async with session.get("https://warbrokers.io/player_count.php") as resp:
        return await resp.text()

async def fetch_playercount(session):
    async with session.get("https://warbrokers.io/players_online.php") as resp:
        return await resp.text()

async def fetch_data(session):
    return await fetch_total_players(session), await fetch_playercount(session)