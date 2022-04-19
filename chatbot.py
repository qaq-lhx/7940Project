#!/usr/bin/env python3

import logging
import queue

import flask
import telegram
import telegram.ext

import environment
import handlers
import webhook


class Chatbot:
    def __init__(self, env=None):
        if env is None:
            env = environment.Env()
        self.env = env
        self.bot = telegram.Bot(token=env.telegram_access_token)
        if env.production:
            self.dispatcher = telegram.ext.Dispatcher(bot=self.bot, update_queue=queue.Queue())
            self.app = flask.Flask(__name__)
        else:
            self.updater = telegram.ext.Updater(bot=self.bot)
            self.dispatcher = self.updater.dispatcher
        for handler in handlers.Handlers:
            self.dispatcher.add_handler(handler)
        if env.production:
            webhook.WebHook(self.env, self.app, self.bot, self.dispatcher)

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()


def init_logging(level=logging.INFO):
    logging.basicConfig(
        format='[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z',
        level=level
    )


if __name__ == '__main__':
    init_logging(level=logging.DEBUG)
    logging.warning('Chatbot is running in the development mode.')
    Chatbot(env=environment.Env(production=False)).start_polling()
else:
    init_logging()
    logging.info('Chatbot is running in the production mode.')
    app = Chatbot().app
