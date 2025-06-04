from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_countries_keyboard():
    countries = [
        ("🇺🇦 Україна", "news_ua"),
        ("🇺🇸 США", "news_us"),
        ("🇬🇧 Велика Британія", "news_gb"),
        ("🇩🇪 Німеччина", "news_de"),
        ("🇫🇷 Франція", "news_fr")
    ]

    keyboard = [
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in countries
    ]

    return InlineKeyboardMarkup(keyboard)
