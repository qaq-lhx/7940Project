from telegram import Update, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from callback_utils import undo_callback_chat_all, callback
from db_table import feedback
from handler import GetChatbot


def write_comment_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    comment = query_data['text']
    movie_id = query_data['data']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    feedback.add_comment(movie_id, comment, chatbot().db)
    if back_to is not None:
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
        ]])
    else:
        reply_markup = None
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Thanks for your sharing!\nYou can use command \"/search <keyword>\" or simply use command \"/search\" to find another movie.',
        reply_markup=reply_markup
    )
    undo_callback_chat_all(update.effective_chat, chatbot().db)


chatbot = GetChatbot()
Callback = chatbot, write_comment_callback
