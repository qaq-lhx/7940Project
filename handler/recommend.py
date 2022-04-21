from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback
from db_table.movie_info import recommend_movie_in_db

from handler import GetChatbot

def build_recommend_results(keywords, results, db):
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            '{} ({}), \u2606:{}'.format(result[1], result[2], result[3]),
            callback_data=callback('recommend_callback', {
                'action': 'show_movie_info',
                'selected_id': result[0],
                'recommend_keywords': keywords
            }, db)
        )] for result in results])
    if len(results) < 1:
        return 'I can\'t find any movie for you.', None
    if len(results) > 1:
        message = 'Here are the movies I recommend:'
    else:
        message = 'Here is the movie I recommend:'
    return message, reply_markup


def recommend(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text('Usage: /recommend <keyword>')
        return
    keywords = context.args
    message, reply_markup = build_recommend_results(keywords, recommend_movie_in_db(keywords, chatbot().db), chatbot().db)
    if reply_markup is None:
        update.message.reply_text(message)
        return
    else:
        update.message.reply_text(message, reply_markup=reply_markup)
        return 'recommend_callback'


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('recommend', recommend)
