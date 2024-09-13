from fastapi import FastAPI
from .routers import chat, user, auth
from .connection import engine  # Import the engine from your connection module

app = FastAPI()

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    # Create all tables
    from . import connection


@app.get("/health")
async def health_check():
    return {"status": "OK"}
