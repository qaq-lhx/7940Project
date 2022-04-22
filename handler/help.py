from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback_chat, undo_callback_chat_all
from handler import GetChatbot
from words import get_some_random_words

HelpMessages = {
    'start': '/start - Show a start menu.\n\nUsage: /start',
    'search': '/search - Search for a movie.\n\nUsage: /search [<keyword>...]',
    'recommend': '/recommend - Get some recommendations.\n\nUsage: /recommend [<keyword>...]',
    'help': '/help - Ask for help.\n\nUsage: /help [<keyword>...]'
}


def give_help(query, query_data, update: Update, context: CallbackContext):
    if 'help_keywords' in query_data:
        text = ' '.join(query_data['help_keywords'])
    elif 'text' in query_data:
        undo_callback_chat_all(update.effective_chat, chatbot().db)
        text = query_data['text']
    else:
        text = None
    if text is not None:
        possible_command = text.lstrip('/').lower()
        if possible_command in HelpMessages:
            reply_message = HelpMessages[possible_command]
        else:
            reply_message = 'Let me see... "' + text + '"... Well... I don\'t quite understand.'
        message = update.message
        chat = update.effective_chat
        if message is not None:
            message.reply_text(reply_message)
        elif chat is not None:
            context.bot.send_message(chat.id, reply_message)


def help_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text(get_some_random_words('need_help_keyword'))
        callback_chat(update.effective_chat, 'help_callback', None, chatbot().db)
    else:
        give_help(None, {'help_keywords': context.args}, update, context)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('help', help_command)
