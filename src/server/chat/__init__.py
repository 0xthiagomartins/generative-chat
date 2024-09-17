from .. import orm
from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from openai import RateLimitError, AuthenticationError
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.memory.chat_memory import BaseChatMemory, BaseMemory
from langchain.prompts import (
    ChatPromptTemplate,
    BaseChatPromptTemplate,
)


MODELS: dict[str, BaseChatModel] = {
    "gpt-3.5-turbo": ChatOpenAI,
    "gpt-4": ChatOpenAI,
    "gpt-4-turbo": ChatOpenAI,
    "gpt-4-turbo-preview": ChatOpenAI,
    "claude-3-opus": ChatAnthropic,
    "claude-3-sonnet": ChatAnthropic,
    "claude-3-haiku": ChatAnthropic,
    "gemini-1.5-pro": ChatGoogleGenerativeAI,
    "gemini-1.5-pro-preview": ChatGoogleGenerativeAI,
}


class Model:
    def __init__(self, name: str, api_key: str = None):
        self.name: str = name
        self.chat: BaseChatModel = self.get_chat(name, api_key=api_key)
        self.can_send_attachments: bool = False

    def get_chat(self, name: str, *args, **kwargs) -> BaseChatModel:
        assert name in MODELS, f"Model {name} not available"
        return MODELS[name](model_name=name, *args, **kwargs)


class ChatBot:
    system_message = "You are a helpful AI assistant."

    def __init__(self, user_id: int):
        self.prompt_template: BaseChatPromptTemplate = ChatPromptTemplate.from_messages(
            [("system", self.system_message), ("user", "{input}")]
        )
        self.user_id = user_id
        self.model: Model = Model("gpt-4")
        self.conversations: dict[int, InMemoryChatMessageHistory] = {}

    def get_response(self, conversation_id: int, content: str, model: str) -> str:
        user_message_data = {
            "conversation_id": conversation_id,
            "content": content,
            "is_from_user": True,
        }
        orm.messages.create(data=user_message_data)
        conversation = self.conversations[conversation_id]
        ai_response = self.__get_response(conversation, content)
        ai_message_data = {
            "conversation_id": conversation_id,
            "content": ai_response,
            "is_from_user": False,
        }
        orm.conversation_messages.create(data=ai_message_data)
        return ai_response

    def __get_response(
        self, conversation: InMemoryChatMessageHistory, message: str
    ) -> str:
        try:
            response = conversation.predict(input=message)
            return response
        except RateLimitError:
            return "I apologize, but the AI service is currently unavailable due to rate limiting. Please try again later."
        except AuthenticationError:
            return "There's an issue with the AI service authentication. Please contact support."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def start_new_conversation(self, model: str = "gpt-3.5-turbo") -> int:
        conversation_id = orm.conversations.create(data={"user_id": self.user_id})
        memory: BaseChatMemory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        conversation: ConversationChain = ConversationChain(
            llm=self.model.chat, prompt=self.prompt_template, memory=memory
        )
        self.conversations[conversation_id] = conversation
        orm.conversations.update(
            by="id",
            value=conversation_id,
            data={
                "title": "New Conversation",
                "messages": [],
            },
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

    def change_model(self, conversation_id: int, new_model: str):
        if conversation_id not in self.conversations:
            return False
        old_conversation = self.conversations[conversation_id]
        new_conversation = self.langchain_service.start_new_conversation(new_model)
        new_conversation.memory = old_conversation.memory
        orm.conversations.update(
            by="id", value=conversation_id, data={"conversation": new_conversation}
        )
        self.conversations[conversation_id] = new_conversation
        return True
