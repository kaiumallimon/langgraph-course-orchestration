"""
FastAPI Course Classifier Application

This is the main entry point for the MVC-patterned FastAPI application.
The application classifies user messages into different course categories
and routes them to specialized AI agents.

Run with: uvicorn main:app --reload
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )