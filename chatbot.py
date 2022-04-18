#!/usr/bin/env python3

import http
import logging
import os
import queue

import flask
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher

global bot
global dispatcher
global app


def init():
    global bot
    global dispatcher
    global app
    bot = Bot(token=os.environ['TELEGRAM_ACCESS_TOKEN'])
    dispatcher = Dispatcher(bot=bot, update_queue=queue.Queue())

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('hello', hello_command))
    app = flask.Flask(__name__)


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info('Update: ' + str(update))
    logging.info('context: ' + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')



def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


init()


@app.post('/' + os.environ['TELEGRAM_WEBHOOK_SECRET_PATH'])
def on_webhook_request():
    dispatcher.process_update(Update.de_json(flask.request.get_json(force=True), bot))
    return flask.Response('', status=http.HTTPStatus.NO_CONTENT)


@app.errorhandler(http.HTTPStatus.NOT_FOUND)
@app.errorhandler(http.HTTPStatus.METHOD_NOT_ALLOWED)
def on_unauthorized_request(e):
    status = http.HTTPStatus(http.HTTPStatus.UNAUTHORIZED)
    return flask.Response(str(status.value) + ' ' + status.phrase, status=status.value, mimetype='text/plain')
