import requests
import time


def get_playercount():
    link = "https://raw.githubusercontent.com/EpicEfeathers/wb/main/data/total_playercount.csv"
    results = requests.get(link).text

    results = results.split("\n")
    results = results[-49] # Value from 1 day ago (48 half hours)

    return results


def return_data(): # SPEED THIS UP
    start = time.time()
    data = get_playercount()
    print(time.time() -start)

    start = time.time()
    current = int(requests.get("https://wbapi.wbpjs.com/status/playerCount").text)
    print(time.time() - start)
    yesterday = int(data.replace("\r", "").split(",")[1]) # don't get timestamp

    return current, yesterday
