from cgitb import text
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackContext
from callback_utils import callback, callback_chat,undo_callback_chat_all
import chatbot
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext
from db_table.label import add_label_to_db

from handler import GetChatbot


def custom_label_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    custom_label = query_data['text']
    movie_id = query_data['data']
    add_label_to_db(movie_id,custom_label,chatbot().db)
    button = [[InlineKeyboardButton('Yes', callback_data=callback('label_callback',{
        'command':'write_comment',
        'movie_id': movie_id
    },chatbot().db))],[InlineKeyboardButton('No', callback_data=callback('label_callback',{
        'command':'cancel_and_exit',
        'movie_id': movie_id
    },chatbot().db))]]
    reply_markup = InlineKeyboardMarkup(button)
    context.bot.send_message(chat_id=update.effective_chat.id,text='You custom label is submitted! \nDo you want to write comment for is movie?',reply_markup=reply_markup)
    undo_callback_chat_all(update.effective_chat, chatbot().db)

chatbot = GetChatbot()
Callback = chatbot, custom_label_callback