import json
import re
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

def connect_to_database(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def fetch_articles_from_tables(conn, table_names, days_ago):
    dataframes = []
    some_days_ago = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    for table in table_names:
        sql_query = f"SELECT * FROM {table} WHERE parsing_date >= '{some_days_ago}'"
        df = pd.read_sql(sql_query, con=conn)
        df["source"] = table
        dataframes.append(df)
    return dataframes

def preprocess_articles(articles_df):
    stop_words = set(stopwords.words('english'))
    articles_df['article_text'] = articles_df['article_text'].apply(lambda x: ' '.join(
        [word for word in word_tokenize(x) if word.casefold() not in stop_words]
    ))
    vectorizer = TfidfVectorizer()
    article_vectors = vectorizer.fit_transform(articles_df['article_text'])
    return article_vectors

# def preprocess_articles(articles_df):
#     stop_words = set(stopwords.words('english'))
#
#     articles_df['article_text'] = articles_df['article_text'].apply(lambda x: ' '.join(
#         [word for word in word_tokenize(x) if word.casefold() not in stop_words]
#     ))
#
#     # Remove all non-alphanumeric characters using regex
#     articles_df['article_text'] = articles_df['article_text'].apply(lambda x: re.sub(r'\W+', ' ', x))
#
#     # Convert text to lower case
#     articles_df['article_text'] = articles_df['article_text'].str.lower()
#
#     vectorizer = TfidfVectorizer()
#     article_vectors = vectorizer.fit_transform(articles_df['article_text'])
#     return article_vectors
def find_similar_articles(article_vectors, threshold):
    similarities = cosine_similarity(article_vectors)
    similar_articles_dict = {}
    for i in range(len(similarities)):
        for j in range(i + 1, len(similarities)):
            if similarities[i, j] > threshold:
                if all_articles.iloc[i]["url"] not in similar_articles_dict:
                    similar_articles_dict[all_articles.iloc[i]["url"]] = []
                similar_articles_dict[all_articles.iloc[i]["url"]].append(all_articles.iloc[j]["url"])
    return similar_articles_dict

def print_article_groups(similar_articles_dict, all_articles):
    printed_groups = set()
    c = 0
    for key, val in similar_articles_dict.items():
        group = set(val + [key])
        sources = [all_articles.loc[all_articles['url'] == article_url]['source'].values[0] for article_url in group]
        if len(set(sources)) < 3:
            continue
        if str(group) not in printed_groups:
            c += 1
            print(f"Articles group {c}:")
            for article_url in group:
                article = all_articles.loc[all_articles['url'] == article_url]
                print(f"URL: {article_url}")
            printed_groups.add(str(group))

def create_article_groups_dict(similar_articles_dict, all_articles):
    article_groups_dict = {}
    c = 0
    for key, val in similar_articles_dict.items():
        group = set(val + [key])
        sources = [all_articles.loc[all_articles['url'] == article_url]['source'].values[0] for article_url in group]
        if len(set(sources)) < 3:
            continue
        c += 1
        group_key = f"Articles group {c}"
        article_groups_dict[group_key] = [(article_url, all_articles.loc[all_articles['url'] == article_url]['article_text'].values[0]) for article_url in group]
    return article_groups_dict


# conn = connect_to_database("none", "none", "none", "none")


table_names = ['deadline_film', 'deadline_tv', 'hollywoodreporter_movies_news',
               'hollywoodreporter_tv_news', 'indiwire_film', 'indiwire_tv',
               'variety_film_news', 'variety_tv_news']

dataframes = fetch_articles_from_tables(conn, table_names, 2)
all_articles = pd.concat(dataframes, ignore_index=True)

article_vectors = preprocess_articles(all_articles)
similar_articles_dict = find_similar_articles(article_vectors, 0.5)
article_grupped = create_article_groups_dict(similar_articles_dict, all_articles)

# print(json.dumps(article_grupped, indent=4))