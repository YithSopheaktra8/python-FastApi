from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from src.config import Config
import uuid
import logging


pwd_context = CryptContext(
    schemes=["bcrypt"]
)

ACCESS_TOKEN_EXPIRY = 3600 # 1 hour

def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expired : timedelta = None, refresh_token: bool = False) -> str:
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + expired if expired is not None else datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh_token
    token = jwt.encode(
        payload=payload,
        key= Config.JWT_SECRET,
        algorithm= Config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt= token,
            key= Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)