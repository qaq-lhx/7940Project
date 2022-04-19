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
            handler[0].chatbot = self
            self.dispatcher.add_handler(handler[1])
        if env.production:
            webhook.WebHook(self.env, self.app, self.bot, self.dispatcher)

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()
