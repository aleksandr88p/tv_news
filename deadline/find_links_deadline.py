"""
https://deadline.com
Deadline (Film and TV)


https://deadline.com/v/film/
https://deadline.com/v/film/page/2/


https://deadline.com/v/tv/
https://deadline.com/v/tv/page/2/
"""

import json

import requests
from bs4 import BeautifulSoup

def find_links_deadline():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    response1 = requests.get('https://deadline.com/v/film/', headers=headers)
    page1 = response1.text
    soup1 = BeautifulSoup(page1, 'lxml')
    all_items1 = soup1.find_all('div', 'river-story')
    deadline_film = []

    for item in all_items1:
        title = item.find('h3', attrs={'class': 'c-title'}).text.strip()
        link = item.find('h3', attrs={'class': 'c-title'}).find('a')['href']
        deadline_film.append(link)


    response2 = requests.get('https://deadline.com/v/tv/', headers=headers)
    page2 = response2.text
    soup2 = BeautifulSoup(page2, 'lxml')
    all_items2 = soup2.find_all('div', 'river-story')
    deadline_tv = []

    for item in all_items2:
        title = item.find('h3', attrs={'class': 'c-title'}).text.strip()
        link = item.find('h3', attrs={'class': 'c-title'}).find('a')['href']
        deadline_tv.append(link)


    return {'deadline_film': deadline_film, 'deadline_tv': deadline_tv}


d = find_links_deadline()

print(json.dumps(d, indent=4))