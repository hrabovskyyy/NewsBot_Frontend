from datetime import datetime, timedelta
import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import API_BASE_URL

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from keyboards.main import SEARCH_NEWS

    user_data = context.user_data

    # Початок діалогу
    if update.message and update.message.text == SEARCH_NEWS:
        await update.effective_chat.send_message(
            "🔍 <b>Що шукаємо?</b>\n"
            "Опиши новину, яку треба знайти 👇",
            parse_mode="HTML"
        )
        return "SEARCHING_NEWS"
    elif not user_data.get("search_text"):
        user_data["search_text"] = update.message.text

        from keyboards.search_keyboard import get_search_keyboard
        await update.effective_chat.send_message(
            "⏳ <b>За який період шукати новину?</b>",
            reply_markup=get_search_keyboard(),
            parse_mode="HTML"
        )
        return "SEARCHING_NEWS"
    elif update.callback_query.data:
        callback_data = update.callback_query.data
        period = callback_data.split("_")[2]
        url = f"{API_BASE_URL}/News/search"

        await update.effective_chat.send_message("Шукаю новини...")

        # НОВИНИ ЗА ОСТАННІЙ ТИЖДЕНЬ
        if period == "week":
            url = f"{API_BASE_URL}/News/search"

            to = datetime.today().strftime('%Y-%m-%d')
            from_param = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

            params = {
                "q": user_data.get("search_text"),
                "from": from_param,
                "to": to,
            }

            data = requests.get(url, params=params).json()

            articles = data.get("articles")
            if not articles:
                await update.effective_chat.send_message("Не знайшов новин за цим запитом 🫤")
                return ConversationHandler.END

            await send_all_articles(update, data.get("articles")[:5])

            from handlers.main_menu import back_to_main_menu
            await back_to_main_menu(update, context)
            return ConversationHandler.END

        # ЗА ВЕСЬ ЧАС
        if period == "anytime":
            to = datetime.today().strftime('%Y-%m-%d')
            from_param = datetime.strptime("2025-05-11", "%Y-%m-%d")

            params = {
                "q": user_data.get("search_text"),
                "from": from_param,
                "to": to,
            }

            data = requests.get(url, params=params).json()

            articles = data.get("articles")
            if not articles:
                await update.effective_chat.send_message("Не знайшов новин за цим запитом 🫤")
                return ConversationHandler.END

            await send_all_articles(update, data.get("articles")[:5])

            from handlers.main_menu import back_to_main_menu
            await back_to_main_menu(update, context)
            return ConversationHandler.END

        await update.callback_query.answer()
        return ConversationHandler.END
    else:
        ConversationHandler.END

async def send_all_articles(update: Update, response):
    # Ітеруємо по статтях
    for article in response:
        title = article.get("title", "Без заголовка")
        author = article.get("author", "Невідомий автор")
        source = article.get("source", {}).get("name", "Невідоме джерело")
        published_at = article.get("publishedAt", "Невідома дата")
        url = article.get("url", "Без URL")

        await update.effective_chat.send_message(
            f"📰 <b>{title}</b>\n\n"
            f"✍️ <b>Автор:</b> {author}\n"
            f"🏛️ <b>Джерело:</b> {source}\n"
            f"📅 <b>Дата публікації:</b> {published_at}\n"
            f"🔗 <a href='{url}'>Читати повну новину</a>",
            parse_mode="HTML"
        )