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

    response1 = requests.get('https://www.indiewire.com/t/film/', headers=headers)
    page1 = response1.text
    soup1 = BeautifulSoup(page1, 'lxml')
    all_items1 = soup1.find('div', attrs={'data-alias': 'cards__inner-wrapper'}).find_all('div', attrs={'data-alias': 'card__card-title'})
    indiwire_film = []
    for item in all_items1:
        link = item.find('a')['href']
        title = item.find('a').text.strip()
        indiwire_film.append(link)


    response2 = requests.get('https://www.indiewire.com/t/tv/', headers=headers)
    page2 = response2.text
    soup2 = BeautifulSoup(page2, 'lxml')
    all_items2 = soup2.find('div', attrs={'data-alias': 'cards__inner-wrapper'}).find_all('div', attrs={'data-alias': 'card__card-title'})
    indiwire_tv = []
    for item in all_items2:
        link = item.find('a')['href']
        title = item.find('a').text.strip()
        indiwire_tv.append(link)

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

    try:
        title = soup.find('div', attrs={"data-component": "template-article"}).find('h1').text.strip()
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        all_p = soup.find('div', attrs={"data-component": "template-article"}).find('div', attrs={'data-template': 'article'}).find_all('p')
        for p in all_p:
            article += f"{p.text.strip()} "
    except Exception as e:
        print(f'error {e}\ncant find artcicle in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': article,
            'date_time': str(datetime.datetime.now())}
