from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import undo_callback_chat_all
from handler import GetChatbot


def help_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    reply_message = 'Let me see... "{}"? I don\'t quite understand.'.format(query_data['text'])
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    # undo_callback_chat(query_data['instance'], chatbot().db)
    undo_callback_chat_all(update.effective_chat, chatbot().db)


chatbot = GetChatbot()
Callback = chatbot, help_callback
