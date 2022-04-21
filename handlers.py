from handler import text_message_dispatcher, callback_query_dispatcher, start, help, search, button, \
    recommend, default

Handlers = [
    text_message_dispatcher.Handler,
    callback_query_dispatcher.Handler,
    start.Handler,
    help.Handler,
    search.Handler,
    button.Handler,
    recommend.Handler,
    default.Handler,
]
