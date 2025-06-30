from fastapi import HTTPException
from typing import Any, Dict, Optional

class BookAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code

class BookNotFound(BookAPIException):
    def __init__(self, book_id: int):
        super().__init__(
            status_code=404,
            detail=f"Book with id {book_id} not found",
            error_code="BOOK_NOT_FOUND"
        )

class BookAlreadyExists(BookAPIException):
    def __init__(self, isbn: str):
        super().__init__(
            status_code=400,
            detail=f"Book with ISBN {isbn} already exists",
            error_code="BOOK_ALREADY_EXISTS"
        )

class InvalidRating(BookAPIException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Rating must be between 1.0 and 5.0",
            error_code="INVALID_RATING"
        )

class ValidationError(BookAPIException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )