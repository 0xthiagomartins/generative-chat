from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .. import auth, orm
from ..chat import ChatBot

router = APIRouter()


class ChatMessageCreate(BaseModel):
    content: str
    model: str = "gpt-3.5-turbo"
    conversation_id: int


class ConversationCreate(BaseModel):
    title: str


class ModelChange(BaseModel):
    conversation_id: int
    new_model: str


@router.post("/conversations", tags=["chat"])
async def create_conversation(
    conversation: ConversationCreate,
    current_user: dict = Depends(auth.get_current_user),
):
    conversation_id = ChatBot().start_new_conversation(current_user["id"])
    return {"id": conversation_id, "title": conversation.title}


@router.get("/conversations", tags=["chat"])
async def get_conversations(
    current_user: dict = Depends(auth.get_current_user),
):
    conversations = orm.conversations.list(
        filter={"user_id": current_user["id"]}, order={"created_at": "desc"}, mode="all"
    )
    return conversations


@router.post("/chat/text", tags=["chat"])
async def chat(
    message: ChatMessageCreate, current_user: dict = Depends(auth.get_current_user)
):
    response = ChatBot().get_response(
        message.conversation_id,
        message.content,
        message.model,
    )
    return {"response": response}


@router.get("/chat/history/{conversation_id}", tags=["chat"])
async def get_chat_history(
    conversation_id: int, current_user: dict = Depends(auth.get_current_user)
):
    history = ChatBot().get_conversation_history(conversation_id)
    return history


@router.post("/chat/image", tags=["chat"])
async def generate_image():
    return


@router.post("/chat/change_model", tags=["chat"])
async def change_model(
    model_change: ModelChange, current_user: dict = Depends(auth.get_current_user)
):
    chat_bot = ChatBot()
    success = chat_bot.change_model(
        model_change.conversation_id, model_change.new_model
    )
    if success:
        return {"message": "Model changed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")
