from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from schemas import Book, BookCreate, BookWithReviews
from crud import book_crud
from cache import cache
from exceptions import BookNotFound, BookAlreadyExists

router = APIRouter(prefix="/books", tags=["books"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[Book])
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all books with caching support.
    
    - **skip**: Number of books to skip (pagination)
    - **limit**: Maximum number of books to return
    """
    cache_key = f"books:list:{skip}:{limit}"
    
    # Try to get from cache first
    cached_books = cache.get(cache_key)
    if cached_books:
        logger.info("Books retrieved from cache")
        return cached_books
    
    # If not in cache, get from database
    books = book_crud.get_books(db, skip=skip, limit=limit)
    books_data = [Book.from_orm(book).dict() for book in books]
    
    # Cache the result
    cache.set(cache_key, books_data)
    logger.info(f"Retrieved {len(books)} books from database and cached")
    
    return books

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **published_date**: When the book was published (optional)
    - **description**: Book description (optional)
    - **isbn**: Book ISBN (optional, must be unique)
    """
    # Check if book with same ISBN already exists
    if book.isbn:
        existing_book = book_crud.get_book_by_isbn(db, book.isbn)
        if existing_book:
            raise BookAlreadyExists(book.isbn)
    
    try:
        new_book = book_crud.create_book(db, book)
        
        # Invalidate books cache
        cache.invalidate_pattern("books:list:*")
        
        logger.info(f"Created new book: {new_book.title}")
        return new_book
    
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise HTTPException(status_code=500, detail="Failed to create book")

@router.get("/{book_id}", response_model=BookWithReviews)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a specific book by ID including its reviews.
    
    - **book_id**: The ID of the book to retrieve
    """
    book = book_crud.get_book(db, book_id)
    if not book:
        raise BookNotFound(book_id)
    
    return book