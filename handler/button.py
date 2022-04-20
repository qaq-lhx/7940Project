from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from callback_utils import callback

from handler import GetChatbot


def button(update: Update, context: CallbackContext):
    label = {
    'help':'/help',
    'hello':'/hello 1',
    'hi':'/hello 2'
    }   
    keyboard = [[InlineKeyboardButton(text=i,callback_data=callback('button_callback',label[i],chatbot().db))] for i in label]
    update.message.reply_text('Choose a button!',
        reply_markup = InlineKeyboardMarkup(keyboard))

chatbot = GetChatbot()
Handler = chatbot, CommandHandler('button', button)