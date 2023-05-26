import time
import random
from for_database import create_connection, check_article_exists, insert_article, close_connection

def process_links(find_article_function, links):
    """
    Обрабатывает список ссылок, используя заданную функцию find_article_function, и сохраняет новые статьи в базе данных.

    Args:
    find_article_function (function): Функция для извлечения данных статьи по ссылке.
    links (dict): Словарь, где ключами являются имена таблиц, а значениями - списки ссылок на статьи.

    """
    # Create a new database connection
    connection = create_connection()
    # Initialize counters
    counters = {table_name: {'new_articles': 0, 'duplicate_articles': 0} for table_name in links.keys()}

    # Iterate over the links
    for table_name, link_list in links.items():
        for link in link_list:
            try:
                # Check if the article already exists in the database
                if not check_article_exists(connection, table_name, link):
                    # If the article does not exist, parse it and insert it into the database
                    article_data = find_article_function(table_name, link)
                    insert_article(connection, table_name, article_data)
                    counters[table_name]['new_articles'] += 1
                else:
                    counters[table_name]['duplicate_articles'] += 1

                # Pause for a random time between requests to avoid being blocked
                time.sleep(random.uniform(1, 5))
            except Exception as e:
                print(f"Error processing link {link} in table {table_name}: {e}")

    # Close the database connection
    close_connection(connection)

    for table_name, count in counters.items():
        print(f"For {table_name}: Added {count['new_articles']} new articles, Found {count['duplicate_articles']} duplicate articles")
