import json
import re
import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime


def find_links_for_box_office():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
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

    response = requests.get('https://editorial.rottentomatoes.com/weekend-box-office/', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    links_dict = {}
    all_items = soup.find_all('div', attrs={'class': 'col-sm-8 newsItem col-full-xs'})
    for item in all_items:
        link = item.find('a')['href']
        date = item.find('p', attrs={'class': 'publication-date'}).text.strip()
        links_dict[date] = link

    return links_dict


def parse_article_box_office(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
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
        url=url, headers=headers,
    )

    soup = BeautifulSoup(response.text, 'lxml')
    article_content = soup.find('div', attrs={"class": "articleContentBody"})
    article_text = ''.join(article_content.stripped_strings)  # просто вся статья

    # Разделяем текст статьи на разделы
    result_separator = 'FULL LIST OF BOX OFFICE RESULTS:'
    result_index = article_text.lower().find(result_separator.lower())

    if result_index != -1:
        # Извлекаем текст до раздела с результатами кассовых сборов
        article_without_results = article_text[:result_index].strip()  # без той таблицы о кассовых сборах

        # Извлекаем текст с результатами кассовых сборов
        results_text = article_text[result_index:].strip()  # просто табличка со сборами
        # # Выводим результаты
        # print('Весь текст статьи:')
        # print(article_text)
        # print('---')
        #
        # print('Текст статьи без результатов кассовых сборов:')
        # print(article_without_results)
        # print('---')
        #
        # print('Текст с результатами кассовых сборов:')
        # print(results_text)
    else:
        print('Результаты кассовых сборов не найдены.')


d = find_links_for_box_office()
for k, v in d.items():
    parse_article_box_office(v)
