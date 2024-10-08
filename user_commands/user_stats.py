import requests
from bs4 import BeautifulSoup


def get_user(uid):
    URL = f"https://stats.warbrokers.io/players/i/{uid}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    div = soup.find("div", class_= "page-header")
    name = div.find(string=True, recursive=False).strip()
    player_stats = {'name': name}


    div = soup.find("div", class_= "determinate")
    progressPercentage = div.find('span', class_='progressPercentage').get_text()

    stats = soup.find_all('div', class_='player-details-number-box-grid')

    player_stats['progressPercentage'] = progressPercentage

    for stat in stats:
        header = stat.find('div', class_='player-details-number-box-header').get_text(strip=True).lower()
        value = stat.find('div', class_='player-details-number-box-value').get_text(strip=True)
        player_stats[header] = value

    return player_stats