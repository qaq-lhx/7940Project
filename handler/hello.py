import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


Handler = CommandHandler('hello', hello_command)
