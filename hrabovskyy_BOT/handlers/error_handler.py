import logging
import traceback
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="logs/errors.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
)

async def log_error(update, context: ContextTypes.DEFAULT_TYPE):
    error_text = f"❌ Помилка: {context.error}"
    traceback_text = "".join(traceback.format_exception(None, context.error, context.error.__traceback__))

    print(error_text)
    print(traceback_text)

    logger.error(error_text)
    logger.error(traceback_text)

    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Виникла внутрішня помилка. Адмін уже в курсі."
        )
