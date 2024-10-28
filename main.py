from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello") # path parameter name with query parameter age
async def say_hello(name: Optional[str] = 'user',age : int = 0) -> dict:
    return {
        "message": f"Hello {name}",
        "age" : f"Age is {age}"
    }


class BookModel(BaseModel):
    title: str
    author : str

@app.post("/create_book")
async def create_book(book_data : BookModel):
    return {
        "title" : book_data.title,
        "author" : book_data.author
    }

@app.get("/get_header",status_code=200)
async def get_header(
        accept: str = Header(None),
        content_type : str = Header(None),
        user_agent : str = Header(None),
        host: str = Header(None)
):
    return {
        "accept" : accept,
        "Content-Type" : content_type,
        "User-Agent" : user_agent,
        "host" : host
    }