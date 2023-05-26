import json

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

    def get_links_from_page(url, headers):
        response = requests.get(url, headers=headers)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        all_items = soup.find_all('div', 'river-story')
        links = []
        for item in all_items:
            link = item.find('h3', attrs={'class': 'c-title'}).find('a')['href']
            links.append(link)
        return links

    deadline_film = get_links_from_page('https://deadline.com/v/film/', headers)
    deadline_film += get_links_from_page('https://deadline.com/v/film/page/2/', headers)

    deadline_tv = get_links_from_page('https://deadline.com/v/tv/', headers)
    deadline_tv += get_links_from_page('https://deadline.com/v/tv/page/2/', headers)

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

