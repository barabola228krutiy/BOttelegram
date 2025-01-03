import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Дані про комплектуючі
COMPONENTS = {
    "CPU": [
        {"name": "Intel Core i5-12400", "price": 200, "link": "https://hard.rozetka.com.ua/ua/intel-bx8071512400/p331700458/"},
        {"name": "AMD Ryzen 5 5600X", "price": 250, "link": "https://hard.rozetka.com.ua/ua/amd_100_100000065box/p257442296/"}
    ],
    "GPU": [
        {"name": "NVIDIA RTX 3060", "price": 400, "link": "https://hard.rozetka.com.ua/ua/videocards/c80087/21330=geforce-rtx-3060;21349=4241/?gad_source=1&gclid=CjwKCAiA65m7BhAwEiwAAgu4JLnuQ5wyxXpE2rm2eNVtTrle6kZhDUWyqBl8mbpkaraTrUZChgBzgBoCG8cQAvD_BwE"},
        {"name": "AMD RX 6600", "price": 350, "link": "https://hard.rozetka.com.ua/ua/videocards/c80087/21330=rx-6600/"}
    ],
    "RAM": [
        {"name": "16GB DDR4 3200MHz", "price": 80, "link": "https://hard.rozetka.com.ua/ua/memory/c80081/21249=10836;21250=129342/"},
        {"name": "32GB DDR4 3600MHz", "price": 150, "link": "https://hard.rozetka.com.ua/ua/memory/c80081/21249=15807;21250=3600-mgts/"}
    ]
}

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

# Обробка вибору категорії
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    component_type = query.data
    components = COMPONENTS.get(component_type, [])

    if components:
        # Видаляємо попереднє повідомлення
        await query.message.delete()

        keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
        message = f"Ось доступні {component_type}:\n"
        for component in components:
            # Використовуємо Markdown для створення посилання
            message += f"\n- {component['name']} ($ {component['price']}) - [Посилання]({component['link']})"
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(message, reply_markup=reply_markup, disable_web_page_preview=True, parse_mode="Markdown")
    elif component_type == 'back':
        # Видаляємо попереднє повідомлення при натисканні на кнопку "Назад"
        await query.message.delete()
        await start(update, context)  # Викликаємо функцію для повернення на старт
    else:
        await query.edit_message_text(f"На жаль, немає доступних {component_type}.")

# Головна функція
def main():
    application = ApplicationBuilder().token("7282082862:AAFU6b37ullnVbFhbrC2F1VTVJzEcxB7UH8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_selection))

    # Запускаємо бота
    application.run_polling()

if __name__ == "__main__":
    main()

#VozniukDanya