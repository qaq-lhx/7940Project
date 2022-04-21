from handler import message, callback_query_dispatcher, start, help, hello, search_rating, turn_to_rating, \
    add_label, write_comment, next_movie_rating, search_view, view_comment, next_movie_view, summary, search, button, recommend

Handlers = [
    message.Handler,
    callback_query_dispatcher.Handler,
    start.Handler,
    help.Handler,
    hello.Handler,
    search_rating.Handler,
    turn_to_rating.Handler,
    add_label.Handler,
    write_comment.Handler,
    next_movie_rating.Handler,
    search_view.Handler,
    summary.Handler,
    view_comment.Handler,
    next_movie_view.Handler,
    search.Handler,
    button.Handler,
    recommend.Handler,
]
