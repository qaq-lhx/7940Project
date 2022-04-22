from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table import rating
from db_table.label import get_labels_from_db
from handler import GetChatbot


def rating_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """give user some labels to evaluate a movie."""
    labels = ['funny', 'exciting', 'attractive', 'lovely', 'ordinary', 'boring', 'uncomfortable', 'terrible']
    movie_id = query_data['movie_id']
    movie = query_data['movie']
    score = query_data['score']
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
    has_insert_this_time = False
    if 'inserted' not in query_data or query_data['inserted'] is not True:
        rating.insert_rating_in_db(movie_id, score, chatbot().db)
        has_insert_this_time = True
        query_data['inserted'] = True
    result = get_labels_from_db(movie_id, chatbot().db)
    result = [item[0] for item in result]
    button = [[InlineKeyboardButton(label, callback_data=callback('label_callback', {
        'command': 'normal_label',
        'movie_id': movie_id,
        'label': label,
        'more_label': result,
        'added_label': [],
        **back_object
    }, chatbot().db))] for label in labels]
    if len(result) != 0:
        result = [item for item in result if item not in labels]
        if len(result) != 0:
            result = result[:6]
            button.extend([[InlineKeyboardButton('more labels', callback_data=callback('label_callback', {
                'command': 'more_label',
                'movie_id': movie_id,
                'more_label': result,
                'added_label': [],
                'back_to': 'rating_callback',
                'back_with_data': query_data
            }, chatbot().db))]])
    button.extend([[InlineKeyboardButton('custom label', callback_data=callback('label_callback', {
        'command': 'custom_label',
        'movie_id': movie_id,
        'more_label': result,
        'added_label': [],
        'back_to': 'rating_callback',
        'back_with_data': query_data
    }, chatbot().db))]])
    button.extend([[InlineKeyboardButton('write comment', callback_data=callback('label_callback', {
        'command': 'write_comment',
        'movie_id': movie_id,
        'label': None,
        'back_to': 'rating_callback',
        'back_with_data': query_data
    }, chatbot().db))]])
    button.extend([[InlineKeyboardButton('cancel and exit', callback_data=callback('label_callback', {
        'command': 'cancel_and_exit',
        'movie_id': movie_id,
        'label': None,
        'back_to': 'rating_callback',
        'back_with_data': query_data
    }, chatbot().db))]])
    if back_to is not None:
        button.append([
            InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
        ])
    reply_markup = InlineKeyboardMarkup(button)
    if has_insert_this_time:
        query.edit_message_text('You give 【 {} 】 score to \"{}\"'.format(score, movie))
        context.bot.send_message(query.message.chat_id, text='You can give labels for this movie',
                                 reply_markup=reply_markup)
    else:
        query.edit_message_text('You can give labels for this movie')
        query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, rating_callback
