#need to modify
#查询movie的整体评价，average rating, label...
import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('summary', hello_command)