from email import message
import logging

from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackContext
from callback_utils import callback

from handler import GetChatbot
from db_table import rating

def rating_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """give user some button to rate a movie."""
    movie_id = query_data['movie_id']
    movie = query_data['movie']
    score = query_data['score']
    rating.insert_rating_in_db(movie_id,score,chatbot().db)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(score, callback_data=callback('rating_callback', {
            'movie_id':movie_id,
            'movie': movie,
            'score':score
        }, chatbot().db))] for score in range(1,6)
    ])
    query.edit_message_text('You give {} score to \"{}\"'.format(score,movie))
    context.bot.send_message(query.message.chat_id,text='You can give labels for this movie',reply_markup=reply_markup)


chatbot = GetChatbot()
Callback = chatbot, rating_callback