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

    def generate_answer(self, messages: list[Message], contexts: list[str]) -> str:
        if not contexts:
            return "関連するファイルを見つけられませんでした。"
        
        question = messages[-1].content
        contexts_ = "\n\n".join(contexts)

        base_prompt = """
        Answer question using the following pieces of retrieved context.
        Use up to three sentences to answer.
        You should answer in Japanese.

        <Question>
        {}

        <Contexts>
        {}
        """
        prompt = base_prompt.format(question, contexts_)

        return self.get_chat(messages=[Message(role="user", content=prompt)]).content
