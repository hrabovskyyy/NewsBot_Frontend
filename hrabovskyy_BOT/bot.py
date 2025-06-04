from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    filters, ConversationHandler,
)
from config import BOT_TOKEN
from handlers.headlines import (
    handle_category_choice,
    handle_country_choice,
    handle_news_request
)
from handlers.main_menu import handle_start_menu, back_to_main_menu
from handlers.search import handle_search
from handlers.favorites import handle_favorites_menu, handle_delete_favorite
from handlers.reactions import handle_reaction, handle_add_favorite
from handlers.profile import handle_profile
from handlers.error_handler import log_error
from services.scheduler import schedule_daily_news


async def unknown_message(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Я працюю тільки через кнопки. Оберіть опцію з меню.")


async def on_startup(app):
    schedule_daily_news(app)


async def handle_text_message(update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if "пошук" in text:
        await handle_search(update, context)
    elif "улюблен" in text:
        await handle_favorites_menu(update, context)
    elif "профіль" in text:
        await handle_profile(update, context)
    elif text == "📰 Отримати новини":
        await handle_category_choice(update, context)
    else:
        await handle_start_menu(update, context)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    app.add_handler(CommandHandler("start", handle_start_menu))

    from keyboards.main import SEARCH_NEWS, BACK
    from handlers.search import handle_search
    search_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex(f"^{SEARCH_NEWS}$"), handle_search)],
        states={
            "SEARCHING_NEWS": [
                MessageHandler(filters.TEXT, handle_search),
                CallbackQueryHandler(handle_search, pattern="^search_news_"),
            ]
        },
        fallbacks=[
            MessageHandler(filters.TEXT & filters.Regex(f"^{BACK}$") , handle_start_menu),
            CallbackQueryHandler(back_to_main_menu, pattern=f"END"),
        ]
    )

    app.add_handler(search_conv)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    app.add_handler(CallbackQueryHandler(handle_category_choice, pattern="^category_menu$"))
    app.add_handler(CallbackQueryHandler(handle_country_choice, pattern="^category_"))
    app.add_handler(CallbackQueryHandler(handle_news_request, pattern="^news_"))

    app.add_handler(CallbackQueryHandler(handle_favorites_menu, pattern="^view_favourites$"))
    app.add_handler(CallbackQueryHandler(handle_delete_favorite, pattern="^deletefav\\|"))
    app.add_handler(CallbackQueryHandler(handle_add_favorite, pattern="^addfav\\|"))
    app.add_handler(CallbackQueryHandler(handle_reaction, pattern="^(like|dislike)$"))
    app.add_handler(CallbackQueryHandler(back_to_main_menu, pattern="^back_to_menu$"))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_message))

    app.add_error_handler(log_error)

    print("🤖 Бот запущено...")
    app.run_polling()


if __name__ == "__main__":
    main()