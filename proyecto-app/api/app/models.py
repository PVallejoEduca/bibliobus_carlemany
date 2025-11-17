from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    isbn: Mapped[str | None] = mapped_column(String(40))
    authors: Mapped[str | None] = mapped_column(Text)
    original_publication_year: Mapped[int | None] = mapped_column(Integer)
    original_title: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    language_code: Mapped[str | None] = mapped_column(String(16))
    image_url: Mapped[str | None] = mapped_column(Text)

    copies: Mapped[list["Copy"]] = relationship(back_populates="book", cascade="all, delete-orphan")


class Copy(Base):
    __tablename__ = "copies"

    copy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False)

    book: Mapped[Book] = relationship(back_populates="copies")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="copy")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String)
    member_since: Mapped[date | None] = mapped_column(Date)

    ratings: Mapped[list["Rating"]] = relationship(back_populates="user")
    login: Mapped["UserLogin"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserLogin(Base):
    __tablename__ = "user_logins"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    nickname: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    user: Mapped[User] = relationship(back_populates="login")


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (CheckConstraint("rating BETWEEN 1 AND 5", name="rating_between_1_5"),)

    rating_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    copy_id: Mapped[int] = mapped_column(ForeignKey("copies.copy_id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="ratings")
    copy: Mapped[Copy] = relationship(back_populates="ratings")
