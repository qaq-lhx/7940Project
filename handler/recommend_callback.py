from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback, undo_callback_chat_all
from db_table.movie_info import get_movie_in_db, get_movie_AVGrating_in_db, recommend_movie_in_db
from handler import GetChatbot
from handler.recommend import build_recommend_results, new_recommend


def show_movie_info(query, query_data, update: Update, context: CallbackContext):
    movie_id = query_data['selected_id']
    keywords = query_data['recommend_keywords']
    movie = get_movie_in_db(movie_id, chatbot().db)
    rating = get_movie_AVGrating_in_db(movie_id, chatbot().db)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('\u1438', callback_data=callback('recommend_callback', {
            'action': 'recommend_again',
            'recommend_keywords': keywords
        }, chatbot().db)),
         # click to evaluate a movie
         InlineKeyboardButton('evaluate', callback_data=callback('evaluate', {'movie_id': movie_id}, chatbot().db)),
         # click to view comment of a movie
         InlineKeyboardButton('comment', callback_data=callback('view', {'movie_id': movie_id}, chatbot().db))],
    ])
    if movie is None:
        message = 'Oops! I\'m sorry. I can\'t tell you more about the movie.'
    else:
        message = '{} ({})\n\nGenres: {}\n\nRating: {}\n\nOverview: {}'.format(
            movie[1],
            movie[5],
            ', '.join(movie[4].split('|')),
            rating[1],
            movie[6]
        )
    query.edit_message_text(message)
    query.edit_message_reply_markup(reply_markup)
    return 'recommend_callback'


def recommend_again(query, query_data, update: Update, context: CallbackContext):
    keywords = query_data['recommend_keywords']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    message, reply_markup = build_recommend_results(keywords, recommend_movie_in_db(keywords, chatbot().db), back_to,
                                                    back_with_data, chatbot().db)
    if reply_markup is None:
        query.edit_message_text(message)
        return
    else:
        query.edit_message_text(message)
        query.edit_message_reply_markup(reply_markup)
        return 'recommend_callback'


def recommend_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    if 'instance' in query_data and 'text' in query_data and 'data' in query_data:
        data = query_data['data']
        data['text'] = query_data['text']
        undo_callback_chat_all(update.effective_chat, chatbot().db)
    else:
        data = query_data
    actions[data['action']](query, data, update, context)


actions = {
    'new_recommend': new_recommend,
    'show_movie_info': show_movie_info,
    'recommend_again': recommend_again,
}
chatbot = GetChatbot()
Callback = chatbot, recommend_callback
