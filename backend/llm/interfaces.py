from schemas import Message


class ChatModel:
    def call(self, messages: list[Message], **api_parameters) -> Message:
        raise NotImplementedError