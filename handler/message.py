import logging

from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext

from handler import GetChatbot


def echo(update: Update, context: CallbackContext):
    reply_message = update.message.text.upper()
    logging.info('Update: ' + str(update))
    logging.info('context: ' + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


chatbot = GetChatbot()
Handler = chatbot, MessageHandler(Filters.text & (~Filters.command), echo)
