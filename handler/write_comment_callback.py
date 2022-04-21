from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import undo_callback_chat_all
from handler import GetChatbot
from db_table import feedback

def write_comment_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    comment = query_data['text']
    movie_id = query_data['data']
    feedback_id = update.message.message_id
    feedback.add_comment(feedback_id,movie_id,comment,chatbot().db)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Thanks for your sharing!\nYou can use command \"/search <keyword>\" or simply use command \"/search\" to find another movie.')
    undo_callback_chat_all(update.effective_chat, chatbot().db)

chatbot = GetChatbot()
Callback = chatbot, write_comment_callback