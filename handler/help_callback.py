from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from handler import GetChatbot
from handler.help import give_help


def help_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    give_help(query, query_data, update, context)


chatbot = GetChatbot()
Callback = chatbot, help_callback
