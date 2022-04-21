from email import message
import logging

from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackContext
from callback_utils import callback
import chatbot
from db_table.label import get_labels_from_db

from handler import GetChatbot
from db_table import rating

def rating_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """give user some labels to evaluate a movie."""
    labels = ['funny','exciting','attractive','lovely','ordinary','boring','uncomfortable','terrible']
    movie_id = query_data['movie_id']
    movie = query_data['movie']
    score = query_data['score']
    rating.insert_rating_in_db(movie_id,score,chatbot().db)
    result = get_labels_from_db(movie_id,chatbot().db)
    button = [[InlineKeyboardButton(label, callback_data=callback('label_callback', {
            'command':'normal_label',
            'movie_id': movie_id,
            'label':label,
            'more_label':result,
            'added_label': []
        }, chatbot().db))] for label in labels]    
    if len(result) != 0:
        result = [item for item in result if item not in labels]
        if len(result) != 0:
            result = result[:6]
            button.extend([[InlineKeyboardButton('more labels',callback_data=callback('label_callback',{
                'command':'more_label',
                'movie_id': movie_id,
                'more_label':result,
                'added_label': []
            }, chatbot().db))]])    
    button.extend([[InlineKeyboardButton('custom label',callback_data=callback('label_callback',{
        'command':'custom_label',
        'movie_id': movie_id,
        'more_label':result,
        'added_label': []
    }, chatbot().db))]])
    button.extend([[InlineKeyboardButton('write comment',callback_data=callback('label_callback',{
        'command':'write_comment',
        'movie_id': movie_id,
        'label':None
    }, chatbot().db))]])
    button.extend([[InlineKeyboardButton('cancel and exit',callback_data=callback('label_callback',{
        'command':'cancel_and_exit',
        'movie_id': movie_id,
        'label':None
    }, chatbot().db))]])
    reply_markup = InlineKeyboardMarkup(button)
    query.edit_message_text('You give 【 {} 】 score to \"{}\"'.format(score,movie))
    context.bot.send_message(query.message.chat_id,text='You can give labels for this movie',reply_markup=reply_markup)


chatbot = GetChatbot()
Callback = chatbot, rating_callback