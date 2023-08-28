import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram import KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from model_handler import get_headers, query
from database_handler import Database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)


url_tinkoff = 'https://api-inference.huggingface.co/models/tinkoff-ai/ruDialoGPT-medium'
url_main = "https://api-inference.huggingface.co/models/SasnayaLetovka/tinkoff-zhientaev-model"

BOT_TOKEN = get_from_env('BOT_TOKEN')
HF_TOKEN = get_from_env('HUGGING_FACE_TOKEN')
API_URL = url_main


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    remove_context_button = [[KeyboardButton('Стереть контекст')]]
    keyboard = ReplyKeyboardMarkup(remove_context_button, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hello, i am gpt-like chat bot ',
                                   reply_markup=keyboard)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_text == 'Стереть контекст':
        db.delete_context(user_id)
        answer = 'Контекст удален'
    else:
        headers = get_headers(HF_TOKEN)

        message_id = update.message.message_id

        answer = query(input_text=user_text,
                       API_URL=API_URL,
                       headers=headers,
                       db=db,
                       user_id=user_id)
        if answer == '':
            answer = 'Не знаю, что ответить'
        db.add_context(user_id, message_id, user_text, answer)
        db.get_context(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    db = Database()
    db.connect()

    application.run_polling()

    db.close()
