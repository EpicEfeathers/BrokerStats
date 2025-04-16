import requests, pprint

maps = {
	0: 'Desert',
	1: 'Northwest',
	2: 'Pacific',
	3: 'Office',
	4: 'Flooded',
	5: 'Temple',
	6: 'Escape',
	7: 'Southwest',
	8: 'Remagen',
    9: 'Battle Royale Map',
	13: 'City Point',
	14: 'Tomb',
	15: 'The Somme',
    17: 'Dead End City Map',
	18: 'Tribute',
	19: 'Cyber Tribute',
	20: 'Moonbase',
	21: 'Area 15 Base',
	22: 'Area 15 Bunker',
	24: 'Skullisland',
	25: 'Hanger',
	27: 'Quarry',
	28: 'Dwarfsdungeon',
	29: 'Kitchen',
	31: 'Frontier',
	32: 'Heist',
	33: 'Tower Of Power',
	34: 'Three Lane',
	35: 'Sniper Alley',
	36: 'Pyramid',
	37: 'Containers',
	38: 'Spacestation',
	39: 'Siege',
	40: 'Crisscross',
	41: 'Snipers Only',
	43: 'Zen Garden',
	44: 'Cologne',
	47: 'Goldmine',
	49: 'Goldmine V2'
}

modes = {
	128: "Team Death Match",
	138: "Missile Launch",
	275: "Bomb Disposal",
	135: "Capture Points",
	136: "Vehicle Escort",
	15: "Gun Game",
}

def process_server_data(data, all_servers=False, region="USA"):
    servers = []
    for i in range(0, len(data), 6): # range(start, stop, step)

        player_count = int(data[i+4])
        mode = modes.get(int(data[i+3]), None) # if doesn't exist, use None
        wb_map = maps.get(int(data[i+5]), "New map that I don't have data for :P") # if doesn't exist, tell user haha
        server_name = data[i+1]

        if (not all_servers and player_count == 0) or (region not in server_name): # checks if only looking for servers with players on them
            continue

        server = {
            "server_name": server_name,     
            "mode": mode, 
            "player_count": player_count, 
            "map": wb_map}

        servers.append(server) # adds the remaining values to the list

    return servers