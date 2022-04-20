from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, CallbackQueryHandler

from handler import GetChatbot
from handlers import Handlers
from states import States


def just_answer(update: Update, context: CallbackContext):
    update.callback_query.answer()


def on_receive_chatbot(c):
    for _, value in States.items():
        value[0].provide(c)


chatbot = GetChatbot()
chatbot.on_receive = on_receive_chatbot
just_answer_handler = CallbackQueryHandler(just_answer)
Handler = chatbot, ConversationHandler(
    entry_points=[handler[1] for handler in Handlers],
    states={key: [value[1]] for key, value in States.items()},
    fallbacks=[just_answer_handler],
)
