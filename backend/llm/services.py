import json

from interfaces import Message, ChatModel
from models import OpenAIChatModel
from schemas import Message

class ChatService:
    def __init__(self, model: ChatModel) -> None:
        self.model = model

    def get_chat(self, messages: list[Message], **api_parameters) -> Message:
        return self.model.call(messages, **api_parameters)

    def get_keywords(self, text: str) -> list[str]:
        prompt = """
        Extract important keyword from the text you'll be given.
        Return response as JSON as below.
        {"keywords": ["financial", "fiscal year", "football"]}

        Text is below.
        ### Text
        """
        prompt += text
        prompt += """
        ### JSON
        """

        tmp = self.get_chat(messages=[Message(role="user", content=prompt)])
        result = json.loads(tmp.content)["keywords"]
        return result

    def generate_answer(self, message):
        pass