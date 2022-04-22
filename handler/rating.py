from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from callback_utils import callback
from handler import GetChatbot


def rating(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """give user some button to rate a movie."""
    movie_id = query_data['movie_id']
    movie = query_data['movie']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    if back_to is None:
        back_object = {}
    else:
        if back_with_data is None:
            back_object = {'back_to': back_to}
        else:
            back_object = {'back_to': back_to, 'back_with_data': back_with_data}
    buttons = [[InlineKeyboardButton(str(score), callback_data=callback('rating_callback', {
        'movie_id': movie_id,
        'movie': movie,
        'score': score,
        **back_object
    }, chatbot().db)) for score in range(1, 6)]]
    if back_to is not None:
        buttons.append([
            InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
        ])
    reply_markup = InlineKeyboardMarkup(buttons)
    query.edit_message_text('Please rate for the movie \" {} \"'.format(movie))
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, rating
