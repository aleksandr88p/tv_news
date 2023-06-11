import schedule
import time

from deadline import find_links_deadline, find_article_deadline
from hollywoodreporter import find_links_hollywoodreporter, find_article_hollywoodreporter
from indiwire import find_links_indiwire, find_article_indiwire
from variety import find_links_variety, find_article_variety
from processing import process_links
from box_office import process_box_oficce

def process_articles():
    sources = [
        {
            "name": "Deadline",
            "find_links": find_links_deadline,
            "find_article": find_article_deadline,
        },
        {
            "name": "Hollywood Reporter",
            "find_links": find_links_hollywoodreporter,
            "find_article": find_article_hollywoodreporter,
        },
        {
            "name": "Indiwire",
            "find_links": find_links_indiwire,
            "find_article": find_article_indiwire,
        },
        {
            "name": "Variety",
            "find_links": find_links_variety,
            "find_article": find_article_variety,
        },
    ]

    for source in sources:
        print(f"Processing articles from {source['name']}...")
        links = source['find_links']()
        process_links(source['find_article'], links)


def run_schedule():
    schedule.every(5).hours.do(process_articles)
    schedule.every().day.do(process_box_oficce)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_schedule()