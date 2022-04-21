import logging

from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackContext
from callback_utils import callback

from handler import GetChatbot


def rating(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """give user some button to rate a movie."""
    movie_id = query_data['movie_id']
    movie = query_data['movie']
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(score, callback_data=callback('rating_callback', {
            'movie_id':movie_id,
            'movie': movie,
            'score':score
        }, chatbot().db))] for score in range(1,6)
    ])
    query.edit_message_text('Please rate for the movie \" {} \"'.format(movie))
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, rating