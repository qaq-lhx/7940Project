import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CallbackContext

from db_table.callback_data import fetch, store
from db_table.movie_info import get_movie_in_db, search_movie_in_db
from handler import GetChatbot
from handler.search import build_search_results


def show_movie_info(query, query_data):
    movie_id = query_data['selected_id']
    keywords = query_data['search_keywords']
    movie = get_movie_in_db(movie_id, chatbot().db)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('\u1438', callback_data=str(store(json.dumps({
            'action': 'search_again',
            'search_keywords': keywords
        }), chatbot().db)))],
    ])
    if movie is None:
        message = 'Oops! I\'m sorry. I can\'t tell you more about the movie.'
    else:
        message = '{} ({})\n\nGenres: {}\n\nOverview: {}'.format(
            movie[1],
            movie[5],
            ', '.join(movie[4].split('|')),
            movie[6]
        )
    query.edit_message_text(message)
    query.edit_message_reply_markup(reply_markup)
    return 'search_callback'


def search_again(query, query_data):
    keywords = query_data['search_keywords']
    message, reply_markup = build_search_results(keywords, search_movie_in_db(keywords, chatbot().db))
    if reply_markup is None:
        query.edit_message_text(message)
        return
    else:
        query.edit_message_text(message)
        query.edit_message_reply_markup(reply_markup)
        return 'search_callback'


def search_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query_data = json.loads(fetch(int(query.data), chatbot().db))
    return actions[query_data['action']](query, query_data)


actions = {
    'show_movie_info': show_movie_info,
    'search_again': search_again
}
chatbot = GetChatbot()
Handler = chatbot, CallbackQueryHandler(search_callback)
