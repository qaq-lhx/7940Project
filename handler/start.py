#need to modify
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback

from handler import GetChatbot


def starting(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Start to find a movie you like!\nYou can follow our guide to Find/Rate the movie\nSeacrhing movie:/seacrh <keyword>\nRecommend movie:/recommend <genres>')

chatbot = GetChatbot()
Handler = chatbot, CommandHandler('start', starting)