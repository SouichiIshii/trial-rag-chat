from pydantic import BaseModel


class ChatRequest(BaseModel):
    content: str

class Message:
    role: str
    content: str
