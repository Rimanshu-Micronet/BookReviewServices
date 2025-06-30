from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from schemas import Review, ReviewCreate
from crud import book_crud, review_crud
from exceptions import BookNotFound

router = APIRouter(prefix="/books", tags=["reviews"])
logger = logging.getLogger(__name__)

@router.get("/{book_id}/reviews", response_model=List[Review])
async def get_book_reviews(
    book_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific book.
    
    - **book_id**: The ID of the book
    - **skip**: Number of reviews to skip (pagination)
    - **limit**: Maximum number of reviews to return
    """
    # Check if book exists
    book = book_crud.get_book(db, book_id)
    if not book:
        raise BookNotFound(book_id)
    
    reviews = review_crud.get_reviews_for_book(db, book_id, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(reviews)} reviews for book {book_id}")
    
    return reviews

@router.post("/{book_id}/reviews", response_model=Review, status_code=201)
async def create_review(
    book_id: int, 
    review: ReviewCreate, 
    db: Session = Depends(get_db)
):
    """
    Add a review to a specific book.
    
    - **book_id**: The ID of the book to review
    - **reviewer_name**: Name of the reviewer (required)
    - **rating**: Rating from 1.0 to 5.0 (required)
    - **comment**: Review comment (optional)
    """
    # Check if book exists
    book = book_crud.get_book(db, book_id)
    if not book:
        raise BookNotFound(book_id)
    
    try:
        new_review = review_crud.create_review(db, review, book_id)
        logger.info(f"Created review for book {book_id} by {review.reviewer_name}")
        
        return new_review
    
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        raise HTTPException(status_code=500, detail="Failed to create review")