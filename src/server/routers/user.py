from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .. import auth
from .. import orm

router = APIRouter()


class UserConfig(BaseModel):
    theme: str
    language: str


class UserSettings(BaseModel):
    default_text_model: str
    default_image_model: str
    theme: str
    language: str
    show_options_menu_when_clicking_a_message: bool
    show_explicit_content: bool


@router.get("/user/settings", tags=["user"])
async def get_user_settings(current_user: dict = Depends(auth.get_current_user)):
    user = orm.users.get(by="id", value=current_user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "default_text_model": user["default_text_model"],
        "default_image_model": user["default_image_model"],
        "theme": user["theme"],
        "language": user["language"],
        "show_options_menu_when_clicking_a_message": user[
            "show_options_menu_when_clicking_a_message"
        ],
        "show_explicit_content": user["show_explicit_content"],
        "storage_used": user["storage_used"],
        "storage_limit": user["storage_limit"],
    }


@router.put("/user/settings", tags=["user"])
async def update_user_settings(
    settings: UserSettings,
    current_user: dict = Depends(auth.get_current_user),
):
    user = orm.users.get(by="id", value=current_user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orm.users.update(
        by="id",
        value=user["id"],
        data={
            "default_text_model": settings.default_text_model,
            "default_image_model": settings.default_image_model,
            "theme": settings.theme,
            "language": settings.language,
            "show_options_menu_when_clicking_a_message": settings.show_options_menu_when_clicking_a_message,
            "show_explicit_content": settings.show_explicit_content,
        },
    )
    return {"message": "Settings updated successfully"}
