import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:

    movieID = context.args[0]

    # preparing a cursor object
    cursorObject = chatbot().db.cursor()
    cursorObject.execute( """
        SELECT name FROM MovieInfo WHERE id = %s """, ( movieID) )
    
    myresult = cursorObject.fetchall()
    for x in myresult:
        update.message.reply_text('search result : '+ str(x[0]))



chatbot = GetChatbot()
Handler = chatbot, CommandHandler('hello', hello_command)
