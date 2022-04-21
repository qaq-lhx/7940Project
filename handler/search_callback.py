import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table.callback_data import fetch
from db_table.movie_info import get_movie_in_db
from handler import GetChatbot
from handler.search import build_search_results, new_search


def show_movie_info(query, query_data, update: Update, context: CallbackContext):
    movie_id = query_data['selected_id']
    results_id = query_data['search_results_id']
    page = query_data['page']
    page_limit = query_data['page_limit']
    movie = get_movie_in_db(movie_id, chatbot().db)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('\u1438', callback_data=callback('search_callback', {
            'action': 'show_search_results',
            'search_results_id': results_id,
            'page': page,
            'page_limit': page_limit,
            'update_text': True
        }, chatbot().db)),
         # click to evaluate a movie
         InlineKeyboardButton('evaluate', callback_data=callback(
             'evaluate',
             {'movie_id': movie_id, 'movie': movie[1]},
             chatbot().db
         )),
         # click to view comment of a movie
         InlineKeyboardButton('comment', callback_data=callback(
             'view',
             {'movie_id': movie_id},
             chatbot().db
         ))],
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


def show_search_results(query, query_data, update: Update, context: CallbackContext):
    results_id = query_data['search_results_id']
    page = query_data['page']
    page_limit = query_data['page_limit']
    update_markup_only = 'update_text' not in query_data or not query_data['update_text']
    raw_search_results = fetch(results_id, chatbot().db)
    if raw_search_results is None:
        return query.edit_message_text('Oops! I\'m sorry. I can\'t let you proceed.')
    search_results = json.loads(raw_search_results)
    message, reply_markup = build_search_results(
        results_id,
        search_results,
        page,
        page_limit,
        update_markup_only,
        chatbot().db
    )
    if message is None:
        if reply_markup is not None:
            query.edit_message_reply_markup(reply_markup)
    else:
        if reply_markup is None:
            query.edit_message_text(message)
        else:
            query.edit_message_text(message)
            query.edit_message_reply_markup(reply_markup)


def search_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    if 'instance' in query_data and 'text' in query_data and 'data' in query_data:
        data = query_data['data']
        data['instance'] = query_data['instance']
        data['text'] = query_data['text']
    else:
        data = query_data
    actions[data['action']](query, data, update, context)


actions = {
    'new_search': new_search,
    'show_movie_info': show_movie_info,
    'show_search_results': show_search_results
}
chatbot = GetChatbot()
Callback = chatbot, search_callback
