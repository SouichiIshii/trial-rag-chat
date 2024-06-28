from typing import Literal

import requests
from pydantic import BaseModel

from backend.llm.interfaces import ChatModel
from config import OPENAI_API_KEY, OPENAI_CHAT_ENDPOINT
from schemas import Message

class OpenAIChatModel(ChatModel):
    def __init__(self, model_type="gpt-3.5-turbo") -> None:
        self.model_type = model_type
        self.api_key = OPENAI_API_KEY
        self.api_endpoint = OPENAI_CHAT_ENDPOINT
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def call(self, messages, **api_parameters):
        response = requests.post(
            url=self.api_endpoint,
            headers=self._headers,
            json=self._format_content(messages, **api_parameters)
        )
        response.raise_for_status()
        return self._format_return(response)

    def _format_content(self, messages, **api_parameters):
        content = api_parameters
        content.update({
            "messages": [msg.model_dump() for msg in messages],
            "model": self.model_type,
        })
        content_ = self.ContentForm(**content)
        return content_.model_dump()

    def _format_return(self, response):
        return Message(**response.json()["choices"][0]["message"])

    class ContentForm(BaseModel):
        messages: list[Message]
        model: Literal[
            "gpt-3.5-turbo",
            "gpt-4o"
        ]