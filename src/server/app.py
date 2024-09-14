from fastapi import FastAPI
from .routers import chat, user, auth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Ensure OPENAI_API_KEY is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

app = FastAPI()

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    from . import orm


@app.get("/health")
async def health_check():
    return {"status": "OK"}
