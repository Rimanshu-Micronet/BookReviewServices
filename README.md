# Book Review API

A comprehensive FastAPI-based Book Review service with caching, database migrations, and proper error handling.

## Features

- **RESTful API** with OpenAPI/Swagger documentation
- **SQLAlchemy ORM** with PostgreSQL/SQLite support
- **Redis caching** for improved performance
- **Alembic migrations** for database schema management
- **Pydantic validation** for request/response models
- **Comprehensive error handling** with proper HTTP status codes
- **Modular architecture** with clean separation of concerns

## API Endpoints

### Books
- `GET /books` - Fetch all books (with caching)
- `POST /books` - Create a new book
- `GET /books/{id}` - Get a specific book with reviews

### Reviews
- `GET /books/{id}/reviews` - Get all reviews for a book
- `POST /books/{id}/reviews` - Add a review to a book

### Utility
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start Redis (optional, for caching):
```bash
redis-server
```

5. Run the application:
```bash
python run.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Configuration

Environment variables (set in `.env` file):

- `DATABASE_URL` - Database connection string (default: sqlite:///./books.db)
- `REDIS_URL` - Redis connection string (default: redis://localhost:6379)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

## Database Schema

### Books Table
- `id` - Primary key
- `title` - Book title (required)
- `author` - Book author (required)
- `published_date` - Publication date (optional)
- `description` - Book description (optional)
- `isbn` - ISBN (optional, unique)
- `created_at` - Creation timestamp

### Reviews Table
- `id` - Primary key
- `book_id` - Foreign key to books table
- `reviewer_name` - Name of reviewer (required)
- `rating` - Rating 1.0-5.0 (required)
- `comment` - Review comment (optional)
- `timestamp` - Review timestamp

## Caching Strategy

The API implements Redis caching for the `GET /books` endpoint:

1. On request, check Redis cache first
2. If cache miss, query database
3. Store result in cache with TTL
4. Cache is invalidated when new books are created

## Error Handling

The API provides comprehensive error handling with proper HTTP status codes:

- `400` - Bad Request (validation errors, invalid data)
- `404` - Not Found (book not found)
- `500` - Internal Server Error

All errors include detailed error messages and optional error codes.

## Development

### Running Tests
```bash
# Add your test framework and run tests
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

1. Set environment variables appropriately
2. Use PostgreSQL instead of SQLite
3. Configure Redis for caching
4. Set up proper CORS origins
5. Use production WSGI server like Gunicorn
6. Implement proper logging and monitoring

## License

MIT License