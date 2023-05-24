import datetime
import json
import random
import time

import requests
from bs4 import BeautifulSoup


def find_article_hollywoodreporter(table_name, link):
    '''
    что то надо сделать с table_name, может записывать в БД прям в этой функции
    :param table_name:
    :param link:
    :return: думаю возвращать имя таблицы, статью, ссылку и дату парсинга( все в словаре)
    '''
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
    # with open('res.html', 'a') as f:
    #     f.write(response.text)

    # with open('res.html', 'r') as f:
    #     page = f.read()

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


links = [
    "https://www.hollywoodreporter.com/tv/tv-news/the-chosen-lionsgate-crowdfunded-jesus-series-1235497604/",
    "https://www.hollywoodreporter.com/tv/tv-news/idris-elba-produce-doc-paid-in-full-the-battle-for-payback-1235496586/",
    "https://www.hollywoodreporter.com/tv/tv-news/american-idol-season-21-winner-iam-tongi-1235497549/",
    "https://www.hollywoodreporter.com/tv/tv-news/ncis-la-series-finale-callen-hanna-kensi-deeks-1235496690/",
    "https://www.hollywoodreporter.com/tv/tv-news/skyshowtime-europe-original-series-cannes-1235497353/",
    "https://www.hollywoodreporter.com/tv/tv-news/james-marsters-buffy-the-vampire-slayer-writers-struggled-spike-character-1235497263/",
    "https://www.hollywoodreporter.com/tv/tv-news/bill-hader-larry-david-barry-ended-season-3-1235497168/",
    "https://www.hollywoodreporter.com/tv/tv-news/tv-writer-david-simon-negative-impact-future-ai-scripts-1235496804/",
    "https://www.hollywoodreporter.com/tv/tv-news/joe-schmo-show-host-ralph-garman-cameo-reboot-1235496549/",
    "https://www.hollywoodreporter.com/tv/tv-news/secret-invasion-cobie-smulders-samuel-l-jackson-1235496602/",
    "https://www.hollywoodreporter.com/tv/tv-news/vanderpump-rules-ariana-madix-scandoval-reunion-season-11-1235496245/",
    "https://www.hollywoodreporter.com/tv/tv-news/entourage-creator-doug-ellin-rant-1235496198/",
    "https://www.hollywoodreporter.com/tv/tv-news/marvelous-mrs-maisel-tony-shalhoub-abe-midge-sexist-1235495536/",
    "https://www.hollywoodreporter.com/tv/tv-news/abc-scheduling-chief-networks-strike-proof-fall-schedule-1235495830/",
    "https://www.hollywoodreporter.com/tv/tv-news/greys-anatomy-finale-cliffhanger-meredith-grey-ellen-pompeo-returns-1235495733/",
    "https://www.hollywoodreporter.com/tv/tv-news/100-years-of-warner-bros-specials-trailer-max-1235495933/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-china-yang-feng-directs-period-action-drama-the-coldest-city-1235497607/",
    "https://www.hollywoodreporter.com/movies/movie-news/christoph-waltz-hitman-comedy-old-guy-sells-1235497582/",
    "https://www.hollywoodreporter.com/movies/movie-news/sean-penn-joins-ukrainian-war-film-1235497572/",
    "https://www.hollywoodreporter.com/movies/movie-news/elemental-aristotle-and-dante-frameline-2023-festival-lineup-1235497501/",
    "https://www.hollywoodreporter.com/movies/movie-news/harrison-ford-busy-as-ever-indiana-jones-star-wars-1235497244/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-marco-bellocchio-interview-1235496714/",
    "https://www.hollywoodreporter.com/movies/movie-news/ken-jeong-prepped-play-publicist-fools-paradise-1235492810/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-alicia-vikander-interview-film-firebrand-1235496979/",
    "https://www.hollywoodreporter.com/movies/movie-news/fast-x-box-office-opening-1235497038/",
    "https://www.hollywoodreporter.com/movies/movie-news/vin-diesel-bringing-back-stars-fast-x-post-credits-1235497293/",
    "https://www.hollywoodreporter.com/movies/movie-news/killers-flower-moon-dicaprio-scorsese-de-niro-cannes-1235497320/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-according-to-rollerskater-thais-coupet-1235497009/",
    "https://www.hollywoodreporter.com/movies/movie-news/white-friar-film-ivan-murphy-cannes-1235496936/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes2023-rising-star-ester-exposito-elite-on-her-childhood-obsession-with-horror-films-1235496963/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-reaction-todd-haynes-movie-may-december-1235496986/",
    "https://www.hollywoodreporter.com/movies/movie-news/cannes-martin-scorsese-killers-of-the-flower-moon-standing-ovation-1235497045/"

]

for link in links:
    d = find_article_hollywoodreporter(table_name='hollywoodreporter_movies', link=link)
    print(json.dumps(d, indent=4))
    time.sleep(random.randint(1, 3))


""""""