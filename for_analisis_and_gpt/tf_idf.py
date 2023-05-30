import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import datetime


nltk.download('punkt')
nltk.download('stopwords')

conn = mysql.connector.connect(
    host="none",
    user="none",
    password="none",
    database="none"
)



# Имена таблиц
table_names = [
    'deadline_film', 'deadline_tv', 'hollywoodreporter_movies_news',
    'hollywoodreporter_tv_news', 'indiwire_film', 'indiwire_tv',
    'variety_film_news', 'variety_tv_news'
]

dataframes = []

# Calculate the date 7,6,5, etc days ago
some_days_ago = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')

# Извлечение данных из каждой таблицы и добавление их в список датафреймов
for table in table_names:
    sql_query = f"SELECT * FROM {table} WHERE parsing_date >= '{some_days_ago}'"
    df = pd.read_sql(sql_query, con=conn)
    df["source"] = table  # Добавьте столбец источника, чтобы знать, откуда пришла статья
    dataframes.append(df)

# Объединяем все датафреймы в один
all_articles = pd.concat(dataframes, ignore_index=True)

# Удаление стоп-слов из статей
stop_words = set(stopwords.words('english'))
all_articles['article_text'] = all_articles['article_text'].apply(lambda x: ' '.join(
    [word for word in word_tokenize(x) if word.casefold() not in stop_words]
))

# Создание векторного представления статей с использованием TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_articles['article_text'])

# Вычисление косинусного сходства между статьями
similarities = cosine_similarity(X)

# Устанавливаем порог сходства
similarity_threshold = 0.5

# Находим пары статей, которые превышают порог сходства
similar_articles_dict = {}
for i in range(len(similarities)):
    for j in range(i + 1, len(similarities)):
        if similarities[i, j] > similarity_threshold:
            if all_articles.iloc[i]["url"] not in similar_articles_dict:
                similar_articles_dict[all_articles.iloc[i]["url"]] = []
            similar_articles_dict[all_articles.iloc[i]["url"]].append(all_articles.iloc[j]["url"])

# Выводим группы похожих статей
printed_groups = set()
c = 0
for key, val in similar_articles_dict.items():
    group = set(val + [key])

    # Получаем список источников для каждой статьи в группе
    sources = [all_articles.loc[all_articles['url'] == article_url]['source'].values[0] for article_url in group]

    # Если количество уникальных источников в группе меньше какого то числа
    if len(set(sources)) < 3:
        continue

    if str(group) not in printed_groups:
        c += 1
        print(f"Articles group {c}:")

        for article_url in group:
            article = all_articles.loc[all_articles['url'] == article_url]
            # print(f"URL: {article_url}, Название: {article['title'].values[0]}, Источник: {article['source'].values[0]}")
            print(f"URL: {article_url}")
        printed_groups.add(str(group))


