from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    content: str


@app.post("/chat")
async def chat(message: Message):
    # This is a simple echo response for testing
    return {"response": f"Server received: {message.content}"}


@app.get("/health")
async def health_check():
    return {"status": "OK"}
