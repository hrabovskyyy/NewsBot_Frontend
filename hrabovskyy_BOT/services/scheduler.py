from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
from config import DAILY_NEWS_HOUR
from services.api_client import get_top_headlines
from keyboards.reactions import get_reaction_keyboard

# Список користувачів, які мають отримувати розсилку
subscribed_users = set()

def schedule_daily_news(app):
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

    @scheduler.scheduled_job("cron", hour=DAILY_NEWS_HOUR)
    async def send_daily_news():
        if not subscribed_users:
            print("📭 Немає підписаних користувачів.")
            return

        headlines = await get_top_headlines(country="ua", category="general", page_size=3)

        for user_id in subscribed_users:
            for item in headlines:
                text = f"🗞 <b>{item['title']}</b>\n\n{item.get('description') or 'Без опису'}"
                buttons = get_reaction_keyboard(item['url'])

                try:
                    await app.bot.send_message(
                        chat_id=user_id,
                        text=text,
                        parse_mode="HTML",
                        reply_markup=buttons
                    )
                except Exception as e:
                    print(f"❌ Не вдалося надіслати користувачу {user_id}: {e}")

    scheduler.start()
