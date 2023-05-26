import datetime
import json
import random
import time

import requests
from bs4 import BeautifulSoup


def find_article_indiwire(table_name, link):
    '''
    что то надо сделать с table_name, может записывать в БД прям в этой функции
    :param table_name:
    :param link:
    :return: думаю возвращать имя таблицы, статью, ссылку и дату парсинга( все в словаре)
    '''
    cookies = {
        'usprivacy': '1---',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+23+2023+19%3A10%3A30+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1&AwaitingReconsent=false',
        'omni_visit_id': 'pmc.1684861701386.3ca978c1-1bcf-4d92-b24c-fbc54285c5c7',
        '_ga_3QZ1BLEPP5': 'GS1.1.1684861701.1.1.1684861830.0.0.0',
        '_ga': 'GA1.1.854944783.1684861701',
        'OneTrustWPCCPAGoogleOptOut': 'true',
    }

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

links = [
    "https://www.indiewire.com/criticism/movies/asteroid-city-review-wes-anderson-1234866295/",
    "https://www.indiewire.com/news/breaking-news/matt-damon-oblivious-barbie-oppenheimer-box-office-battle-1234866583/",
    "https://www.indiewire.com/news/breaking-news/bella-thorne-short-film-taormina-film-fest-1234866601/",
    "https://www.indiewire.com/news/breaking-news/florence-pugh-indie-film-pissed-off-joined-mcu-1234866559/",
    "https://www.indiewire.com/news/business/cannes-2023-film-market-sales-so-far-1234863378/",
    "https://www.indiewire.com/features/interviews/jim-jarmusch-man-ray-squrl-1234866511/",
    "https://www.indiewire.com/news/breaking-news/christopher-abbott-yorgos-lanthimos-poor-things-1234866283/",
    "https://www.indiewire.com/news/breaking-news/natalie-portman-wants-to-return-to-star-wars-1234866221/",
    "https://www.indiewire.com/news/breaking-news/michelle-rodriguez-fast-furious-spinoffs-1234866192/",
    "https://www.indiewire.com/gallery/best-mermaid-movies/",
    "https://www.indiewire.com/news/box-office/john-wick-4-vod-super-mario-bros-1234866141/",
    "https://www.indiewire.com/gallery/classic-disney-remakes-ranked/",
    "https://www.indiewire.com/news/breaking-news/sam-levinson-defends-the-idol-1234866529/",
    "https://www.indiewire.com/gallery/best-lgbtq-tv-shows/",
    "https://www.indiewire.com/features/craft/emmys-2023-best-costume-contenders-wednesday-diplomat-1923-1234863179/",
    "https://www.indiewire.com/news/breaking-news/aubrey-plaza-binged-the-sopranos-1234866176/",
    "https://www.indiewire.com/news/breaking-news/every-tv-film-production-affected-wga-strike-1234860037/",
    "https://www.indiewire.com/news/breaking-news/melissa-mccarthy-physically-ill-volatile-set-experience-1234866019/",
    "https://www.indiewire.com/criticism/shows/barry-season-4-episode-7-review-a-nice-meal-spoilers-1234865020/",
    "https://www.indiewire.com/criticism/shows/succession-season-4-episode-9-review-church-and-state-spoilers-1234865434/",
    "https://www.indiewire.com/news/breaking-news/adam-mckay-succession-series-finale-1234865359/",
    "https://www.indiewire.com/features/craft/bill-hader-barry-season-4-directing-toolkit-interview-1234861460/",
    "https://www.indiewire.com/features/craft/the-other-two-episode-4-black-white-pleasantville-homage-1234863344/",
    "https://www.indiewire.com/features/interviews/mrs-davis-ending-finale-explains-origins-ai-app-spoilers-1234864629/"
]


# for link in links:
#     d = find_article_indiwire('k', link)
#     print(json.dumps(d, indent=4))
#     time.sleep(random.randint(1, 3))