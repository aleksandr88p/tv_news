import json

from tf_idf_two import article_grupped
import openai

# Инициализируем ключ API
openai.api_key = ''

# for group, value in article_grupped.items():
#     print(group)
#     for item in value:
#         print(item[1])
#     print('********')
# Проходим по каждой группе статей
# for group_key, group_articles in article_grupped.items():
#
#     # Выбираем первую статью в группе для генерации обзора
#     article_to_summarize = group_articles[0][1]
#     print(group_key)
#     print(article_to_summarize)
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=article_to_summarize,
#         temperature=0.4,
#         max_tokens=300
#     )
#
#     summary = response.choices[0].text.strip()
#
#     print(article_to_summarize)
#     print(f"\nSummary for {group_key}:\n{summary}")


print(json.dumps(article_grupped, indent=4))