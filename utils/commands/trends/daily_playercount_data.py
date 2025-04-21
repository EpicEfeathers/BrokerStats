import requests

def get_playercount():
    link = "https://raw.githubusercontent.com/EpicEfeathers/wb/main/data/playercount.csv"
    results = requests.get(link).text

    results = results.split("\n")
    results = results[-97:-1] # return results for last 2 days (96 half hours). don't get last index as empty string 

    return results

def calculate_average(data, start, end):
    average = 0

    for item in data[start:end]:
        item = item.replace("\r", "").split(",") # remove newline char, and split by comma
        item = item[1:] # remove first index (timestamp)
        for count in item:
            average += int(count)
    return round(average/48)

def get_avgs():
    data = get_playercount()
    average = calculate_average(data, -48, None) # today's data
    yesterday_avg = calculate_average(data, -96, -48)

    return average, yesterday_avg