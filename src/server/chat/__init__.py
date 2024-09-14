from .langchain_service import LangChainService
from .. import orm


class ChatBot:
    def __init__(self):
        self.langchain_service = LangChainService()
        self.conversations = {}

    def get_response(self, conversation_id: int, content: str, model: str) -> str:
        user_message_data = {
            "conversation_id": conversation_id,
            "content": content,
            "is_from_user": True,
        }
        orm.chat_messages.create(data=user_message_data)
        conversation = self.conversations[conversation_id]
        ai_response = self.langchain_service.get_response(conversation, content)
        ai_message_data = {
            "conversation_id": conversation_id,
            "content": ai_response,
            "is_from_user": False,
        }

        orm.chat_messages.create(data=ai_message_data)
        return ai_response

    def start_new_conversation(self, user_id: int, model: str = "gpt-3.5-turbo") -> int:
        conversation_id = orm.conversations.create(data={"user_id": user_id})
        conversation = self.langchain_service.start_new_conversation(
            conversation_id, model
        )
        self.conversations[conversation_id] = conversation
        orm.conversations.update(
            by="id", value=conversation_id, data={"conversation": conversation}
        )
        return conversation_id

    def get_conversation_history(self, conversation_id: int):
        return orm.conversations.list(
            filter={"conversation_id": conversation_id, "archived": False},
            order={"timestamp": "desc"},
            mode="all",
        )

    def delete_conversation(self, conversation_id: int):
        self.conversations.pop(conversation_id)
        return orm.conversations.delete(by="id", value=conversation_id)

    def get_response(self, conversation_id: int, message: str):
        if conversation_id not in self.conversations:
            self.start_new_conversation(conversation_id)

        return self.langchain_service.get_response(
            self.conversations[conversation_id], message
        )
