import json
from typing import List, Tuple, Optional, Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback, callback_chat
from db_table.callback_data import store
from db_table.movie_info import search_movie_in_db
from db_table.rating import get_movie_average_ratings
from handler import GetChatbot
from pagination import build_pagination_page_numbers, build_pagination_button
from words import get_some_random_words


def search_with_ratings(keywords: List[str], excluded_ids: List[int], limit: int, db) -> \
        List[Tuple[int, str, str, float]]:
    results = search_movie_in_db(keywords, excluded_ids, limit, db)
    if len(results) < 1:
        return []
    ratings = get_movie_average_ratings([result[0] for result in results], db)
    return [result + (ratings[result[0]],) for result in results]


def build_search_results(results_id: Optional[int], results: List[Tuple[int, str, str, float]], page: int,
                         page_limit: int, update_markup_only: bool, back_to: Optional[str], back_with_data, db):
    if len(results) < 1:
        if update_markup_only:
            return None, None
        else:
            if back_to is None:
                return get_some_random_words('found_no_movie'), None
            else:
                return get_some_random_words('found_no_movie'), InlineKeyboardMarkup([[
                    InlineKeyboardButton('\u25c0 Go Back',
                                         callback_data=callback(back_to, back_with_data, chatbot().db))
                ]])
    if results_id is None:
        results_id = store(json.dumps(results), db)
    total = len(results)
    need_pagination = total > page_limit
    pagination_buttons = None
    if need_pagination:
        prev_page, pagination_page_numbers, next_page = build_pagination_page_numbers(total, page, page_limit)
        results_to_show = results[(page - 1) * page_limit:page * page_limit]
        pagination_buttons = [[build_pagination_button(callback('search_callback', {
            'action': 'show_search_results',
            'search_results_id': results_id,
            'page': page_number,
            'page_limit': page_limit
        }, db), page, page_number) for page_number in pagination_page_numbers]]
        prev_next_buttons = []
        if prev_page is not None:
            prev_next_buttons.append(InlineKeyboardButton('\u1438', callback_data=callback('search_callback', {
                'action': 'show_search_results',
                'search_results_id': results_id,
                'page': prev_page,
                'page_limit': page_limit
            }, db)))
        if next_page is not None:
            prev_next_buttons.append(InlineKeyboardButton('\u1433', callback_data=callback('search_callback', {
                'action': 'show_search_results',
                'search_results_id': results_id,
                'page': next_page,
                'page_limit': page_limit
            }, db)))
        if len(prev_next_buttons) > 1:
            pagination_buttons.append(prev_next_buttons)
        elif len(prev_next_buttons) == 1:
            if prev_page is not None:
                pagination_buttons[0].insert(0, prev_next_buttons[0])
            elif next_page is not None:
                pagination_buttons[0].append(prev_next_buttons[0])
    else:
        results_to_show = results
    buttons_to_show = [[InlineKeyboardButton(
        '{} ({}), \u2606:{:0.1f}'.format(result[1], result[2], result[3]),
        callback_data=callback('show_movie_details_callback', {
            'movie_id': result[0],
            'back_to': 'search_callback',
            'back_with_data': {
                'action': 'show_search_results',
                'search_results_id': results_id,
                'page': page,
                'page_limit': page_limit,
                'update_text': True,
                'back_to': back_to,
                'back_with_data': back_with_data
            },
        }, db)
    )] for result in results_to_show]
    if need_pagination:
        buttons_to_show += pagination_buttons
    if back_to is not None:
        buttons_to_show.append([
            InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
        ])
    if update_markup_only:
        message = None
    else:
        if total > 1:
            message = get_some_random_words('found_some_movies')
        else:
            message = get_some_random_words('found_a_movie')
    return message, InlineKeyboardMarkup(buttons_to_show)


def prepare_data_for_new_search(addons: Optional[Dict] = None):
    if addons is None:
        addons = {}
    return {
        'action': 'new_search',
        'search_limit': chatbot().env.search_limit,
        'page': 1,
        'page_limit': chatbot().env.page_limit,
        **addons
    }


def new_search(query, query_data, update: Update, context: CallbackContext):
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    if 'text' in query_data:
        keywords = query_data['text'].split(' ')
    elif 'search_keywords' in query_data:
        keywords = query_data['search_keywords']
    else:
        if back_to is None:
            reply_markup = None
        else:
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))
            ]])
        if query is None:
            update.message.reply_text(get_some_random_words('need_search_keyword'), reply_markup=reply_markup)
        else:
            query.edit_message_text(get_some_random_words('need_search_keyword'))
            if reply_markup is not None:
                query.edit_message_reply_markup(reply_markup)
        callback_chat(update.effective_chat, 'search_callback', query_data, chatbot().db)
        return
    limit = query_data['search_limit']
    page = query_data['page']
    page_limit = query_data['page_limit']
    message, reply_markup = build_search_results(
        None,
        search_with_ratings(keywords, [], limit, chatbot().db),
        page,
        page_limit,
        False,
        back_to,
        back_with_data,
        chatbot().db
    )
    if message is not None:
        if reply_markup is None:
            if query is None:
                update.message.reply_text(message)
            else:
                query.edit_message_text(message)
        else:
            if query is None:
                update.message.reply_text(message, reply_markup=reply_markup)
            else:
                query.edit_message_text(message)
                query.edit_message_reply_markup(reply_markup)


def search_command(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text(get_some_random_words('need_search_keyword'))
        callback_chat(update.effective_chat, 'search_callback', prepare_data_for_new_search(), chatbot().db)
    else:
        new_search(None, prepare_data_for_new_search(addons={'search_keywords': context.args}), update, context)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('search', search_command)
