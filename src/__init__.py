from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.auth.routers import auth_router

from src.db.main import init_db


# life span of the application which will be called when the application starts and ends
@asynccontextmanager
async def life_span(app:FastAPI):
    await init_db()
    yield
    print("Application shutdown")

version = "v1"

app = FastAPI(
    title="fastApi",
    description="restapi with fastapi",
    version=version,
    lifespan=life_span

)

# register the routers in the application
app.include_router(book_router,prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router,prefix=f"/api/{version}/auth", tags=["auth"])