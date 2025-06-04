from telegram import Update
from telegram.ext import ContextTypes
from services.api_client import get_favorites_by_user, delete_favorite
from keyboards.reactions import get_favorite_action_keyboard
from services.message_cleaner import delete_previous_message
from keyboards.main import get_back_keyboard

user_last_message = {}

async def handle_favorites_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    telegram_id = str(user_id)

    await delete_previous_message(update, context, user_last_message)
    favorites = await get_favorites_by_user(telegram_id)

    if not favorites:
        msg = await update.effective_chat.send_message("😕 У вас ще немає улюблених новин.", reply_markup=get_back_keyboard())
        user_last_message[user_id] = msg.message_id
        return

    for item in favorites:
        text = f"⭐ <b>{item['title']}</b>"
        buttons = get_favorite_action_keyboard(item['url'], item['id'])

        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="HTML",
            reply_markup=buttons
        )

    msg = await context.bot.send_message(chat_id, "✅ Ось ваші улюблені новини.", reply_markup=get_back_keyboard())
    user_last_message[user_id] = msg.message_id


async def handle_delete_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data  # format: deletefav|<id>

    try:
        _, fav_id = data.split("|", 1)
        success = await delete_favorite(fav_id)

        if success:
            await query.answer("✅ Видалено з улюблених", show_alert=False)
            await query.message.delete()
        else:
            await query.answer("⚠️ Не вдалося видалити", show_alert=True)

    except Exception as e:
        await query.answer("❌ Помилка при видаленні", show_alert=True)
        print(f"[Delete Favorite Error] {e}")
