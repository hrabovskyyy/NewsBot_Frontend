from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.main import get_main_menu_keyboard
from services.message_cleaner import delete_previous_message

# 🔗 Підключення підменю
from handlers.headlines import handle_category_choice
from handlers.search import handle_search
from handlers.favorites import handle_favorites_menu
from handlers.profile import handle_profile

user_last_message = {}

async def handle_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    chat_id = update.effective_chat.id

    await delete_previous_message(update, context, user_last_message)

    if text in ["/start", "🔙 Назад"]:
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text="👋 Вітаю!\nОберіть, що ви хочете зробити:",
            reply_markup=get_main_menu_keyboard()
        )
        user_last_message[user_id] = msg.message_id
        return

    if text == "📰 Отримати новини":
        await handle_category_choice(update, context)
        return

    if text == "🔍 Пошук новини":
        await handle_search(update, context)
        return

    if text == "⭐ Улюблені новини":
        await handle_favorites_menu(update, context)
        return

    if text == "👤 Профіль":
        await handle_profile(update, context)
        return

    await update.message.reply_text("❓ Оберіть варіант з меню нижче.")


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    query = update.callback_query
    user_id = query.from_user.id

    # await delete_previous_message(update, context, user_last_message)

    msg = await update.effective_chat.send_message(
        text="👋 Повертаємося в головне меню:",
        reply_markup=get_main_menu_keyboard()
    )
    user_last_message[user_id] = msg.message_id
    await query.answer()
