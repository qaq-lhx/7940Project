#need to modify
#写评论这个流程中查找movie
import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('search_rating', hello_command)