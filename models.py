from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    published_date = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    isbn = Column(String(20), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to reviews
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reviewer_name = Column(String(100), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    comment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to book
    book = relationship("Book", back_populates="reviews")

# Create index for faster queries on book_id
Index('ix_reviews_book_id', Review.book_id)