from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from database import engine, Base
from routers import books, reviews
from exceptions import BookAPIException
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    yield
    # Cleanup can be added here if needed

app = FastAPI(
    title="Book Review API",
    description="A comprehensive API for managing books and reviews",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router)
app.include_router(reviews.router)

# Custom exception handlers
@app.exception_handler(BookAPIException)
async def book_api_exception_handler(request: Request, exc: BookAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": getattr(exc, 'error_code', None)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "error_code": "VALIDATION_ERROR"
        }
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Book Review API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )