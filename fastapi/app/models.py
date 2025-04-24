from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, index=True, nullable=False)
    username = mapped_column(String, nullable=True)
