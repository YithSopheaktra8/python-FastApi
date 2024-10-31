from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from typing import List

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.schemas import *
from src.db.main import get_session

from src.books.services import BookService
from src.books.models import BookModel

book_router = APIRouter()

book_service = BookService()


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
async def get_all_books(session : AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post('/',status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_a_book(book_data: CreateBookModel, session : AsyncSession = Depends(get_session)):
    new_book = await book_service.create_a_book(session, book_data)
    return new_book

@book_router.get("/{book_uid}")
async def get_book(book_uid: str, session : AsyncSession = Depends(get_session)):
    book = await book_service.get_book(session,book_uid)
    if book:
        return book
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="book not found")


@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_update_data : BookUpdateModel,session : AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(session,book_uid,book_update_data)
    return updated_book

@book_router.delete("/{book_uid}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session : AsyncSession = Depends(get_session)):
    result = await book_service.delete_book(session,book_uid)
    return result
