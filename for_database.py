import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

config = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'database': db_name,
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

def check_article_exists_box_oficce(connection, table_name, url):
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM {table_name} WHERE article_link = %s"
    cursor.execute(query, (url,))
    result = cursor.fetchone()
    return result[0] > 0

def insert_article(connection, table_name, article_data):
    cursor = connection.cursor()
    query = f"INSERT INTO {table_name} (url, title, article_text, parsing_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (article_data['link'], article_data['title'], article_data['article'], article_data['date_time']))
    connection.commit()

# def insert_box_office_article(connection, table_name, article_data):
#     cursor = connection.cursor()
#     query = f"INSERT INTO {table_name} (article_date, article_link, article_content) VALUES (%s, %s, %s)"
#     cursor.execute(query, (article_data['article_date'], article_data['article_link'], article_data['article_content']))
#     connection.commit()

def insert_box_office_article(connection, table_name, article_data):
    cursor = connection.cursor()
    query = f"INSERT INTO {table_name} (article_date, article_link, article_content) VALUES (%s, %s, %s)"
    cursor.execute(query, (article_data['article_date'], article_data['article_link'], article_data['article_content']))
    connection.commit()
