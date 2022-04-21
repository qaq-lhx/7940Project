import math
from typing import Tuple, Optional, List

from telegram import InlineKeyboardButton


def build_pagination_page_numbers(total: int, page: int, page_limit: int) -> \
        Tuple[Optional[int], List[Optional[int]], Optional[int]]:
    max_page = math.ceil(total / page_limit)
    pagination_page_numbers = [page]
    prev_page = None
    next_page = None
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


def build_pagination_button(callback_data, current_page: int, target_page: Optional[int]) -> InlineKeyboardButton:
    if target_page is None:
        return InlineKeyboardButton('\u2026', callback_data='-1')
    if target_page == current_page:
        return InlineKeyboardButton('<' + str(target_page) + '>', callback_data='-1')
    return InlineKeyboardButton(str(target_page), callback_data=callback_data)
