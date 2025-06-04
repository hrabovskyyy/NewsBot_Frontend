from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

LAST_WEEK = "Останній тиждень"
LAST_MONTH = "Останній місяць"
ANYTIME = "Будь-коли"

def get_search_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Останній тиждень", callback_data="search_news_week")],
        [InlineKeyboardButton(text="Будь-коли", callback_data="search_news_anytime")],
    ]
    return InlineKeyboardMarkup(keyboard)
