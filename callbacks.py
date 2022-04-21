<<<<<<< HEAD
from handler import search_callback, button_callback, help_callback,rating,rating_callback,label_callback
=======

from handler import search_callback, button_callback, help_callback,rating,rating_callback, recommend_callback
>>>>>>> 6e458f2bc7c7b0dca056a5c77753212e329248e4


Callbacks = {
    'search_callback': search_callback.Callback,
    'button_callback': button_callback.Callback,
    'help_callback': help_callback.Callback,
    'evaluate':rating.Callback,
    'rating_callback':rating_callback.Callback,
<<<<<<< HEAD
    'label_callback':label_callback.Callback,
=======
    'recommend_callback': recommend_callback.Callback,

>>>>>>> 6e458f2bc7c7b0dca056a5c77753212e329248e4
}
