
from handler import search_callback, button_callback, help_callback,rating,rating_callback, recommend_callback


Callbacks = {
    'search_callback': search_callback.Callback,
    'button_callback': button_callback.Callback,
    'help_callback': help_callback.Callback,
    'evaluate':rating.Callback,
    'rating_callback':rating_callback.Callback,
    'recommend_callback': recommend_callback.Callback,

}
