"""
https://www.hollywoodreporter.com
The Hollywood Reporter (Film News, and TV News)
"""
import json

import requests
from bs4 import BeautifulSoup


def find_links_hollywoodreporter():
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
    """
    'https://www.hollywoodreporter.com/c/movies/movie-news/page/{n}/'
    на первой странице, встречаются результаты которые были и вчера. Возможно и не надо будет переключаться на следующую
    """

    response = requests.get('https://www.hollywoodreporter.com/c/movies/movie-news/', headers=headers)
    page1 = response.text
    soup = BeautifulSoup(page1, 'lxml')
    all_items = soup.find_all('div', attrs={"class": "story lrv-u-padding-tb-1 lrv-u-padding-tb-150@desktop // u-border-dotted-b lrv-u-border-color-grey-dark lrv-u-border-b-1"})
    hollywoodreporter_movies_news = []

    for item in all_items:
        tit_and_url = item.find('h3').find('a')
        title = tit_and_url.text.strip()
        url = tit_and_url['href']
        hollywoodreporter_movies_news.append(url)


    response2 = requests.get('https://www.hollywoodreporter.com/c/tv/tv-news/', headers=headers)
    page2 = response2.text
    soup2 = BeautifulSoup(page2, 'lxml')
    all_items2 = soup2.find_all('div', attrs={"class": "story lrv-u-padding-tb-1 lrv-u-padding-tb-150@desktop // u-border-dotted-b lrv-u-border-color-grey-dark lrv-u-border-b-1"})
    hollywoodreporter_tv_news = []
    for item in all_items2:
        tit_and_url = item.find('h3').find('a')
        title = tit_and_url.text.strip()
        url = tit_and_url['href']
        hollywoodreporter_tv_news.append(url)

    return {'hollywoodreporter_movies_news': hollywoodreporter_movies_news, 'hollywoodreporter_tv_news': hollywoodreporter_tv_news}



# someDict = find_links_hollywoodreporter()
#
# print(json.dumps(someDict, indent=4))

