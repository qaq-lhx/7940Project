import logging

from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from handler import GetChatbot, start
from states import States


def hello_command(update: Update, context: CallbackContext) -> None:
    logging.info(context.args)
    update.message.reply_text('Good day, ' + ' '.join(context.args) + '!')


def on_receive_chatbot(c):
    for _, value in States.items():
        value[0].provide(c)


chatbot = GetChatbot()
chatbot.on_receive = on_receive_chatbot
Handler = chatbot, ConversationHandler(
    entry_points=[start.Handler[1]],
    states={key: [value[1]] for key, value in States.items()},
    fallbacks=[start.Handler[1]]
)
