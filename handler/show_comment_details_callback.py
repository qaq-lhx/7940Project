from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table.feedback import get_comment_content
from db_table.feedback_reaction import get_reaction, get_likes_count, get_dislikes_count, update_reaction
from handler import GetChatbot
from words import get_some_random_words


def show_comment_details_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    feedback_id = query_data['feedback_id']
    user = update.effective_user
    if 'set_reaction' in query_data:
        if user is not None:
            set_reaction = query_data['set_reaction']
            update_reaction(feedback_id, user.id, set_reaction, chatbot().db)
        del query_data['set_reaction']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    comment = get_comment_content(feedback_id, chatbot().db)
    if user is None:
        user_reaction = None
    else:
        user_reaction = get_reaction(feedback_id, user.id, chatbot().db)
    likes_count = get_likes_count(feedback_id, chatbot().db)
    dislikes_count = get_dislikes_count(feedback_id, chatbot().db)
    if back_to is None:
        back_to_button = []
    else:
        back_to_button = [
            [InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))]
        ]
    likes_count_text = ''
    if likes_count > 0:
        likes_count_text = str(likes_count) + ' '
    dislikes_count_text = ''
    if dislikes_count > 0:
        dislikes_count_text = str(dislikes_count) + ' '
    like_text = 'Like'
    if likes_count > 1:
        like_text = 'Likes'
    dislike_text = 'Dislike'
    if dislikes_count > 1:
        dislike_text = 'Dislikes'
    if user_reaction is True:
        like_text = 'Liked \U0001F44D'
    elif user_reaction is False:
        dislike_text = 'Disliked \U0001F44E'
    like_button_text = likes_count_text + like_text
    dislike_button_text = dislikes_count_text + dislike_text
    like_action_object = {'set_reaction': True}
    dislike_action_object = {'set_reaction': False}
    if user_reaction is True:
        like_action_object = {'set_reaction': None}
    elif user_reaction is False:
        dislike_action_object = {'set_reaction': None}
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(like_button_text, callback_data=callback(
            'show_comment_details_callback',
            {
                **like_action_object,
                **query_data
            },
            chatbot().db
        )),
        InlineKeyboardButton(dislike_button_text, callback_data=callback(
            'show_comment_details_callback',
            {
                **dislike_action_object,
                **query_data
            },
            chatbot().db
        ))
    ]] + back_to_button)
    if comment is None:
        message = get_some_random_words('no_comment')
    else:
        message = get_some_random_words('read_a_comment') + '\n\n' + comment
    query.edit_message_text(message)
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, show_comment_details_callback
