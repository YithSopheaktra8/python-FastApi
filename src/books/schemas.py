from pydantic import BaseModel
import  uuid
from datetime import datetime

class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author : str
    publisher : str
    publish_date : str
    page_count : int
    language : str
    created_at: datetime
    updated_at: datetime


class CreateBookModel(BaseModel):
    title: str
    author : str
    publisher : str
    page_count : int
    language : str
    publish_date : str


class BookUpdateModel(BaseModel):
    title: str
    author : str
    publisher : str
    page_count : int