from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    published_date: Optional[datetime] = None
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=20)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=1, max_length=100)
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if not (1.0 <= v <= 5.0):
            raise ValueError('Rating must be between 1.0 and 5.0')
        return v

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class BookWithReviews(Book):
    reviews: List[Review] = []

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None