import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

SYSTEM_TEXT = "Пожалуйста, загрузите фотографии карточки товара."
USER_STATE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SYSTEM_TEXT)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USER_STATE[user_id] = "WAIT_CATEGORY"

    await update.message.reply_text(
        "Фото получены.\n\n"
        "Вопрос №1: Категория товара на маркетплейсе (точная)?"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = (update.message.text or "").strip()

    if USER_STATE.get(user_id) == "WAIT_CATEGORY":
        USER_STATE[user_id] = "DONE"
        await update.message.reply_text(
            f"Категория принята: {text}\n\n"
            "Ок. Следующий вопрос добавляю дальше."
        )
        return

    await update.message.reply_text("Пожалуйста, сначала загрузите фотографии карточки товара.")


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()

