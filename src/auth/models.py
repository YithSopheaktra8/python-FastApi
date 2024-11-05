from datetime import datetime, date
import uuid
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, # use the UUID data type from PostgreSQL
            primary_key=True, # make the uuid the primary key
            nullable=False, # make the uuid not nullable
            default=uuid.uuid4   # generate a new uuid when a new record is created
        )
    )
    username : str
    email : str
    first_name : str
    last_name : str
    password_hash : str = Field(
        exclude= True # exclude the password_hash from the response

    )
    is_verified : bool = Field(
        default=False # set the default value to False
    )
    created_at : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now # set the default value to the current datetime
        )
    )
    updated_at : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now # set the default value to the current datetime
        )
    )

    # define a method to return a string representation of the User
    def __repr__(self):
        return f"User : {self.username} - email : {self.email}"
