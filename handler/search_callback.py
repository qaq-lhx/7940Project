import json

from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import undo_callback_chat_all
from db_table.callback_data import fetch
from handler import GetChatbot
from handler.search import build_search_results, new_search
from words import get_some_random_words


def show_search_results(query, query_data, update: Update, context: CallbackContext):
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    results_id = query_data['search_results_id']
    page = query_data['page']
    page_limit = query_data['page_limit']
    update_markup_only = 'update_text' not in query_data or not query_data['update_text']
    raw_search_results = fetch(results_id, chatbot().db)
    if raw_search_results is None:
        query.edit_message_text(get_some_random_words('session_expired'))
        query.edit_message_reply_markup(None)
        return
    search_results = json.loads(raw_search_results)
    message, reply_markup = build_search_results(
        results_id,
        search_results,
        page,
        page_limit,
        update_markup_only,
        back_to,
        back_with_data,
        chatbot().db
    )
    if message is None:
        if reply_markup is not None:
            query.edit_message_reply_markup(reply_markup)
    else:
        if reply_markup is None:
            query.edit_message_text(message)
        else:
            query.edit_message_text(message)
            query.edit_message_reply_markup(reply_markup)


def search_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    if 'instance' in query_data and 'text' in query_data and 'data' in query_data:
        data = query_data['data']
        data['text'] = query_data['text']
        undo_callback_chat_all(update.effective_chat, chatbot().db)
    else:
        data = query_data
    actions[data['action']](query, data, update, context)


actions = {
    'new_search': new_search,
    'show_search_results': show_search_results
}
chatbot = GetChatbot()
Callback = chatbot, search_callback
