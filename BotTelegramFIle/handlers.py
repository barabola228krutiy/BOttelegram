from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from BotTelegramFIle.components import COMPONENTS

# Обробка вибору категорії
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    component_type = query.data
    components = COMPONENTS.get(component_type, [])

    if components:
        await query.message.delete()

        keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]
        message = f"Ось доступні {component_type}:\n"
        for component in components:
            message += f"\n- {component['name']} ($ {component['price']}) - [Посилання]({component['link']})"
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(message, reply_markup=reply_markup, disable_web_page_preview=True, parse_mode="Markdown")
    elif component_type == 'back':
        await query.message.delete()
        await start(update, context)
    else:
        await query.edit_message_text(f"На жаль, немає доступних {component_type}.")
