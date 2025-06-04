import json
import os
from telegram import Update
from telegram.ext import ContextTypes
from services.api_client import add_favorite

REACTIONS_FILE = "data/reactions.json"

def load_reactions():
    if not os.path.exists(REACTIONS_FILE):
        return {}
    with open(REACTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_reactions(data):
    os.makedirs("data", exist_ok=True)
    with open(REACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def handle_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    action = query.data  # like / dislike
    message_text = query.message.text

    reactions = load_reactions()

    reactions.setdefault(user_id, [])
    reactions[user_id].append({
        "reaction": action,
        "text": message_text[:100]
    })

    save_reactions(reactions)

    await query.answer("✅ Дякую за оцінку!")

async def handle_add_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    message_text = query.message.text_html
    callback_data = query.data  # формат: addfav|https://...

    try:
        _, url = callback_data.split("|", 1)
        title = message_text.split("\n")[0].replace("📰", "").replace("🔎", "").replace("⭐", "").strip()

        success = await add_favorite(title, url, str(user_id))

        if success:
            await query.answer("✅ Додано до улюблених!", show_alert=False)
        else:
            await query.answer("⚠️ Не вдалося додати.", show_alert=True)

    except Exception as e:
        await query.answer("❌ Помилка під час додавання.", show_alert=True)
        print(f"[AddFavorite Error] {e}")
