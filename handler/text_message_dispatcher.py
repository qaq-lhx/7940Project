import json

from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext

from callbacks import Callbacks
from db_table.callback_data import fetch_chat
from handler import GetChatbot
from handler.default import default_reply


def handle_text_message(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat is not None:
        instance, raw_data = fetch_chat(chat.id, chatbot().db)
        if instance is not None and raw_data is not None:
            query_data = json.loads(raw_data)
            data = {
                'instance': instance,
                'text': update.message.text,
                'data': query_data['data']
            }
            Callbacks[query_data['call']][1](update.callback_query, data, update, context)
            return
    default_reply(update, context)


chatbot = GetChatbot()
Handler = chatbot, MessageHandler(Filters.text & (~Filters.command), handle_text_message)
