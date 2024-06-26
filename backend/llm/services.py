from interfaces import Message, ChatModel
from models import OpenAIChatModel


class ChatService:
    def __init__(self, model: ChatModel) -> None:
        self.model = model

    def get_chat(self, messages: list[Message], **api_parameters) -> Message:
        return self.model.call(messages, **api_parameters)
