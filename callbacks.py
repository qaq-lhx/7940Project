from handler import search_callback, button_callback, help_callback,rating,rating_callback,label_callback


Callbacks = {
    'search_callback': search_callback.Callback,
    'button_callback': button_callback.Callback,
    'help_callback': help_callback.Callback,
    'evaluate':rating.Callback,
    'rating_callback':rating_callback.Callback,
    'label_callback':label_callback.Callback,
}
