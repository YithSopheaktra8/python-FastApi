from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash

class UserService:
    async def get_user_by_email(self, email : str, session : AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email : str, session : AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data:UserCreateModel , session: AsyncSession):
        user_data_dict = user_data.model_dump() # convert the pydantic model to a dictionary
        new_user = User(**user_data_dict) # create a User instance from the dictionary or impasse the dictionary as keyword arguments
        new_user.password_hash = generate_password_hash(user_data_dict["password"]) # generate the password hash
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user) # refresh the user to get the uid or the primary key
        return new_user
