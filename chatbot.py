import queue

import flask
import mysql.connector
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
        self.db = mysql.connector.connect(
            host=env.db_host,
            user=env.db_username,
            passwd=env.db_password,
            database=env.db_name
        )
        if env.production:
            self.dispatcher = telegram.ext.Dispatcher(bot=self.bot, update_queue=queue.Queue())
            self.app = flask.Flask(__name__)
        else:
            self.updater = telegram.ext.Updater(bot=self.bot)
            self.dispatcher = self.updater.dispatcher
        for handler in handlers.Handlers:
            handler[0].chatbot = self
            if handler[0].on_receive is not None:
                handler[0].on_receive(self)
            self.dispatcher.add_handler(handler[1])
        if env.production:
            webhook.WebHook(self.env, self.app, self.bot, self.dispatcher)

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()
