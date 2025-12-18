import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

SYSTEM_TEXT = "Пожалуйста, загрузите фотографии карточки товара."

# Хранилище по пользователям
USER_DATA = {}

QUESTIONS = [
    ("category", "WAIT_CATEGORY", "Вопрос №1: Категория товара на маркетплейсе (точная)?"),
    ("brand", "WAIT_BRAND", "Вопрос №2: Бренд (как на упаковке/в карточке)? Если нет — напишите: без бренда."),
    ("form", "WAIT_FORM", "Вопрос №3: Форма/вид товара (капсулы/порошок/крем/масло/набор и т.д.)?"),
    ("dosage", "WAIT_DOSAGE", "Вопрос №4: Дозировка/объём/кол-во (например: 1320 мг, 60 капсул)?"),
    ("audience", "WAIT_AUDIENCE", "Вопрос №5: Для кого (взрослые/дети/универсально)?"),
    ("country", "WAIT_COUNTRY", "Вопрос №6: Страна производства?"),
    ("notes", "WAIT_NOTES", "Вопрос №7: Важные особенности (что обязательно указать)? Если нет — напишите: нет."),
]

STEP_ORDER = {step: i for i, (_, step, _) in enumerate(QUESTIONS)}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(SYSTEM_TEXT)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # старт анкеты заново при новых фото
    USER_DATA[user_id] = {"step": "WAIT_CATEGORY", "answers": {}}

    await update.message.reply_text(
        "Фото получены.\n\n"
        + QUESTIONS[0][2]
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = (update.message.text or "").strip()

    if user_id not in USER_DATA:
        await update.message.reply_text("Пожалуйста, сначала загрузите фотографии карточки товара.")
        return

    step = USER_DATA[user_id]["step"]
    answers = USER_DATA[user_id]["answers"]

    idx = STEP_ORDER.get(step)
    if idx is None:
        await update.message.reply_text("Пожалуйста, сначала загрузите фотографии карточки товара.")
        return

    key, _, _ = QUESTIONS[idx]
    answers[key] = text

    next_idx = idx + 1
    if next_idx < len(QUESTIONS):
        _, next_step, next_q = QUESTIONS[next_idx]
        USER_DATA[user_id]["step"] = next_step
        await update.message.reply_text(next_q)
        return

    USER_DATA[user_id]["step"] = "DONE"

    result = (
        "✅ Данные собраны.\n\n"
        f"Категория: {answers.get('category')}\n"
        f"Бренд: {answers.get('brand')}\n"
        f"Форма: {answers.get('form')}\n"
        f"Дозировка/объём: {answers.get('dosage')}\n"
        f"Для кого: {answers.get('audience')}\n"
        f"Страна: {answers.get('country')}\n"
        f"Особенности: {answers.get('notes')}\n"
    )
    await update.message.reply_text(result)


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN не найден в переменных окружения")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()
