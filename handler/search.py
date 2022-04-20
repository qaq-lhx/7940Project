from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback
from db_table.movie_info import search_movie_in_db
from handler import GetChatbot


def build_search_results(keywords, results, db):
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            '{} ({})'.format(result[1], result[2]),
            callback_data=callback('search_callback', {
                'action': 'show_movie_info',
                'selected_id': result[0],
                'search_keywords': keywords
            }, db)
        )] for result in results])
    if len(results) < 1:
        return 'I can\'t find any movie for you.', None
    if len(results) > 1:
        message = 'Here are the movies I found:'
    else:
        message = 'Here is the movie I found:'
    return message, reply_markup


def search_command(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text('Usage: /search <keyword>')
        return
    keywords = context.args
    message, reply_markup = build_search_results(keywords, search_movie_in_db(keywords, chatbot().db), chatbot().db)
    if reply_markup is None:
        update.message.reply_text(message)
        return
    else:
        update.message.reply_text(message, reply_markup=reply_markup)
        return 'search_callback'


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('search', search_command)
