from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool
    created: str
    updated: str


class UserInDBModel(UserModel):
    hashed_password: str
