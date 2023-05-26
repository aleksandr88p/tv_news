import requests
from bs4 import BeautifulSoup
import datetime
from processing import process_links
from for_database import create_connection, check_article_exists, insert_article, close_connection

def find_links_hollywoodreporter():
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


def find_article_hollywoodreporter(table_name, link):
    headers = {
        'authority': 'www.hollywoodreporter.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.hollywoodreporter.com/c/tv/tv-news/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    title = ''
    first_p = ''
    article = ''
    try:
        title = soup.find('h1', attrs={'class': 'article-title'}).text
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        first_p = soup.find('p', attrs={'class': 'article-excerpt'}).text  # первая строка, которая над фото
    except Exception as e:
        print(f'error {e}\ncant find first_p in {link}')

    try:
        article += f"{first_p}. "
        all_p = soup.find('article').find_all('p', attrs={"class": "paragraph"})
        for p in all_p:
            article += f"{p.text.strip()} "
    except Exception as e:
        print(f'error {e}\ncant find article in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': article,
            'date_time': str(datetime.datetime.now())}

