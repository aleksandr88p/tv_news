import mysql.connector

config = {
    'user': 'none',
    'password': 'none',
    'host': 'none',
    'database': 'none',
    'port': 'none'
}

sources = ['deadline_film', 'deadline_tv', 'hollywoodreporter_movies_news',
           'hollywoodreporter_tv_news','variety_film_news', 'variety_tv_news',
           'indiwire_film','indiwire_tv']

# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor()
#
# for source in sources:
#     create_table_query = f"""
#     CREATE TABLE IF NOT EXISTS {source} (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         url VARCHAR(255) NOT NULL,
#         title VARCHAR(255) NOT NULL,
#         article_text LONGTEXT NOT NULL,
#         parsing_date DATETIME NOT NULL
#     );
#     """
#     cursor.execute(create_table_query)
#
# cnx.commit()
# cursor.close()
# cnx.close()

# try:
#     # Соединение с БД
#     connection = mysql.connector.connect(**config)
#
#     cursor = connection.cursor()
#
#     for table_name in sources:
#         # Запрос на изменение типа данных колонок url и title
#         alter_table_query = f"""
#         ALTER TABLE {table_name}
#         MODIFY COLUMN url TEXT NOT NULL,
#         MODIFY COLUMN title TEXT NOT NULL;
#         """
#         # Выполнение запроса
#         cursor.execute(alter_table_query)
#
#         print(f"Таблица {table_name} успешно обновлена.")
#
#     cursor.close()
#
# except mysql.connector.Error as error:
#     print("Ошибка при обновлении таблицы {}".format(error))
#
# finally:
#     if connection.is_connected():
#         connection.close()
#         print("Соединение с БД закрыто.")


"""

"""
