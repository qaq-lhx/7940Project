from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback_chat
from handler import GetChatbot


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('What can I do for you?')
    callback_chat(update.effective_chat, 'help_callback', None, chatbot().db)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('help', help_command)
