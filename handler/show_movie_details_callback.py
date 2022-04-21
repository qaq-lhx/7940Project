from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table.movie_info import get_movie_in_db
from db_table.rating import get_movie_average_ratings
from handler import GetChatbot


def show_movie_details_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    movie_id = query_data['movie_id']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    movie = get_movie_in_db(movie_id, chatbot().db)
    ratings_dict = get_movie_average_ratings([movie_id], chatbot().db)
    if movie_id in ratings_dict:
        rating = ratings_dict[movie_id]
    else:
        rating = None
    if back_to is None:
        back_to_button = []
    else:
        back_to_button = [InlineKeyboardButton('\u1438', callback_data=callback(back_to, back_with_data, chatbot().db))]
    reply_markup = InlineKeyboardMarkup([
        back_to_button + [
            # Click to evaluate the movie
            InlineKeyboardButton('evaluate', callback_data=callback(
                'evaluate',
                {'movie_id': movie_id, 'movie': movie[1]},
                chatbot().db
            )),
            # Click to view comments of the movie
            InlineKeyboardButton('comment', callback_data=callback(
                'view',
                {'movie_id': movie_id},
                chatbot().db
            ))
        ],
    ])
    if movie is None:
        message = 'Oops! I\'m sorry. I can\'t tell you more about the movie.'
    else:
        if rating is None:
            message = '{} ({})\n\nGenres: {}\n\nOverview: {}'.format(
                movie[1],
                movie[5],
                ', '.join(movie[4].split('|')),
                movie[6]
            )
        else:
            message = '{} ({})\n\nRating: {:0.1f}\n\nGenres: {}\n\nOverview: {}'.format(
                movie[1],
                movie[5],
                rating,
                ', '.join(movie[4].split('|')),
                movie[6]
            )
    query.edit_message_text(message)
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, show_movie_details_callback
