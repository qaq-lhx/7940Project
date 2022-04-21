from handler import text_message_dispatcher, callback_query_dispatcher, start, help, add_label, search, button, \
    recommend

Handlers = [
    text_message_dispatcher.Handler,
    callback_query_dispatcher.Handler,
    start.Handler,
    help.Handler,
    add_label.Handler,
    search.Handler,
    button.Handler,
    recommend.Handler,
]
