import json

import requests
from bs4 import BeautifulSoup
import datetime


def find_links_indiwire():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.indiewire.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    def get_links_from_page(url, headers):
        response = requests.get(url, headers=headers)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        all_items = soup.find('div', attrs={'data-alias': 'cards__inner-wrapper'}).find_all('div', attrs={
            'data-alias': 'card__card-title'})
        links = []
        for item in all_items:
            link = item.find('a')['href']
            links.append(link)
        return links

    indiwire_film = get_links_from_page('https://www.indiewire.com/t/film/', headers)
    indiwire_film += get_links_from_page('https://www.indiewire.com/t/film/page/2/', headers)

    indiwire_tv = get_links_from_page('https://www.indiewire.com/t/tv/', headers)
    indiwire_tv += get_links_from_page('https://www.indiewire.com/t/tv/page/2/', headers)

    return {'indiwire_film': indiwire_film, 'indiwire_tv': indiwire_tv}


def find_article_indiwire(table_name, link):
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

    # sometimes data_component has different values
    data_component = soup.find('div', attrs={"data-component": "template-article"}) or soup.find('div', attrs={
        "data-component": "template-video"}) or soup.find('div', attrs={"data-component": "template-hub-package"})

    try:
        title = data_component.find('h1').text.strip()
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        if data_component.find('div', attrs={"data-template": 'article'}):
            all_p = data_component.find('div', attrs={'data-template': 'article'}).find_all('p')
        elif data_component.find('div', attrs={"data-template": 'hub'}):
            all_p = data_component.find('div', attrs={'data-template': 'hub'}).find_all('p')

        for p in all_p:
            article += f"{p.text.strip()} "

    except Exception as e:
        print(f'error {e}\ncant find article in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': article,
            'date_time': str(datetime.datetime.now())}



