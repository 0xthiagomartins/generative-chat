from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from .routers import chat, user, auth


app = FastAPI()

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    from . import configuration
    from . import orm


@app.get("/health")
async def health_check():
    return {"status": "OK"}
