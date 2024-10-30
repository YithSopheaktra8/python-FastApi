from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from src.books.models import BookModel

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True # allow to see sql query
    )
)

async def init_db():
    async with engine.begin() as conn:
        # create the table in the database if it does not exist # create the table in the database if it does not exist
        # we also can drop all tables and create them again by using the following code metadata.drop_all()
        await conn.run_sync(SQLModel.metadata.create_all)