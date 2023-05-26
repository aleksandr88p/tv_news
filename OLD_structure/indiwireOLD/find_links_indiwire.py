"""
https://www.indiewire.com
IndieWire (Film and TV)

https://www.indiewire.com/t/film/
https://www.indiewire.com/t/film/page/2/


https://www.indiewire.com/t/tv/
https://www.indiewire.com/t/tv/page/2/
"""

import json
import requests
from bs4 import BeautifulSoup

def find_links_indiwire():
    import requests

    cookies = {
        'usprivacy': '1---',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+23+2023+19%3A10%3A10+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0002%3A1%2CC0004%3A0%2CC0001%3A1%2CC0003%3A1&AwaitingReconsent=false',
        'omni_visit_id': 'pmc.1684861701386.3ca978c1-1bcf-4d92-b24c-fbc54285c5c7',
        '_ga_3QZ1BLEPP5': 'GS1.1.1684861701.1.1.1684861810.0.0.0',
        '_ga': 'GA1.1.854944783.1684861701',
        'OneTrustWPCCPAGoogleOptOut': 'true',
    }

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

# d = find_links_indiwire()
# print(json.dumps(d, indent=4))