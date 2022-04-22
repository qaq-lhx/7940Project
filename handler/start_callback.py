from telegram import Update
from telegram.ext import CallbackContext

from handler import GetChatbot
from handler.start import build_start_greetings


def start_callback(query, query_data, update: Update, context: CallbackContext):
    text, reply_markup = build_start_greetings(update.effective_chat.id)
    query.edit_message_text(text)
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, start_callback
