#need to modify
#查询movie的top n个评论
import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('view_comment', hello_command)