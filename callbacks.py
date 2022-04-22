from handler import search_callback, button_callback, help_callback, rating, rating_callback, label_callback, \
    recommend_callback, write_comment_callback, show_movie_details_callback, custom_label_callback, \
    show_comments_callback, show_comment_details_callback, undo_callback_chat_callback, start_callback

Callbacks = {
    'search_callback': search_callback.Callback,
    'button_callback': button_callback.Callback,
    'help_callback': help_callback.Callback,
    'evaluate': rating.Callback,
    'rating_callback': rating_callback.Callback,
    'label_callback': label_callback.Callback,
    'recommend_callback': recommend_callback.Callback,
    'write_comment_callback': write_comment_callback.Callback,
    'custom_label_callback': custom_label_callback.Callback,
    'show_movie_details_callback': show_movie_details_callback.Callback,
    'show_comments_callback': show_comments_callback.Callback,
    'show_comment_details_callback': show_comment_details_callback.Callback,
    'undo_callback_chat_callback': undo_callback_chat_callback.Callback,
    'start_callback': start_callback.Callback,
}

for _, callback in Callbacks.items():
    if len(callback) > 2:
        callback[2].provide(Callbacks)
