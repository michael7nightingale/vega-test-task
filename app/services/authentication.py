from jose import jwt, JWTError
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core.config import get_app_settings
from app.schemas.token import Token


def encode_jwt_token(user_id: str) -> str:
    settings = get_app_settings()
    token = Token(
        user_id=user_id,
        exp=datetime.now() + timedelta(minutes=settings.EXPIRE_MINUTES)
    )
    return jwt.encode(
        token.model_dump(),
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_jwt_token(encoded_token: str) -> Token | None:
    settings = get_app_settings()
    try:
        payload = jwt.decode(
            token=encoded_token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return Token(**payload)
    except (JWTError, ValidationError):
        return


def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return sha256_crypt.verify(password, hashed_password)
