import json

from tf_idf_two import article_grupped
import openai

openai.api_key = ''


# Начальное сообщение для генерации обзора summarize following text in three paraghraps
prompt = "summarize following text in three paraghraps:\n"
# prompt = "Сделайте крутой веселый обзор статей и напиши на русском я пришлю тебе несколько статей и разделю их так \n******\n"
# for group_key, group_articles in article_grupped.items():
#     print(f"\nОбзоры для {group_key}:")
#
#     for article in group_articles:
#         article_text = article[1]
#         prompt_with_article = prompt + article_text
#
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=prompt_with_article,
#             temperature=0.4,
#             max_tokens=150
#         )
#
#         summary = response.choices[0].text.strip()
#         print(article[0])
#         print(summary)

for group_key, group_articles in article_grupped.items():
    print(f"\nОбзоры для {group_key}:")

    articles_text = "\n".join([article[1] for article in group_articles])

    prompt_with_articles = prompt + articles_text

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_with_articles,
        temperature=0.4,
        max_tokens=500
    )

    # summary = response.choices[0].text.strip()
    # summary = response.choices[0]['text']
    summary = response['choices'][0]['text']
    print(summary)