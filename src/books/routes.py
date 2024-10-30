from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.book_data import books
from src.books.schemas import *

book_router = APIRouter()

@book_router.get("/get_header",status_code=200)
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


@book_router.get("/", response_model=List[BookModel])
async def get_all_books():
    return books

@book_router.post('/',status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel):
    new_book = book_data.model_dump()
    books.book_routerend(new_book)
    return new_book

@book_router.get("/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_update_data : BookUpdateModel) ->dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['author'] = book_update_data.author
            return book

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book not found")

@book_router.delete("/{book_id}")
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book not found")