import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from BotTelegramFIle.handlers import handle_selection
from BotTelegramFIle.config import TOKEN


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("CPU", callback_data='CPU')],
        [InlineKeyboardButton("GPU", callback_data='GPU')],
        [InlineKeyboardButton("RAM", callback_data='RAM')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Вітаю! Я допоможу підібрати комплектуючі для ПК. Оберіть категорію:", reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Вітаю! Я допоможу підібрати комплектуючі для ПК. Оберіть категорію:", reply_markup=reply_markup
        )

# Налаштовуємо бота
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Створюємо додаток Telegram
    application = ApplicationBuilder().token(TOKEN).build()

    # Додаємо обробники команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_selection))

    # Запускаємо бота
    application.run_polling()

if __name__ == "__main__":
    main()
