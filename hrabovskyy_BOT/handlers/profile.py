import json
import os

import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.message_cleaner import delete_previous_message

user_last_message = {}

FAV_FILE = "data/favorites.json"
REACTIONS_FILE = "data/reactions.json"
HISTORY_FILE = "data/history.json"

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id

    await delete_previous_message(update, context, user_last_message)

    fav_count = await count_favourites(update, context)

    reactions_count = 0
    if os.path.exists(REACTIONS_FILE):
        with open(REACTIONS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                reactions_count = len(data.get(user_id, []))
            except Exception:
                pass

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                history = data.get(user_id, [])[-5:]
            except Exception:
                pass

    text = (
        f"👤 <b>Профіль користувача</b>\n\n"
        f"⭐ Улюблених: <b>{fav_count}</b>   📎 Реакцій: <b>{reactions_count}</b>\n\n"
        f"🔍 Останні запити:\n"
    )
    if history:
        for h in reversed(history):
            text += f"• {h}\n"
    else:
        text += "— Немає історії пошуку."

    # 🔘 Інлайн-кнопка назад
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Улюблені", callback_data="view_favourites")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ])

    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    user_last_message[int(user_id)] = msg.message_id

async def count_favourites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from config import API_BASE_URL

    chat_id = update.effective_chat.id
    url = f"{API_BASE_URL}/Favorites/user/{chat_id}"
    data = requests.get(url).json()

    return len(data)


