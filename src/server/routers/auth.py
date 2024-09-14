from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from ..auth import (
    authenticate_user,
    create_access_token,
    register_user,
)

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None
    full_name: str = ""


@router.post("/token", response_model=Token, tags=["authorization"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", tags=["authentication"])
async def register_user(user: UserCreate):
    user_id = register_user(
        username=user.username,
        email=user.email,
        password=user.password,
        full_name=user.full_name,
    )
    return {"message": "User created successfully", "user_id": user_id}
