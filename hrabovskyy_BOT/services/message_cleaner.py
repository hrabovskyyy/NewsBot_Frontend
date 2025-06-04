from telegram import Update
from telegram.ext import ContextTypes

async def delete_previous_message(update: Update, context: ContextTypes.DEFAULT_TYPE, user_last_message: dict):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        if user_id in user_last_message:
            msg_id = user_last_message[user_id]
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception as e:
        print(f"⚠️ Неможливо видалити повідомлення: {e}")
