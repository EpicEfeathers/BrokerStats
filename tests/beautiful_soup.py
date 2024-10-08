import requests
from bs4 import BeautifulSoup
import time

start = time.time()

URL = "https://stats.warbrokers.io/players/i/609aa68ed142afe952202c5c"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

div = soup.find("div", class_= "determinate")
span_text = div.find('span', class_='progressPercentage').get_text()
print(span_text)

stats = soup.find_all('div', class_='player-details-number-box-grid')

player_stats = {}

for stat in stats:
    header = stat.find('div', class_='player-details-number-box-header').get_text(strip=True).lower()
    value = stat.find('div', class_='player-details-number-box-value').get_text(strip=True)
    player_stats[header] = value


print(time.time() - start)