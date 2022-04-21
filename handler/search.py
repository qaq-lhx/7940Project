import json
import math
from typing import List, Tuple, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from callback_utils import callback, callback_chat
from db_table.callback_data import store
from db_table.movie_info import search_movie_in_db
from db_table.rating import get_movie_average_ratings
from handler import GetChatbot


def search_with_ratings(keywords: List[str], excluded_ids: List[int], limit: int, db) -> \
        List[Tuple[int, str, str, float]]:
    results = search_movie_in_db(keywords, excluded_ids, limit, db)
    ratings = get_movie_average_ratings([result[0] for result in results], db)
    return [result + (ratings[result[0]],) for result in results]


def build_pagination_page_numbers(total: int, page: int, page_limit: int) -> \
        Tuple[Optional[int], List[Optional[int]], Optional[int]]:
    max_page = math.ceil(total / page_limit)
    pagination_page_numbers = [page]
    prev_page = None,
    next_page = None,
    if page > 1:
        prev_page = page - 1
        pagination_page_numbers.insert(0, prev_page)
    if page < max_page:
        next_page = page + 1
        pagination_page_numbers.append(next_page)
    if page == 1 and 3 <= max_page:
        pagination_page_numbers.append(3)
    if page == max_page and max_page - 2 >= 1:
        pagination_page_numbers.insert(0, max_page - 2)
    if pagination_page_numbers[0] > 1:
        if pagination_page_numbers[0] > 2:
            pagination_page_numbers.insert(0, None)
        pagination_page_numbers.insert(0, 1)
    if pagination_page_numbers[-1] < max_page:
        if pagination_page_numbers[-1] < max_page - 1:
            pagination_page_numbers.append(None)
        pagination_page_numbers.append(max_page)
    return prev_page, pagination_page_numbers, next_page


def build_pagination_button(results_id: int, current_page: int, page: Optional[int], page_limit: int, db):
    if page is None:
        return InlineKeyboardButton('\u2026', callback_data='-1')
    if page == current_page:
        return InlineKeyboardButton('<{}>'.format(page), callback_data='-1')
    return InlineKeyboardButton(str(page), callback_data=callback('search_callback', {
        'action': 'show_search_results',
        'search_results_id': results_id,
        'page': page,
        'page_limit': page_limit
    }, db))


def build_search_results(results_id: Optional[int], results: List[Tuple[int, str, str, float]], page: int,
                         page_limit: int, update_markup_only: bool, db):
    if len(results) < 1:
        if update_markup_only:
            return None, None
        else:
            return 'I can\'t find any movie for you.', None
    if results_id is None:
        results_id = store(json.dumps(results), db)
    total = len(results)
    need_pagination = total > page_limit
    pagination_buttons = None
    if need_pagination:
        prev_page, pagination_page_numbers, next_page = build_pagination_page_numbers(total, page, page_limit)
        results_to_show = results[(page - 1) * page_limit:page * page_limit]
        pagination_buttons = [build_pagination_button(results_id, page, page_number, page_limit, db) for page_number in
                              pagination_page_numbers]
        if prev_page is not None:
            pagination_buttons.insert(0, InlineKeyboardButton('\u1438', callback_data=callback('search_callback', {
                'action': 'show_search_results',
                'search_results_id': results_id,
                'page': prev_page,
                'page_limit': page_limit
            }, db)))
        if next_page is not None:
            pagination_buttons.append(InlineKeyboardButton('\u1433', callback_data=callback('search_callback', {
                'action': 'show_search_results',
                'search_results_id': results_id,
                'page': next_page,
                'page_limit': page_limit
            }, db)))
    else:
        results_to_show = results
    buttons_to_show = [[InlineKeyboardButton(
        '{} ({}), \u2606:{:0.1f}'.format(result[1], result[2], result[3]),
        callback_data=callback('search_callback', {
            'action': 'show_movie_info',
            'selected_id': result[0],
            'search_results_id': results_id,
            'page': page,
            'page_limit': page_limit
        }, db)
    )] for result in results_to_show]
    if need_pagination:
        print(pagination_buttons)
        # buttons_to_show.append(pagination_buttons)
        buttons_to_show.append([InlineKeyboardButton('test', callback_data='-1')])
    if update_markup_only:
        message = None
    else:
        if len(results) > 1:
            message = 'Here are the movies I found:'
        else:
            message = 'Here is the movie I found:'
    return message, InlineKeyboardMarkup(buttons_to_show)


def new_search(query, query_data, update: Update, context: CallbackContext):
    if 'text' in query_data:
        keywords = query_data['text'].split(' ')
    else:
        keywords = query_data['search_keywords']
    limit = query_data['search_limit']
    page = query_data['page']
    page_limit = query_data['page_limit']
    message, reply_markup = build_search_results(
        None,
        search_with_ratings(keywords, [], limit, chatbot().db),
        page,
        page_limit,
        False,
        chatbot().db
    )
    if message is not None:
        if reply_markup is None:
            update.message.reply_text(message)
        else:
            update.message.reply_text(message, reply_markup=reply_markup)


def search_command(update: Update, context: CallbackContext):
    query_data = {
        'action': 'new_search',
        'search_limit': chatbot().env.search_limit,
        'page': 1,
        'page_limit': chatbot().env.page_limit
    }
    if len(context.args) < 1:
        update.message.reply_text('What do you want to search for?')
        callback_chat(update.effective_chat, 'search_callback', query_data, chatbot().db)
    else:
        query_data['search_keywords'] = context.args
        new_search(None, query_data, update, context)


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('search', search_command)
