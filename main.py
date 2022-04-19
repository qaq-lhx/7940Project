#!/usr/bin/env python3

import logging

import chatbot
import environment


def init_logging(level=logging.INFO):
    logging.basicConfig(
        format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
        level=level
    )


if __name__ == '__main__':
    init_logging(level=logging.INFO)
    logging.warning('Chatbot is running in the development mode.')
    chatbot.Chatbot(env=environment.Env(production=False)).start_polling()
else:
    init_logging()
    logging.info('Chatbot is running in the production mode.')
    app = chatbot.Chatbot().app
