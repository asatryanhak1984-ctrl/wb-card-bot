import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

SYSTEM_TEXT = "Пожалуйста, загрузите фотографии карточки товара."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SYSTEM_TEXT)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Фото получены.\n\n"
        "Что вижу на фото (извлечённые данные):\n"
        "— Анализ изображений будет подключён на следующем шаге.\n\n"
        "Вопрос №1: Категория товара на маркетплейсе (точная)?"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ответ получен.\n"
        "Следующий вопрос будет задан автоматически."
    )

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()

