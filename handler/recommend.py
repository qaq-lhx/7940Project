from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback
from chunks import split_list_into_chunks
from db_table.movie_info import recommend_movie_in_db, get_genres_in_db
from handler import GetChatbot
from words import get_some_random_words


def build_recommend_results(keywords, results, db):
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            '{} ({}), \u2606:{}'.format(result[1], result[2], result[3]),
            callback_data=callback('show_movie_details_callback', {
                'movie_id': result[0],
                'back_to': 'recommend_callback',
                'back_with_data': {
                    'action': 'recommend_again',
                    'recommend_keywords': keywords
                },
            }, db)
        )] for result in results])
    if len(results) < 1:
        return 'I can\'t find any movie for you.', None
    if len(results) > 1:
        message = 'Here are the movies I recommend:'
    else:
        message = 'Here is the movie I recommend:'
    return message, reply_markup


def build_genre_selector(db):
    genres = get_genres_in_db(db)
    return InlineKeyboardMarkup(
        split_list_into_chunks([InlineKeyboardButton(
            genre,
            callback_data=callback('recommend_callback', {
                'action': 'new_recommend',
                'recommend_keywords': genre.split(' ')
            }, db)
        ) for genre in genres], 3)
    )


def new_recommend(query, query_data, update: Update, context: CallbackContext):
    if 'text' in query_data:
        keywords = query_data['text'].split(' ')
    elif 'recommend_keywords' in query_data:
        keywords = query_data['recommend_keywords']
    else:
        if query is None:
            update.message.reply_text(
                get_some_random_words('need_genre'),
                reply_markup=build_genre_selector(chatbot().db)
            )
        else:
            query.edit_message_text(get_some_random_words('need_genre'))
            query.edit_message_reply_markup(build_genre_selector(chatbot().db))
        return
    message, reply_markup = build_recommend_results(
        keywords,
        recommend_movie_in_db(keywords, chatbot().db),
        chatbot().db
    )
    if message is not None:
        if reply_markup is None:
            if query is None:
                update.message.reply_text(message)
            else:
                query.edit_message_text(message)
        else:
            if query is None:
                update.message.reply_text(message, reply_markup=reply_markup)
            else:
                query.edit_message_text(message)
                query.edit_message_reply_markup(reply_markup)


def recommend(update: Update, context: CallbackContext):
    query_data = {'action': 'new_recommend'}
    if len(context.args) < 1:
        update.message.reply_text(get_some_random_words('need_genre'), reply_markup=build_genre_selector(chatbot().db))
    else:
        query_data['recommend_keywords'] = context.args
        new_recommend(None, query_data, update, context)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('recommend', recommend)
