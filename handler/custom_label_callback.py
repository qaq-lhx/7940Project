from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback, undo_callback_chat_all
from db_table.label import add_label_to_db
from handler import GetChatbot


def custom_label_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    custom_label = query_data['text']
    movie_id = query_data['data']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    has_insert_this_time = False
    if 'inserted' not in query_data or query_data['inserted'] is not True:
        add_label_to_db(movie_id, custom_label, chatbot().db)
        has_insert_this_time = True
        query_data['inserted'] = True
    button = [[InlineKeyboardButton('Yes', callback_data=callback('label_callback', {
        'command': 'write_comment',
        'movie_id': movie_id,
        'back_to': 'custom_label_callback',
        'back_with_data': query_data
    }, chatbot().db)), InlineKeyboardButton('No', callback_data=callback('label_callback', {
        'command': 'cancel_and_exit',
        'movie_id': movie_id,
        'back_to': 'custom_label_callback',
        'back_with_data': query_data
    }, chatbot().db))]]
    if back_to is not None:
        button.append([
            InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
        ])
    reply_markup = InlineKeyboardMarkup(button)
    if has_insert_this_time:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='You custom label is submitted! \nDo you want to write comment for is movie?',
                                 reply_markup=reply_markup)
    else:
        query.edit_message_text('Do you want to write comment for is movie?')
        query.edit_message_reply_markup(reply_markup)

    undo_callback_chat_all(update.effective_chat, chatbot().db)


chatbot = GetChatbot()
Callback = chatbot, custom_label_callback
