from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks import get_openai_callback
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from typing import Dict, Tuple, Any

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
SYSTEM_MESSAGE = "You are a helpful AI assistant."
PERSIST_DIRECTORY = "./chroma_db"


class Model:
    def __init__(self, name: str, api_key: str = None):
        self.name: str = name
        self.chat: BaseChatModel = self.get_chat(name, api_key)
        self.can_send_attachments: bool = False

    def get_chat(self, name: str, api_key: str = None) -> BaseChatModel:
        assert name in MODELS, f"Model {name} not available"
        api_key = os.getenv(f"{name.upper().replace('-', '_')}_API_KEY")
        return MODELS[name](model_name=name, api_key=api_key)


class Chatbot:
    def __init__(self):
        self.current_model: Model = Model("gpt-4")
        self.conversation = self._create_conversation()
        self.vectorstore = Chroma(
            embedding_function=OpenAIEmbeddings(), persist_directory=PERSIST_DIRECTORY
        )
        self.session_store: Dict[str, InMemoryChatMessageHistory] = {}

    def _create_conversation(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_MESSAGE),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        return ConversationChain(
            memory=memory, prompt=prompt, llm=self.current_model.chat
        )

    def switch_model(self, model_name):
        if model_name in MODELS:
            self.current_model = Model(model_name)
            self.conversation = self._create_conversation()
            return f"Switched to {model_name} model."
        else:
            return f"Model {model_name} not available."

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.session_store:
            self.session_store[session_id] = InMemoryChatMessageHistory()
        return self.session_store[session_id]

    def chat(self, user_input: str, user_id: str):
        with_message_history = RunnableWithMessageHistory(
            self.conversation, self.get_session_history
        )
        config = {"configurable": {"session_id": user_id}}

        # Retrieve conversation history from vector store
        results = self.vectorstore.similarity_search(
            user_input, k=5, filter={"user_id": user_id}
        )

        if results:
            history = [eval(doc.page_content) for doc in results]
            for hist in history:
                for msg in hist["messages"]:
                    if msg["type"] == "human":
                        self.get_session_history(user_id).add_user_message(
                            msg["content"]
                        )
                    else:
                        self.get_session_history(user_id).add_ai_message(msg["content"])

        # Generate response
        with get_openai_callback() as cb:
            response = with_message_history.invoke(
                [HumanMessage(content=user_input)],
                config=config,
            )

        # Store updated conversation in vector store
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.current_model.name,
            "messages": [
                {
                    "type": "human" if isinstance(msg, HumanMessage) else "ai",
                    "content": msg.content,
                }
                for msg in self.get_session_history(user_id).messages
            ],
        }
        self.vectorstore.add_texts(
            texts=[str(conversation_data)],
            metadatas=[{"user_id": user_id}],
            ids=[f"{user_id}_{datetime.now().timestamp()}"],
        )

        return response.content, cb

    def save_state(self, filename: str) -> None:
        # Implement state saving logic
        pass

    def load_state(self, filename: str) -> None:
        # Implement state loading logic
        pass


# Usage example:
# chatbot = Chatbot()
# response, callback = chatbot.chat("Hello, how are you?", "user123")
# print(response)
# print(f"Tokens used: {callback.total_tokens}")
#
# chatbot.switch_model('claude-3-opus')
# response, callback = chatbot.chat("What's the weather like?", "user123")
# print(response)
# print(f"Tokens used: {callback.total_tokens}")
