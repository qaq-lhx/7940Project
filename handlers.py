from tensorboard import summary
from handler import start,message,help,hello,rating,search_rating,turn_to_rating,add_label,write_comment,next_movie_rating,search_view,summary,view_comment,next_movie_view

Handlers = [
    start.Handler,
    message.Handler,
    help.Handler,
    hello.Handler,
    rating.Handler,
    search_rating.Handler,
    turn_to_rating.Handler,
    add_label.Handler,
    write_comment.Handler,
    next_movie_rating.Handler,
    search_view.Handler,
    summary.Handler,
    view_comment.Handler,
    next_movie_view.Handler

]
