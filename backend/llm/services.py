import json
import re

from backend.llm.interfaces import ChatModel
from backend.llm.models import OpenAIChatModel
from schemas import Message

class ChatService:
    def __init__(self, model: ChatModel) -> None:
        self.model = model

    def get_chat(self, messages: list[Message], **api_parameters) -> Message:
        return self.model.call(messages, **api_parameters)

    def get_keywords(self, text: str) -> list[str]:
        prompt = """
        Extract important keyword from the text you'll be given.
        Return response in JSON format like below.
        {"keywords": ["financial", "fiscal year", "football"]}

        Text is below.
        ### Text
        """
        prompt += text
        prompt += """
        ### JSON
        """

        res = self.get_chat(messages=[Message(role="user", content=prompt)])
        res_content = re.search(r'\{\s*"keywords": \[[^\]]*\]*\}', res.content)
        content = res_content.group(0)
        result = json.loads(content)["keywords"]
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
