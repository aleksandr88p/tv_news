import requests
from bs4 import BeautifulSoup
import datetime

from for_database import create_connection, check_article_exists, insert_article, close_connection
def find_links_deadline():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
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

def find_article_deadline(table_name, link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    response = requests.get(
        url=link,
        headers=headers,
    )

    soup = BeautifulSoup(response.text, 'lxml')
    title = ''
    article = ''
    try:
        title = soup.find('h1', attrs={'class': 'c-title'}).text.strip()
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        all_p = soup.find('article').find_all('p', attrs={"class": "paragraph"})
        for p in all_p:
            article += f"{p.text.strip()} "
    except Exception as e:
        print(f'error {e}\ncant find article in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': article,
            'date_time': str(datetime.datetime.now())}

