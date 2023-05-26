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

    response = requests.get('https://variety.com/v/film/news/', headers=headers)
    page1 = response.text
    soup = BeautifulSoup(page1, 'lxml')
    variety_film_news = []
    all_links = soup.find('section', attrs={'class': 'latest-news-river'}).find_all('a',
                                                                                    attrs={'class': 'c-title__link'})
    for link in all_links:
        title = link.text.strip()
        url = link['href']
        variety_film_news.append(url)

    response2 = requests.get('https://variety.com/v/tv/news/', headers=headers)
    page2 = response2.text
    soup2 = BeautifulSoup(page2, 'lxml')
    variety_tv_news = []
    all_links2 = soup2.find('section', attrs={'class': 'latest-news-river'}).find_all('a',
                                                                                      attrs={'class': 'c-title__link'})
    for link in all_links2:
        title = link.text.strip()
        url = link['href']
        variety_tv_news.append(url)

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
