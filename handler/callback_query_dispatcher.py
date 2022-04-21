import json

from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext

from callbacks import Callbacks
from db_table.callback_data import fetch
from handler import GetChatbot
from words import get_some_random_words


def dispatch(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data != '':
        callback_data_id = int(query.data)
        if callback_data_id >= 0:
            raw_data = fetch(callback_data_id, chatbot().db)
            if raw_data is not None:
                query_data = json.loads(raw_data)
                Callbacks[query_data['call']][1](query, query_data['data'], update, context)
            else:
                query.edit_message_text(get_some_random_words('session_expired'))
                query.edit_message_reply_markup(None)
    query.answer()


def on_receive_chatbot(c):
    for _, value in Callbacks.items():
        value[0].provide(c)


chatbot = GetChatbot()
chatbot.on_receive = on_receive_chatbot
Handler = chatbot, CallbackQueryHandler(dispatch)
