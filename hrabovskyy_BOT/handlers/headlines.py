from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from keyboards.categories import get_categories_keyboard
from keyboards.countries import get_countries_keyboard
from keyboards.main import get_back_keyboard
from services.api_client import get_top_headlines
from keyboards.reactions import get_reaction_keyboard

# 1️⃣ Показ категорій
async def handle_category_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = (
        update.callback_query.message.chat.id
        if update.callback_query
        else update.effective_chat.id
    )
    if update.callback_query:
        await update.callback_query.answer()

    print(f"📥 handle_category_choice для chat_id={chat_id}")

    await context.bot.send_message(
        chat_id=chat_id,
        text="📚 Оберіть категорію новин:",
        reply_markup=get_categories_keyboard()
    )

# 2️⃣ Обробка вибору категорії → країни
async def handle_country_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split("_")[1]
    context.user_data["category"] = category

    print(f"✅ handle_country_choice: обрана категорія = {category}")

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=f"🌍 Оберіть країну для категорії \"{category}\":",
        reply_markup=get_countries_keyboard()
    )

# 3️⃣ Отримання і надсилання новин
async def handle_news_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    country = query.data.split("_")[1]
    category = context.user_data.get("category", "general")

    print(f"🌐 handle_news_request: країна = {country}, категорія = {category}")

    articles = await get_top_headlines(country=country, category=category, page_size=5)

    # 🔍 Перевірка, що відповідь має формат списку
    if not articles or not isinstance(articles, list):
        print(f"❌ handle_news_request: отримано не список або порожній результат {articles}")
        await context.bot.send_message(chat_id, "😕 Новини не знайдено.")
        return

    print(f"📰 handle_news_request: знайдено {len(articles)} новин")

    for article in articles:
        if not isinstance(article, dict):
            print(f"⚠️ Пропущено: очікувався dict, а отримав: {type(article)}")
            continue

        title = article.get("title", "❗Без заголовка")
        description = article.get("description", "Без опису")
        url = article.get("url", "")

        print(f"➡️ {title} ({url})")

        text = f"📰 <b>{title}</b>\n\n{description}"
        buttons = get_reaction_keyboard(url)

        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML",
            reply_markup=buttons
        )

    back_button = [["⬅️ Назад"]]
    reply_markup = ReplyKeyboardMarkup(back_button, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=chat_id,
        text="Натисніть кнопку, щоб повернутись назад.",
        reply_markup=get_back_keyboard()
    )
