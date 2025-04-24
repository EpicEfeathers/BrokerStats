async def fetch_total_players(session):
    async with session.get("https://warbrokers.io/player_count.php") as resp:
        return resp.text()

async def fetch_playercount(session):
    async with session.get("https://warbrokers.io/players_online.ph") as resp:
        return resp.text()

async def fetch_data(session):
    return fetch_total_players(session), fetch_playercount(session)