from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import  CallbackContext
from callback_utils import callback, callback_chat
import chatbot
from db_table.label import add_label_to_db

from handler import GetChatbot

def label_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext) -> None:
    """handle user feedback to a movie"""
    command = query_data['command']
    labels = ['funny','exciting','attractive','lovely','ordinary','boring','uncomfortable','terrible']
    movie_id = query_data['movie_id']
    if command == 'normal_label':
        label = query_data['label']
        add_label_to_db(movie_id,label,chatbot().db)
        added_label = query_data['added_label']
        added_label.extend([label])
        button = [[InlineKeyboardButton('add another label',callback_data=callback('label_callback',{
            'command':'add_more_label',
            'movie_id': movie_id,
            'added_label':added_label,
            'label':label,
            'more_label':query_data['more_label']
        }, chatbot().db))],
            [InlineKeyboardButton('write comment',callback_data=callback('label_callback',{
            'command':'write_comment',
            'movie_id': movie_id
        }, chatbot().db))],
            [InlineKeyboardButton('cancel and exit',callback_data=callback('label_callback',{
            'command':'cancel_and_exit',
            'movie_id': movie_id
        }, chatbot().db))]]
        reply_markup = InlineKeyboardMarkup(button)
        query.edit_message_text("""You add a label 【 {} 】 to the movie \nYou can click to add more label to this movie, write comment or exit""".format(label))
        query.edit_message_reply_markup(reply_markup)
    if command == 'more_label':
        result = query_data['more_label']
        #if query_data['added_label']!=None:
            #result = [item for item in result if item not in query_data['added_label']]
        button = [[InlineKeyboardButton(label, callback_data=callback('label_callback', {
            'command':'normal_label',
            'movie_id': movie_id,
            'label':label,
            'more_label':result,
            'added_label':query_data['added_label']
        }, chatbot().db))] for label in result]
        button.extend([[InlineKeyboardButton('custom label',callback_data=callback('label_callback',{
            'command':'custom_label',
                'movie_id': movie_id,
        }, chatbot().db))]])
        button.extend([[InlineKeyboardButton('write comment',callback_data=callback('label_callback',{
            'command':'write_comment',
                'movie_id': movie_id,
        }, chatbot().db))]])
        button.extend([[InlineKeyboardButton('cancel and exit',callback_data=callback('label_callback',{
            'command':'cancel_and_exit',
                'movie_id': movie_id,
        }, chatbot().db))]])
        reply_markup = InlineKeyboardMarkup(button)
        #query.edit_message_text('You can give labels for this movie')
        query.edit_message_reply_markup(reply_markup)
    if command == 'add_more_label':
        added_label = query_data['added_label']
        again_labels = [item for item in labels if item not in added_label]
        again_more_labels = [item for item in query_data['more_label'] if item not in added_label]
        if len(again_labels)!=0:
            button = [[InlineKeyboardButton(label, callback_data=callback('label_callback', {
                'command':'normal_label',
                'movie_id': movie_id,
                'label':label,
                'more_label':query_data['more_label'],
                'added_label':added_label
            }, chatbot().db))] for label in again_labels]
            if len(again_more_labels)!=0:
                button.extend([[InlineKeyboardButton('more labels',callback_data=callback('label_callback',{
                    'command':'more_label',
                    'movie_id': movie_id,
                    'more_label':query_data['more_label'],
                    'added_label':  added_label
                }, chatbot().db))]])
        else:
            if len(again_more_labels)!=0:
                button = [[InlineKeyboardButton(label, callback_data=callback('label_callback', {
                    'command':'normal_label',
                    'movie_id': movie_id,
                    'label':label,
                    'more_label':query_data['more_label'],
                    'added_label':added_label
                }, chatbot().db))] for label in again_more_labels]
        button.extend([[InlineKeyboardButton('custom label',callback_data=callback('label_callback',{
            'command':'custom_label',
            'movie_id': movie_id,
            'more_label':query_data['more_label']
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
        label = query_data['label']
        query.edit_message_text("You add a label 【 {} 】 to the movie".format(label))
        reply_markup = InlineKeyboardMarkup(button)
        context.bot.send_message(query.message.chat_id,text='Please choose a label for this movie:',reply_markup=reply_markup)
    if command == 'custom_label':
        query.edit_message_text('Please give your label to the movie')
        callback_chat(update.effective_chat, 'custom_label_callback',  movie_id, chatbot().db)
    if command == 'write_comment':
        query.edit_message_text('Please type in your comment to the movie')
        callback_chat(update.effective_chat, 'write_comment_callback',  movie_id, chatbot().db)
    if command == 'cancel_and_exit':
        query.edit_message_text('Thanks for your sharing!\nYou can use command \"/search <keyword>\" or simply use command \"/search\" to find another movie.')



chatbot = GetChatbot()
Callback = chatbot, label_callback