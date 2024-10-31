from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select,desc

from src.books.models import BookModel
from src.books.schemas import CreateBookModel, BookUpdateModel
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.execute(statement) # execute the statement
        books = result.scalars().all() # get all the books from the result and convert them to a list
        return books

    async def create_a_book(self, session: AsyncSession, book_data: CreateBookModel):
        # Debugging statement to verify `book_data` type
        print("Type of book_data:", type(book_data))

        # Use `model_dump` and verify that `book_data` is of `CreateBookModel`
        if isinstance(book_data, CreateBookModel):
            book_data_dict = book_data.model_dump()
        else:
            raise TypeError("book_data is not an instance of CreateBookModel")

        new_book = BookModel(**book_data_dict) # create a new instance of the Book

        new_book.publish_date = datetime.strptime(book_data_dict["publish_date"], "%Y-%m-%d")

        session.add(new_book) # add the new book to the session
        await session.commit() # commit the session to save the new book to the database
        return new_book

    async def get_book(self, session: AsyncSession, book_uid: str):
        statement = select(BookModel).where(BookModel.uid == book_uid)
        result = await session.execute(statement)
        book = result.scalar_one_or_none()
        return book if book is not None else None

    async def update_book(self, session: AsyncSession, book_id: str, book_update_data: BookUpdateModel):
        book_to_update = self.get_book(session, book_id) # get the book to update
        if book_to_update: # check if the book exists
            book_update_data_dict = book_update_data.model_dump() # convert the book update data to a dictionary
            for key, value in book_update_data_dict.items(): # loop through the dictionary
                setattr(book_to_update, key, value) # set the attribute of the book to update
            await session.commit() # commit the session to save the changes
            return book_to_update
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_to_delete = self.get_book(session, book_uid)  # get the book to delete
        if book_to_delete is not None: # check if the book exists
            await session.delete(book_to_delete) # delete the book
            await session.commit()
            return {"message": "Book deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Book not found")