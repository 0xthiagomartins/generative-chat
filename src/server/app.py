from fastapi import FastAPI
from .routers import chat, user, auth
from sqlmodel import SQLModel, create_engine
from sqlmodel_controller import set_engine

# Create a SQLite engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Create the engine
engine = create_engine(sqlite_url, echo=True)

app = FastAPI()

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    # Set the engine for sqlmodel-controller
    set_engine(engine)

    # Create the database tables
    SQLModel.metadata.create_all(engine)


@app.get("/health")
async def health_check():
    return {"status": "OK"}
