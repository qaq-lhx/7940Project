import json

from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext

from callbacks import Callbacks
from db_table.callback_data import fetch
from handler import GetChatbot


def dispatch(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    raw_data = fetch(int(query.data), chatbot().db)
    if raw_data is not None:
        query_data = json.loads(fetch(int(query.data), chatbot().db))
        return Callbacks[query_data['call']][1](query, query_data['data'], update, context)


def on_receive_chatbot(c):
    for _, value in Callbacks.items():
        value[0].provide(c)


chatbot = GetChatbot()
chatbot.on_receive = on_receive_chatbot
Handler = chatbot, CallbackQueryHandler(dispatch)
