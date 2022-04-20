import handlers
from handler import message, conversation

AllTypesOfHandlers = [
    message.Handler,
    conversation.Handler,
]
AllTypesOfHandlers += handlers.Handlers
