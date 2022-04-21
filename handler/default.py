from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext

from handler import GetChatbot
from words import get_some_random_words


def default_reply(update: Update, context: CallbackContext):
    update.message.reply_text(get_some_random_words('default') + '\n\n' + get_some_random_words('start_tip'))


def handle_unrecognized_command(update: Update, context: CallbackContext):
    default_reply(update, context)


chatbot = GetChatbot()
Handler = chatbot, MessageHandler(Filters.command, handle_unrecognized_command)
