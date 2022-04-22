from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback
from handler import GetChatbot
from handler.search import prepare_data_for_new_search


def build_start_greetings(chat_id):
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton('Search', callback_data=callback(
            'search_callback',
            prepare_data_for_new_search(addons={'back_to': 'undo_callback_chat_callback', 'back_with_data': {
                'chat_id': chat_id,
                'then_call': 'start_callback'
            }}),
            chatbot().db
        )),
        InlineKeyboardButton('Recommend', callback_data=callback(
            'recommend_callback',
            {'action': 'new_recommend', 'back_to': 'start_callback'},
            chatbot().db
        ))
    ]])
    text = 'Start to find a movie you like!\n' + \
           '\n' + \
           'You can follow our guide to Find/Rate the movie!\n' + \
           '\n' + \
           'Search: Search for a movie with /search.\n' + \
           '\n' + \
           'Recommend: Get some recommendations with /recommend.'
    return text, reply_markup


def starting(update: Update, context: CallbackContext) -> None:
    text, reply_markup = build_start_greetings(update.effective_chat.id)
    update.message.reply_text(text, reply_markup=reply_markup)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('start', starting)
