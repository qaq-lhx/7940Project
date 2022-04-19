#need to modify
#查看别人的评论这个流程中查找movie
import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('search_view', hello_command)