from fastapi import APIRouter, status, Depends
from src.auth.schemas import UserCreateModel,UserModel
from .services import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException


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
