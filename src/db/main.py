from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True # allow to see sql query
    )
)

async def init_db():
    async with async_engine.begin() as conn:
        # create the table in the database if it does not exist # create the table in the database if it does not exist
        # we also can drop all tables and create them again by using the following code metadata.drop_all()
        await conn.run_sync(SQLModel.metadata.create_all)

# create a session maker to create a session to interact with the database
async def get_session() -> AsyncSession:

    Session = sessionmaker(
        bind=async_engine, # bind the session to the engine
        class_=AsyncSession, # use the AsyncSession class to create the session
        expire_on_commit=False # do not expire the session on commit to allow us to use the session after committing
    )

    async with Session() as session:
        yield session