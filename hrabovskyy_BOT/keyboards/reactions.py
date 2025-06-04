from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_reaction_keyboard(article_url: str):
    if not article_url or not isinstance(article_url, str) or not article_url.startswith("http"):
        article_url = "https://example.com"

    # ✂️ Обрізаємо URL для callback_data
    short_url = article_url[:50]  # максимум 50 символів

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👍", callback_data="like"),
            InlineKeyboardButton("👎", callback_data="dislike"),
            InlineKeyboardButton("🌐 Читати", url=article_url)
        ],
        [
            InlineKeyboardButton("⭐ Додати", callback_data=f"addfav|{short_url}")
        ]
    ])

def get_favorite_action_keyboard(url: str, fav_id: str):
    if not url or not isinstance(url, str) or not url.startswith("http"):
        url = "https://example.com"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 Читати", url=url),
            InlineKeyboardButton("🗑️ Видалити", callback_data=f"deletefav|{fav_id}")
        ]
    ])