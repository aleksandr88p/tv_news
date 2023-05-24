import datetime
import json
import random
import time

import requests
from bs4 import BeautifulSoup


def find_article_deadline(table_name, link):
    '''
    что то надо сделать с table_name, может записывать в БД прям в этой функции
    :param table_name:
    :param link:
    :return: думаю возвращать имя таблицы, статью, ссылку и дату парсинга( все в словаре)
    '''

    cookies = {
        'usprivacy': '1---',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+23+2023+20%3A30%3A35+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fdeadline.com%2Fv%2Ffilm%2F&groups=C0002%3A1%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1',
        'omni_visit_id': 'deadline.1684866635602.b620e58b-8193-4b3e-9ed1-09dae31c6f35',
        '_ga_487Y5JM3D8': 'GS1.1.1684866635.1.0.1684866635.0.0.0',
        '_ga': 'GA1.1.662090496.1684866636',
    }

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

    response = requests.get(
        url=link,
        # cookies=cookies,
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


links = [
    "https://deadline.com/2023/05/the-night-agent-gabriel-basso-clint-eastwoods-juror-2-warner-bros-1235376215/",
    "https://deadline.com/gallery/2023-cannes-film-festival-premieres-photos/",
    "https://deadline.com/2023/05/asteroid-city-review-wes-anderson-cannes-1235375328/",
    "https://deadline.com/2023/05/teenage-mutant-ninja-turtles-mutant-mayhem-release-date-pushed-up-1235377184/",
    "https://deadline.com/gallery/asteroid-city-cannes-red-carpet-photos-premiere/",
    "https://deadline.com/2023/05/doc-alliance-awards-features-and-shorts-nominee-announcement-1235377144/",
    "https://deadline.com/2023/05/royce-gracie-ufc-movie-in-works-from-christian-gudegast-tucker-tooley-1235377101/",
    "https://deadline.com/2023/05/sag-aftra-cameo-for-business-deal-1235377077/",
    "https://deadline.com/2023/05/uta-promotes-65-across-20-departments-1235377017/",
    "https://deadline.com/video/banel-et-adama-cannes-news-interviews-ramata-toulaye-sy/",
    "https://deadline.com/2023/05/strike-joaquin-phoenix-rooney-mara-movie-island-pawel-pawlikowski-wga-1235376891/",
    "https://deadline.com/2023/05/lily-rose-depp-the-idol-todd-haynes-may-december-cannes-breaking-baz-1235376824/",
    "https://deadline.com/2023/05/mtv-2023-video-music-awards-date-venue-1235377244/",
    "https://deadline.com/2023/05/mgm-names-josh-mcivor-as-global-general-manager-1235377204/",
    "https://deadline.com/2023/05/nigel-lythgoe-pair-launch-pad-dance-icons-on-first-non-scripted-development-slate-for-mark-kimsey-roger-birnbaums-electromagnetic-productions-1235377089/",
    "https://deadline.com/2023/05/sag-aftra-cameo-for-business-deal-1235377077/",
    "https://deadline.com/2023/05/showtime-research-exec-kim-lemon-departs-mtv-paramount-evp-laurel-weir-1235377027/",
    "https://deadline.com/2023/05/uta-promotes-65-across-20-departments-1235377017/",
    "https://deadline.com/2023/05/comcast-launches-now-tv-streaming-bundle-channels-peacock-1235376996/",
    "https://deadline.com/2023/05/chicken-soup-for-the-soul-reward-viewers-avod-fast-outlets-streaming-prizes-1235376862/",
    "https://deadline.com/2023/05/bungalow-media-and-entertainment-names-christie-mcconnell-svp-development-1235376280/",
    "https://deadline.com/2023/05/hollywood-gun-violence-report-norman-lear-center-1235376350/",
    "https://deadline.com/2023/05/religion-of-sports-names-pietro-moro-coo-cfo-expands-production-division-1235375735/",
    "https://deadline.com/gallery/tv-renewals-2023-photo-gallery/"
]

for link in links:
    d = find_article_deadline(1, link)
    print(json.dumps(d, indent=4))
    time.sleep(random.randint(1, 3))
