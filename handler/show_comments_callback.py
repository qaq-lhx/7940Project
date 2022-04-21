import json
from typing import Optional, List, Tuple

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table.callback_data import store, fetch
from db_table.feedback import get_comments
from handler import GetChatbot
from pagination import build_pagination_page_numbers, build_pagination_button
from words import get_some_random_words


def build_comments(comments_id: Optional[int], comments: List[Tuple[int, int, str]], page: int, page_limit: int,
                   update_markup_only: bool, back_to, back_with_data, db):
    if len(comments) < 1:
        if update_markup_only:
            return None, []
        else:
            return get_some_random_words('no_comment'), []
    if comments_id is None:
        comments_id = store(json.dumps(comments), db)
    if back_to is None:
        back_to_object = {}
    else:
        back_to_object = {'back_to': back_to}
    if back_with_data is None:
        back_with_data_object = {}
    else:
        back_with_data_object = {'back_with_data': back_with_data}
    back_object = {**back_to_object, **back_with_data_object}
    total = len(comments)
    need_pagination = total > page_limit
    pagination_buttons = None
    if need_pagination:
        prev_page, pagination_page_numbers, next_page = build_pagination_page_numbers(total, page, page_limit)
        comments_to_show = comments[(page - 1) * page_limit:page * page_limit]
        pagination_buttons = [[build_pagination_button(callback('show_comments_callback', {
            'comments_id': comments_id,
            'page': page_number,
            'page_limit': page_limit,
            **back_object
        }, db), page, page_number) for page_number in pagination_page_numbers]]
        prev_next_buttons = []
        if prev_page is not None:
            prev_next_buttons.append(InlineKeyboardButton('\u1438', callback_data=callback('show_comments_callback', {
                'comments_id': comments_id,
                'page': prev_page,
                'page_limit': page_limit,
                **back_object
            }, db)))
        if next_page is not None:
            prev_next_buttons.append(InlineKeyboardButton('\u1433', callback_data=callback('show_comments_callback', {
                'comments_id': comments_id,
                'page': next_page,
                'page_limit': page_limit,
                **back_object
            }, db)))
        if len(prev_next_buttons) > 1:
            pagination_buttons.append(prev_next_buttons)
        elif len(prev_next_buttons) == 1:
            if prev_page is not None:
                pagination_buttons[0].insert(0, prev_next_buttons[0])
            elif next_page is not None:
                pagination_buttons[0].append(prev_next_buttons[0])
    else:
        comments_to_show = comments
    buttons_to_show = [[InlineKeyboardButton(
        comment[2],
        callback_data=callback('show_comment_details_callback', {
            'feedback_id': comment[0],
            'back_to': 'show_comments_callback',
            'back_with_data': {
                'comments_id': comments_id,
                'page': page,
                'page_limit': page_limit,
                'update_text': True,
                **back_object
            },
        }, db)
    )] for comment in comments_to_show]
    if need_pagination:
        buttons_to_show += pagination_buttons
    if update_markup_only:
        message = None
    else:
        if total > 1:
            message = get_some_random_words('got_some_comments')
        else:
            message = get_some_random_words('got_a_comment')
    return message, buttons_to_show


def show_comments_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    if 'comments_id' in query_data:
        comments_id = query_data['comments_id']
        raw_comments = fetch(comments_id, chatbot().db)
        if raw_comments is None:
            query.edit_message_text(get_some_random_words('session_expired'))
            query.edit_message_reply_markup(None)
            return
        comments = json.loads(raw_comments)
    else:
        comments_id = None
        movie_id = query_data['movie_id']
        comments = get_comments(movie_id, chatbot().db)
    page = query_data['page']
    page_limit = query_data['page_limit']
    update_markup_only = 'update_text' not in query_data or not query_data['update_text']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    message, buttons_to_show = build_comments(
        comments_id,
        comments,
        page,
        page_limit,
        update_markup_only,
        back_to,
        back_with_data,
        chatbot().db
    )
    if back_to is None:
        back_to_button = []
    else:
        back_to_button = [
            [InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))]
        ]
    buttons_to_show += back_to_button
    if len(buttons_to_show) > 0:
        reply_markup = InlineKeyboardMarkup(buttons_to_show)
    else:
        reply_markup = None
    if message is None:
        if reply_markup is not None:
            query.edit_message_reply_markup(reply_markup)
    else:
        if reply_markup is None:
            query.edit_message_text(message)
        else:
            query.edit_message_text(message)
            query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, show_comments_callback
