import datetime
import json
import random
import time

import requests
from bs4 import BeautifulSoup


def find_article_variety(table_name, link):
    '''
    что то надо сделать с table_name, может записывать в БД прям в этой функции
    :param table_name:
    :param link:
    :return: думаю возвращать имя таблицы, статью, ссылку и дату парсинга( все в словаре)
    '''

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
    artcicle = ''
    try:
        title = soup.find('h1', attrs={'id': 'section-heading'}).text.strip()
    except Exception as e:
        print(f'error {e}\ncant find title in {link}')

    try:
        all_p = soup.find('article').find_all('p', attrs={"class": "paragraph"})
        for p in all_p:
            artcicle += f"{p.text.strip()} "
    except Exception as e:
        print(f'error {e}\ncant find artcicle in {link}')

    return {'table_name': table_name, 'title': title, 'link': link, 'article': artcicle,
            'date_time': str(datetime.datetime.now())}



links = [
    "https://variety.com/2023/film/news/joaquin-phoenix-todd-haynes-nc-17-gay-romance-film-1235621942/",
    "https://variety.com/2023/film/news/leon-ichaso-dead-el-cantante-1235621823/",
    "https://variety.com/2023/film/news/the-color-purple-trailer-oprah-winfrey-musical-1235589157/",
    "https://variety.com/vip/film-exhibitors-are-healing-but-amc-theatres-has-longer-path-to-recovery-1235615310/",
    "https://variety.com/2023/film/news/cannes-club-zero-mia-wasikowska-premiere-1235621424/",
    "https://variety.com/2023/film/news/film-production-center-the-fields-studios-rises-in-governor-j-b-pritzker-1235621759/",
    "https://variety.com/shop/best-coffee-table-books-for-movie-lovers-1234729999/",
    "https://variety.com/vip/after-mario-madness-will-animation-stay-strong-at-summer-box-office-1235602030/",
    "https://variety.com/2023/film/news/joshua-burge-joel-potrykus-vulcanizadora-dweck-productions-1235621657/",
    "https://variety.com/2023/film/news/cannes-film-market-inaugural-investors-circle-selected-projects-1235621626/",
    "https://variety.com/2023/film/news/club-zero-review-mia-wasikowska-jessica-hausner-1235621251/",
    "https://variety.com/2023/film/news/fast-and-furious-spinoffs-female-movie-1235621300/",
    "https://variety.com/2023/film/news/alpha-violet-foremost-by-night-cannes-1235621380/",
    "https://variety.com/2023/film/news/crimecon-clue-awards-2023-submission-true-crime-1235619647/",
    "https://variety.com/2023/film/news/france-tv-distribution-comedy-christmas-carole-1235621507/",
    "https://variety.com/2023/tv/news/max-4k-ultra-hd-priciest-plan-1235622117/",
    "https://variety.com/2023/tv/news/paramount-with-showtime-launch-us-showtime-app-shut-down-1235622045/",
    "https://variety.com/2023/tv/news/algiers-america-music-euphoria-labrinth-1235621631/",
    "https://variety.com/vip/to-fix-streaming-residuals-guilds-cant-give-up-on-data-transparency-1235613593/",
    "https://variety.com/2023/tv/news/the-last-thing-he-told-me-apple-tv-most-watched-1235619651/",
    "https://variety.com/2023/tv/news/max-launch-tv-shows-movies-content-lineup-streaming-1235621458/",
    "https://variety.com/2023/tv/news/la-screenings-panel-latino-us-production-1235621680/",
    "https://variety.com/vip-special-reports/the-state-of-video-streaming-in-2023-a-special-report-1235607613/",
    "https://variety.com/2023/tv/news/belinda-erik-barmack-wild-sheep-angy-skay-1235621525/",
    "https://variety.com/2023/tv/news/cheryl-strayed-tiny-beautiful-things-tv-liz-tigelaar-1235621032/",
    "https://variety.com/2023/tv/news/thomasin-mckenzie-gretel-vella-fremantle-stan-1235621606/",
    "https://variety.com/2023/tv/news/big-brother-the-challenge-usa-premiere-dates-cbs-summer-1235621557/",
    "https://variety.com/2023/tv/news/trump-doc-lev-parnas-from-russia-billy-corben-rakontur-1235619024/",
    "https://variety.com/2023/tv/news/fcc-commissioner-anna-gomez-biden-appointment-1235621536/",
    "https://variety.com/2023/tv/news/crimecon-clue-awards-2023-submission-true-crime-1235619647/"
]


# for link in links:
#     d = find_article_variety(table_name='variety_tv_news',
#                          link=link)
#
#     print(json.dumps(d, indent=4))
#     time.sleep(random.randint(1, 3))