from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_categories_keyboard():
    categories = [
        ("📰 Загальні", "category_general"),
        ("⚙️ Технології", "category_technology"),
        ("💼 Бізнес", "category_business"),
        ("🏥 Здоровʼя", "category_health"),
        ("🏀 Спорт", "category_sports"),
        ("🎭 Розваги", "category_entertainment"),
        ("🌍 Наука", "category_science")
    ]

    keyboard = [
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in categories
    ]

    return InlineKeyboardMarkup(keyboard)
