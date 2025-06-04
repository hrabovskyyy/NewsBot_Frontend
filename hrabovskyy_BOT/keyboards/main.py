from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

HEADLINE_NEWS = "📰 Отримати новини"
SEARCH_NEWS = "🔍 Пошук новини"
FAV_NEWS = "⭐ Улюблені новини"
PROFILE_MENU = "👤 Профіль"
BACK = "🔙 Назад"

def get_main_menu_keyboard():
    keyboard = [
        [HEADLINE_NEWS, SEARCH_NEWS],
        [FAV_NEWS, PROFILE_MENU],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard():
    return ReplyKeyboardMarkup(
        [[BACK]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Повернутись назад"
    )
