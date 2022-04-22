import random


def get_some_random_words(situation: str):
    if situation in Words:
        return random.choice(Words[situation])
    else:
        return random.choice(Words['default'])


Words = {
    'session_expired': [
        'Oops! I\'m sorry. Where were we?',
        'Can you repeat that? My mind was on something else.',
        'Can you repeat all that? I think I\'d better write it down.',
        'Can you repeat what you\'ve said or done? I\'m afraid I didn\'t catch you.',
    ],
    'need_search_keyword': [
        'What do you want to search for?',
    ],
    'found_no_movie': [
        'I can\'t find any movie for you.',
    ],
    'found_a_movie': [
        'Here is the movie I found:',
    ],
    'found_some_movies': [
        'Here are the movies I found:',
    ],
    'no_movie_details': [
        'Oops! I\'m sorry. I can\'t tell you more about the movie.',
    ],
    'no_comment': [
        'No comment. I don\'t know anything.',
    ],
    'got_a_comment': [
        'Here is the comment:',
    ],
    'got_some_comments': [
        'Here are the comments:',
    ],
    'read_a_comment': [
        'The comment says:',
    ],
    'need_genre': [
        'Choose a movie genre that you are interested in:',
    ],
    'need_help_keyword': [
        'What can I do for you?'
    ],
    'recommended_no_movie': [
        'I can\'t recommend any movie to you.',
    ],
    'recommended_a_movie': [
        'Here is the movie I picked to you:',
    ],
    'recommended_some_movies': [
        'Here are the movies I picked to you:',
    ],
    'start_tip': [
        'If you want to ask me how to start, just type /start.',
        'By the way, you can type /start to start.',
    ],
    'default': [
        'Oops! I don\'t know what to say.',
        'I don\'t know what to say, and I cannot think.',
    ],
}
