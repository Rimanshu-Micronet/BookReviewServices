from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Book, Review
from schemas import BookCreate, ReviewCreate
from typing import List, Optional

class BookCRUD:
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.query(Book).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()
    
    @staticmethod
    def create_book(db: Session, book: BookCreate) -> Book:
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    @staticmethod
    def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
        return db.query(Book).filter(Book.isbn == isbn).first()

class ReviewCRUD:
    @staticmethod
    def get_reviews_for_book(db: Session, book_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        return db.query(Review).filter(Review.book_id == book_id).order_by(desc(Review.timestamp)).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_review(db: Session, review: ReviewCreate, book_id: int) -> Review:
        db_review = Review(**review.dict(), book_id=book_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    
    @staticmethod
    def get_review(db: Session, review_id: int) -> Optional[Review]:
        return db.query(Review).filter(Review.id == review_id).first()

book_crud = BookCRUD()
review_crud = ReviewCRUD()