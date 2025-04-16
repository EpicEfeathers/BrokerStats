import requests

def convert_data(data):
    response = str(data.split(f",USA,")[1])
    response = f"USA,{response}" # removes the beginning value e.g. 26,USA,137.220.58.215... -> USA,137.220.58.215...
    
    it = iter(response.split(",")) # converts it into an interable, which remembers its position as you iterate through it
    data = [{"server_name": item[0], "ip": item[1], "player_count": int(item[2])} for item in zip(it, it, it)] # when you do this, it takes three items, and adds them. Since it's an iterable, it remembers its position

    data_filtered = [server for server in data if "beta" not in server["server_name"].lower() and "clan" not in server["server_name"].lower()] # removes clan and beta servers

    data_sorted = sorted(data_filtered, key=lambda x: x["server_name"], reverse=True) # sorts by server name (reversed so on plot it goes downwards)

    return data_sorted

def get_data():
    data = requests.get("https://store1.warbrokers.io/301/get_player_list.php").text
    return convert_data(data)