from pydantic import BaseModel


class Message:
    role: str
    content: str

class ChatModel:
    def call(self, messages: list[Message], **api_parameters) -> Message:
        raise NotImplementedError