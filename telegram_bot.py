# telegram_bot.py
from aiogram import Bot, Dispatcher
import asyncio
import os
from aiogram.client.default import DefaultBotProperties

# Замените своими токеном и ID
TELEGRAM_BOT_TOKEN = "8050272536:AAEJqivZgMqcDRIhUe-yQRXoGIDXEIIFKmA"
TELEGRAM_CHAT_IDS = ["445277169", "1248306679"]

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

loop = asyncio.get_event_loop()


async def send_telegram_message(chat_id: str, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"❌ Failed to send to {chat_id}: {e}")


def send_news_to_telegram(news: dict, analysis: str):
    text = (
        f"🆕 <b>Новая новость MPOB:</b>\n"
        f"<b>{news['title']}</b>\n"
        f"🗓 {news['date']} | 📍 {news['source']}\n"
        f"🔗 {news.get('link', '')}\n\n"
        f"<b>📊 Анализ:</b>\n{analysis}"
    )
    for chat_id in TELEGRAM_CHAT_IDS:
        loop.run_until_complete(send_telegram_message(chat_id, text))
