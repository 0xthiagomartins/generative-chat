from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from openai import RateLimitError, AuthenticationError
from langchain_core.language_models.chat_models import BaseChatModel


class LangChainService:
    def __init__(self):
        self.models: dict[str, BaseChatModel] = {
            "gpt-3.5-turbo": ChatOpenAI(model_name="gpt-3.5-turbo"),
            "gpt-4": ChatOpenAI(model_name="gpt-4"),
            "gpt-4o": ChatOpenAI(model_name="gpt-4o"),
            "gpt-4o-mini": ChatOpenAI(model_name="gpt-4o-mini"),
            "gpt-4-turbo": ChatOpenAI(model_name="gpt-4-turbo"),
            "gpt-4-turbo-preview": ChatOpenAI(model_name="gpt-4-turbo-preview"),
            "gpt-4-turbo-2024-04-09": ChatOpenAI(model_name="gpt-4-turbo-2024-04-09"),
            "gpt-4-turbo-2024-08-06": ChatOpenAI(model_name="gpt-4-turbo-2024-08-06"),
            "gpt-4-turbo-2024-08-06-preview": ChatOpenAI(
                model_name="gpt-4-turbo-2024-08-06-preview"
            ),
            "claude-3-opus": ChatAnthropic(model_name="claude-3-opus"),
            "claude-3-sonnet": ChatAnthropic(model_name="claude-3-sonnet"),
            "claude-3-haiku": ChatAnthropic(model_name="claude-3-haiku"),
            "claude-3-5-sonnet": ChatAnthropic(model_name="claude-3-5-sonnet"),
            "claude-3-5-sonnet-2024-06-20": ChatAnthropic(
                model_name="claude-3-5-sonnet-2024-06-20"
            ),
            "gemini-1.5-flash": ChatGoogleGenerativeAI(model_name="gemini-1.5-flash"),
            "gemini-1.5-pro": ChatGoogleGenerativeAI(model_name="gemini-1.5-pro"),
        }

    def get_response(self, conversation: ConversationChain, message: str):
        try:
            response = conversation.predict(input=message)
            return response
        except RateLimitError:
            return "I apologize, but the AI service is currently unavailable due to rate limiting. Please try again later."
        except AuthenticationError:
            return "There's an issue with the AI service authentication. Please contact support."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def start_new_conversation(self, llm: str = "gpt-3.5-turbo") -> ConversationChain:
        return ConversationChain(
            llm=self.models[llm], memory=ConversationBufferMemory()
        )

    def process_image(self, image, prompt, model="gpt-4-vision-preview"):
        chat = ChatOpenAI(model=model)
        messages = [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": image},
                ]
            )
        ]
        response = chat(messages)
        return response.content


langchain_service = LangChainService()
