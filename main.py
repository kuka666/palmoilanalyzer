import time
from mpob import get_latest_news, is_new_news, load_last_news, save_last_news
from analyzer import analyze_news
from datetime import datetime
from telegram_bot import send_news_to_telegram


def check_and_analyze():
    print(f"\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — Проверка новостей")
    latest_news_list = get_latest_news()
    if not latest_news_list:
        print("⚠️ Новости не найдены")
        return

    saved_news = load_last_news()
    updated = False

    for news in reversed(latest_news_list):  # сначала старые, чтобы не пропустить
        if is_new_news(news, saved_news):
            print(
                f"🆕 Новая новость: {news['date']} — {news['title']} [{news['source']}]"
            )
            print(f"🔗 {news.get('link')}")
            result = analyze_news(news)
            print("\n📊 Анализ:")
            print(result)
            send_news_to_telegram(news, result)
            saved_news.append(news)
            if len(saved_news) > 10:
                saved_news.pop(0)
            updated = True

    if updated:
        save_last_news(saved_news)
    else:
        print("Нет новых новостей.")


if __name__ == "__main__":
    while True:
        check_and_analyze()
        print("⏳ Ожидание 30 минут...")
        time.sleep(1800)
