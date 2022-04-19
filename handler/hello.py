import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from handler import GetChatbot


def hello_command(update: Update, context: CallbackContext) -> None:
    print('hello command is called')
    movieID = context.args[0]
    print('movie id is '+str(movieID))
    # preparing a cursor object
    cursorObject = chatbot().db.cursor()
    cursorObject.execute( """
        SELECT name FROM MovieInfo WHERE id IS ? """, ( movieID) )
    #chatbot().db.commit()
    #query = "SELECT NAME, ROLL FROM STUDENT"
    #cursorObject.execute(query)
   
    myresult = cursorObject.fetchall()
    print('searching result is '+str(myresult))
    update.message.reply_text('search result : '+ myresult)
    
    # disconnecting from server
    #chatbot().db.close()


chatbot = GetChatbot()
Handler = chatbot, CommandHandler('hello', hello_command)
