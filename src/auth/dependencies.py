from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.http import HTTPBearer
from fastapi import Request, HTTPException, status
from src.auth.utils import decode_access_token

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
        credential = await super().__call__(request)

        token = credential.credentials # get the token from the credential or from the request

        token_data = decode_access_token(token) # decode the token

        if not self.token_valid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        payload = decode_access_token(token)
        return True if payload is not None else False

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("This method must be implemented in the child class")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )