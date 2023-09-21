from fastapi import HTTPException
from starlette.middleware import authentication
from starlette.requests import HTTPConnection

from models import User
from services.authentication import decode_jwt_token
from schemas.users import UserSchema


class AuthenticationBackend(authentication.AuthenticationBackend):

    async def verify_token(self, token: str):
        scopes = []
        if token is None:
            return scopes, None

        token = token.split()[-1]
        token_data = decode_jwt_token(token)
        if token_data is None:
            return scopes, None
        user = await User.get_or_none(id=token_data.user_id)
        if user is None:
            return scopes, None
        user = UserSchema(**user.as_dict())
        return scopes, user

    def get_token(self, conn: HTTPConnection) -> str | None:
        token = conn.headers.get("authorization")
        return token

    async def authenticate(self, conn: HTTPConnection):
        token = self.get_token(conn)
        response = await self.verify_token(token)
        scopes, user = response
        return authentication.AuthCredentials(scopes=scopes), user
