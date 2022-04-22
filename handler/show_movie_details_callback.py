from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from callback_utils import callback
from db_table.feedback import get_comments_count
from db_table.label import get_labels_from_db
from db_table.movie_info import get_movie_in_db
from db_table.rating import get_movie_average_ratings
from handler import GetChatbot
from words import get_some_random_words


def show_movie_details_callback(query: CallbackQuery, query_data, update: Update, context: CallbackContext):
    movie_id = query_data['movie_id']
    if 'back_to' in query_data:
        back_to = query_data['back_to']
    else:
        back_to = None
    if 'back_with_data' in query_data:
        back_with_data = query_data['back_with_data']
    else:
        back_with_data = None
    movie = get_movie_in_db(movie_id, chatbot().db)
    ratings_dict = get_movie_average_ratings([movie_id], chatbot().db)
    tags = ['#' + tag[0].lower() for tag in get_labels_from_db(movie_id, chatbot().db)]
    comments_count = get_comments_count(movie_id, chatbot().db)
    if movie_id in ratings_dict:
        rating = ratings_dict[movie_id]
    else:
        rating = None
    if back_to is None:
        back_to_button = []
    else:
        back_to_button = [
            [InlineKeyboardButton('\u25c0 Go Back', callback_data=callback(back_to, back_with_data, chatbot().db))]
        ]
    if comments_count > 0:
        if comments_count > 1:
            show_comments_button_text = 'See {} Comments'.format(comments_count)
        else:
            show_comments_button_text = 'See 1 Comment'
        show_comments_button = [InlineKeyboardButton(show_comments_button_text, callback_data=callback(
            'show_comments_callback',
            {
                'movie_id': movie_id,
                'page': 1,
                'page_limit': chatbot().env.page_limit,
                'update_text': True,
                'back_to': 'show_movie_details_callback',
                'back_with_data': query_data,
            },
            chatbot().db
        ))]
    else:
        show_comments_button = []
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Rate This Movie', callback_data=callback(
        'evaluate',
        {
            'movie_id': movie_id,
            'movie': movie[1],
            'back_to': 'show_movie_details_callback',
            'back_with_data': query_data,
        },
        chatbot().db
    ))] + show_comments_button] + back_to_button)
    if movie is None:
        message = get_some_random_words('no_movie_details')
    else:
        genres = movie[4].split('|')
        if len(genres) > 1:
            genres_display_name = 'Genres'
        else:
            genres_display_name = 'Genre'
        if len(tags) > 1:
            tags_display_name = 'Tags'
        else:
            tags_display_name = 'Tag'
        if rating is None:
            if len(tags) > 0:
                message = '{} ({})\n\n{}: {}\n\nOverview: {}\n\n{}: {}'.format(
                    movie[1],
                    movie[5],
                    genres_display_name,
                    ', '.join(genres),
                    movie[6],
                    tags_display_name,
                    ' '.join(tags)
                )
            else:
                message = '{} ({})\n\n{}: {}\n\nOverview: {}'.format(
                    movie[1],
                    movie[5],
                    genres_display_name,
                    ', '.join(genres),
                    movie[6],
                )
        else:
            if len(tags) > 0:
                message = '{} ({})\n\nRating: {:0.1f}\n\n{}: {}\n\nOverview: {}\n\n{}: {}'.format(
                    movie[1],
                    movie[5],
                    rating,
                    genres_display_name,
                    ', '.join(genres),
                    movie[6],
                    tags_display_name,
                    ' '.join(tags)
                )
            else:
                message = '{} ({})\n\nRating: {:0.1f}\n\n{}: {}\n\nOverview: {}'.format(
                    movie[1],
                    movie[5],
                    rating,
                    genres_display_name,
                    ', '.join(genres),
                    movie[6],
                )
    query.edit_message_text(message)
    query.edit_message_reply_markup(reply_markup)


chatbot = GetChatbot()
Callback = chatbot, show_movie_details_callback
