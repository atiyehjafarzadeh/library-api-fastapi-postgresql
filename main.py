from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session


# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# SQLAlchemy models
class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )


# Create the table if it does not exist
Base.metadata.create_all(bind=engine)


# Pydantic schemas
class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: Optional[int] = Field(default=None, ge=0)
    available: bool = True


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    author: Optional[str] = Field(default=None, min_length=1)
    year: Optional[int] = Field(default=None, ge=0)
    available: Optional[bool] = None


class BookOut(BookIn):
    id: int

    model_config = {"from_attributes": True}


app = FastAPI(
    title="Library API",
    description="A library management API using PostgreSQL",
    version="2.0.0",
)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def find_book(db: Session, book_id: int) -> BookModel:
    book = db.get(BookModel, book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


# GET /books
@app.get("/books", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(BookModel).order_by(BookModel.id).all()


# POST /books
@app.post("/books", response_model=BookOut, status_code=201)
def add_book(data: BookIn, db: Session = Depends(get_db)):
    book = BookModel(**data.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


# GET /books/{id}
@app.get("/books/{id}", response_model=BookOut)
def get_book(id: int, db: Session = Depends(get_db)):
    return find_book(db, id)


# PATCH /books/{id}
@app.patch("/books/{id}", response_model=BookOut)
def update_book(
    id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
):
    book = find_book(db, id)
    changes = data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if value is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )

    for field, value in changes.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book


# DELETE /books/{id}
@app.delete("/books/{id}", status_code=204)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = find_book(db, id)

    db.delete(book)
    db.commit()

    return Response(status_code=204)
