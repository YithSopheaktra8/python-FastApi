from pydantic import BaseModel, Field
import uuid
from datetime import datetime, date



class UserCreateModel(BaseModel):
    first_name: str = Field(
        max_length=20,
        min_length=3
    )
    last_name: str = Field(
        max_length=20,
        min_length=3
    )
    username: str = Field(
        max_length=20,
        min_length=3
    )
    email: str = Field(
        max_length=50,
        min_length=5
    )
    password: str = Field(
        max_length=20,
        min_length=8
    )


class UserModel(BaseModel):
    uid : uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(
        exclude=True
    )
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserLoginModel(BaseModel):
    email: str
    password: str