from fastapi import APIRouter, status, Depends
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from .services import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer


auth_router = APIRouter()


user_service = UserService()



@auth_router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)
async def signup(
        user_data : UserCreateModel,
        # get the session from the get_session function and depend on it if the session is not available FastAPI will create a new session
        session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
    else:
        new_user = await user_service.create_user(user_data, session)
        return new_user

@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login(
    user_data : UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        valid_password = verify_password(password, user.password_hash)
        if valid_password:
            access_token = create_access_token(
                user_data = {
                    "user_uid": str(user.uid),
                    "email": user.email,
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    "user_uid": str(user.uid),
                    "email": user.email,
                },
                refresh_token=True,
                expired = timedelta(days=2)
            )

            return JSONResponse(
                content={
                    "token_type": "bearer",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid" : str(user.uid),
                        "email": user.email,
                    }

                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

@auth_router.get(
    "/refresh_token",
    status_code=status.HTTP_200_OK
)
async def refresh_token_bearer(
    token_details = Depends(RefreshTokenBearer())
):

    print(f"token details {token_details}")
    expired_timestamp = token_details['exp']
    if datetime.fromtimestamp(expired_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data = token_details['user']
        )
        return JSONResponse(
            content={
                "token_type": "bearer",
                "access_token": new_access_token,
            }
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
