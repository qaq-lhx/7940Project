from unittest.mock import call
from telegram import Update
from telegram.ext import CallbackContext

from handler import GetChatbot

# query=update.callback_query    query_data=传过来的data
def button_callback(query,query_data,update: Update, context: CallbackContext):

    context.bot.send_message(update.callback_query.message.chat.id,query_data)

chatbot = GetChatbot()
Callback = chatbot, button_callback