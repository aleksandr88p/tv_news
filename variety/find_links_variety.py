"""
https://variety.com
Variety (Film News, and TV News)

https://variety.com/v/film/news/
https://variety.com/v/film/news/page/2/

https://variety.com/v/tv/news/
https://variety.com/v/tv/news/page/2/
"""

import json

import requests
from bs4 import BeautifulSoup


import requests


def find_links_variety():
    cookies = {
        'pmcsc_sub_unknownip': 'true',
        'usprivacy': '1---',
        'vy_fonts_loaded': '1',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+May+22+2023+21%3A27%3A36+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fvariety.com%2Fv%2Ffilm%2Fnews%2F&groups=C0002%3A1%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1',
        'omni_visit_id': 'variety.1684782739565.1d1281e6-6d8e-43fc-b7ee-805cff53395c',
        '_ga_S6DEFT20P4': 'GS1.1.1684782739.1.1.1684783656.0.0.0',
        '_ga': 'GA1.1.240073813.1684782740',
        'OneTrustWPCCPAGoogleOptOut': 'true',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'pmcsc_sub_unknownip=true; usprivacy=1---; vy_fonts_loaded=1; OptanonConsent=isGpcEnabled=0&datestamp=Mon+May+22+2023+21%3A27%3A36+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fvariety.com%2Fv%2Ffilm%2Fnews%2F&groups=C0002%3A1%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1; omni_visit_id=variety.1684782739565.1d1281e6-6d8e-43fc-b7ee-805cff53395c; _ga_S6DEFT20P4=GS1.1.1684782739.1.1.1684783656.0.0.0; _ga=GA1.1.240073813.1684782740; OneTrustWPCCPAGoogleOptOut=true',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.get('https://variety.com/v/film/news/', headers=headers)
    page1 = response.text
    soup = BeautifulSoup(page1, 'lxml')
    variety_film_news = []
    all_links = soup.find('section', attrs={'class': 'latest-news-river'}).find_all('a', attrs={'class': 'c-title__link'})
    for link in all_links:
        title = link.text.strip()
        url = link['href']
        variety_film_news.append(url)

    response2 = requests.get('https://variety.com/v/tv/news/', headers=headers)
    page2 = response2.text
    soup2 = BeautifulSoup(page2, 'lxml')
    variety_tv_news = []
    all_links2 = soup2.find('section', attrs={'class': 'latest-news-river'}).find_all('a', attrs={'class': 'c-title__link'})
    for link in all_links2:
        title = link.text.strip()
        url = link['href']
        variety_tv_news.append(url)

    return {'variety_film_news': variety_film_news, 'variety_tv_news': variety_tv_news}

someDict = find_links_variety()

print(json.dumps(someDict, indent=4))
