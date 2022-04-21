from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback
from handler import GetChatbot
from handler.search import prepare_data_for_new_search


def starting(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('Search', callback_data=callback(
            'search_callback',
            prepare_data_for_new_search(),
            chatbot().db
        )),
        InlineKeyboardButton('Recommend', callback_data=callback(
            'recommend_callback',
            {'action': 'new_recommend'},
            chatbot().db
        ))
    ]])
    update.message.reply_text(
        'Start to find a movie you like!\n' +
        '\n' +
        'You can follow our guide to Find/Rate the movie!\n' +
        '\n' +
        'Search: Search for a movie with /search.\n' +
        '\n' +
        'Recommend: Get some recommendations with /recommend.',
        reply_markup=reply_markup
    )


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('start', starting)
