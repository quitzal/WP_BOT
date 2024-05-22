from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

def main():
    token = '7005799824:AAHfsjxxny2lybaslr3mAFF4P2-taiDpq_Q'
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('add', add_command))
    dispatcher.add_handler(CommandHandler('search', search_command))
    dispatcher.add_handler(CommandHandler('delete', delete_command))

    # Message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

def help_command(update, context):
    update.message.reply_text('/help - все команды\n/add - добавить окно\n/search - показать все окна\n/delete - удалить окно')

def add_command(update, context):
    update.message.reply_text('Send me the text to add:')
    context.user_data['state'] = 'ADDING'

def search_command(update, context):
    lines = '\n'.join(context.bot_data.get('lines', []))
    update.message.reply_text(lines if lines else 'No lines found.')

def delete_command(update, context):
    lines = context.bot_data.get('lines', [])
    # Create buttons with text from each line
    keyboard = [[line] for line in lines]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Select a line to delete:', reply_markup=reply_markup)
    context.user_data['state'] = 'DELETING'

def handle_message(update, context):
    state = context.user_data.get('state')
    if state == 'ADDING':
        lines = context.bot_data.setdefault('lines', [])
        line_number = len(lines) + 1
        new_line = f"{line_number}. {update.message.text}"
        lines.append(new_line)
        update.message.reply_text('Line added.')
        context.user_data['state'] = None
    elif state == 'DELETING':
        try:
            index = int(update.message.text) - 1  # Adjust index since user sees 1-based index
            lines = context.bot_data.get('lines', [])
            del lines[index]
            update.message.reply_text('Line deleted.')
        except (IndexError, ValueError):
            update.message.reply_text('Invalid selection.')
        context.user_data['state'] = None

if __name__ == '__main__':
    main()