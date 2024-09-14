from passlib.context import CryptContext
from .. import orm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticator:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_user(username: str = None):
        if username:
            return orm.users.get(by="username", value=username)
        return None

    @staticmethod
    def authenticate_user(username: str, password: str):
        user = orm.users.get(by="username", value=username)
        if not user or not user["hashed_password"]:
            return False
        if not Authenticator.verify_password(password, user["hashed_password"]):
            return False
        return user

    @staticmethod
    def register_user(
        username: str = None,
        email: str = None,
        password: str = None,
        full_name: str = "",
    ):
        if not username:
            raise ValueError("Username must be provided")

        existing_user = None
        if username:
            existing_user = orm.users.get(by="username", value=username)
        if existing_user:
            raise ValueError("Username already exists")

        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
        }
        if password:
            user_data["hashed_password"] = pwd_context.hash(password)

        user_id = orm.users.create(data=user_data)
        return user_id
