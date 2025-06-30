"""
Simple script to run the FastAPI application
Usage: python run.py
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )