import json
import re
import time
from for_database import create_connection, check_article_exists_box_oficce, insert_article, close_connection, insert_box_office_article
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

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


def parse_article_box_office(date, url):
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

    else:
        print('Результаты кассовых сборов не найдены.')

    # Преобразование строки даты в объект datetime
    date_obj = datetime.strptime(date, "%B %d, %Y")

    # Преобразование объекта datetime обратно в строку, но уже в формате YYYY-MM-DD
    formatted_date = date_obj.strftime("%Y-%m-%d")

    return {'article_content': article_text, 'article_date': formatted_date, 'article_link': url}

def process_box_oficce():
    links_dict = find_links_for_box_office()

    connection = create_connection()

    # Initialize counters
    counters = {'new_articles': 0, 'duplicate_articles': 0}
    for date, link in links_dict.items():
        try:
            if not check_article_exists_box_oficce(connection, 'box_office_articles', link):
                article_data = parse_article_box_office(url=link, date=date)
                insert_box_office_article(connection, 'box_office_articles', article_data)
                counters['new_articles'] += 1
                # Pause for a random time between requests to avoid being blocked
                time.sleep(random.uniform(1, 3))
            else:
                counters['duplicate_articles'] += 1
        except Exception as e:
            print(f"Error processing link {link}: {e.args}")

    # Close the database connection
    close_connection(connection)

    print(f"Box office: Added {counters['new_articles']} new articles, Found {counters['duplicate_articles']} duplicate articles")


# process_box_oficce()