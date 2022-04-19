from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    print('production:', chatbot().env.production)
    update.message.reply_text('Helping you helping you.')


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('help', help_command)
