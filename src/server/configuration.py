from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("=" * 10)
print("OPENAI_API_KEY:")
print(OPENAI_API_KEY)
print("=" * 10)
