from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None = None
    email: EmailStr


class UserIn(User):
    password: str
