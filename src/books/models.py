from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg


class BookModel(SQLModel, table=True): # table=True is used to create a table in the database
    __tablename__ = "books" # the table name in the database
    uuid: str = Field(
        sa_column=Column(
            pg.UUID, # use the UUID data type from PostgreSQL
            primary_key=True, # make the uuid the primary key
            nullable=False, # make the uuid not nullable
            default=uuid.uuid4   # generate a new uuid when a new record is created
        )
    )
    title: str
    author : str
    publisher : str
    publish_date : str
    page_count : int
    language : str
    created_at: datetime = Field(
        Column(
            pg.TIMESTAMP,
            default=datetime.now # set the default value to the current datetime
        )
    )
    updated_at: datetime = Field(
        Column(
            pg.TIMESTAMP,
            default=datetime.now, # set the default value to the current datetime
        )
    )

    def __repr__(self):
        return f"book : {self.title} - author : {self.author}"