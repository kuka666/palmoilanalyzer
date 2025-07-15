import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_news(news_item):
    date = news_item["date"]
    title = news_item["title"]
    source = news_item["source"]
    link = news_item.get("link", "")

    news_text = f"{title}\nИсточник: {source}\nДата: {date}\nСсылка: {link}"

    prompt = f"""
Ты — ведущий аналитик мирового уровня по рынку Palm Oil.  
Твоя задача — анализировать все доступные новостные ленты, связанные с:
• Palm Oil, сельским хозяйством, погодой, геополитикой, логистикой, торговыми барьерами, законодательными изменениями и макроэкономикой.

🔍 Для анализа строго следуй этим шагам:

1. 📌 Краткая выжимка (Bullet Points):
• Укажи до 5 ключевых фактов, которые реально могут повлиять на цену или логистику Palm Oil.
• Указывай дату и 🔗 ссылку только из новостей, которые я дал ниже.

2. 📊 Анализ влияния на рынок:
• Прогнозируй влияние: рост / падение / нейтрально.
• Учитывай спрос, предложение, климат, геополитику, торговлю и логистику.

3. 💼 Вывод и рекомендации:
• Дай краткий вывод для бизнеса (покупать / ждать / готовиться к перебоям).
• Отметь связи между новостями из разных стран, если они есть.

🎯 Строго используй шаблон:

📌 Новости (кратко):
- [дата] Факт. 🔗 Ссылка
- ...

📊 Аналитика:
- Потенциальное влияние: [рост / падение / нейтрально]
- Причины: ...

💼 Вывод для бизнеса:
...

Вот последние новости:

{news_text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content