from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


Handler = CommandHandler('help', help_command)
