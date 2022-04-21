from handler import search_callback, button_callback, help_callback, rating, rating_callback, label_callback, \
    recommend_callback, write_comment_callback, costum_label_callback, show_movie_details_callback

Callbacks = {
    'search_callback': search_callback.Callback,
    'button_callback': button_callback.Callback,
    'help_callback': help_callback.Callback,
    'evaluate': rating.Callback,
    'rating_callback': rating_callback.Callback,
    'label_callback': label_callback.Callback,
    'recommend_callback': recommend_callback.Callback,
    'write_comment_callback': write_comment_callback.Callback,
    'costum_label_callback': costum_label_callback.Callback,
    'show_movie_details_callback': show_movie_details_callback.Callback,
}
