import mysql.connector
from mysql.connector import Error

config = {
    'user': 'user_for_tv_and_news',
    'password': 'mY@we$omeP@$$w0rd',
    'host': '185.51.121.22',
    'database': 'tv_news',
    'port': '3306'
}
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        print('Connect to mysql successful')
    except Error as e:
        print(f'The error {e} occurred')

    return connection


def close_connection(connection):
    connection.close()


def check_article_exists(connection, table_name, url):
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM {table_name} WHERE url = %s"
    cursor.execute(query, (url,))
    result = cursor.fetchone()
    return result[0] > 0


def insert_article(connection, table_name, article_data):
    cursor = connection.cursor()
    query = f"INSERT INTO {table_name} (url, title, article_text, parsing_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (article_data['link'], article_data['title'], article_data['article'], article_data['date_time']))
    connection.commit()
