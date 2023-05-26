import json

from bs4 import BeautifulSoup
import datetime
import requests


def find_links_variety():
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
        soup = BeautifulSoup(response.text, 'lxml')
        all_links = soup.find('section', attrs={'class': 'latest-news-river'}).find_all('a', attrs={'class': 'c-title__link'})
        return [link['href'] for link in all_links]

    variety_film_news = get_links_from_page('https://variety.com/v/film/news/', headers)
    variety_film_news += get_links_from_page('https://variety.com/v/film/news/page/2/', headers)

    variety_tv_news = get_links_from_page('https://variety.com/v/tv/news/', headers)
    variety_tv_news += get_links_from_page('https://variety.com/v/tv/news/page/2/', headers)

    return {'variety_film_news': variety_film_news, 'variety_tv_news': variety_tv_news}



def find_article_variety(table_name, link):
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

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    title = ''
    article = ''
    try:
        title = soup.find('h1', attrs={'id': 'section-heading'}).text.strip()
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        all_p = soup.find('article').find_all('p', attrs={"class": "paragraph"})
        for p in all_p:
            article += f"{p.text.strip()} "
    except Exception as e:
        print(f'error {e}\ncant find artcicle in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': article,
            'date_time': str(datetime.datetime.now())}


# print(json.dumps(find_links_variety(), indent=4))