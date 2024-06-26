from pydantic import BaseModel


class ChatRequest(BaseModel):
    content: str

class Message(BaseModel):
    role: str
    content: str
