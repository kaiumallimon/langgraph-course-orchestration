from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .controllers.chat_controller import ChatController
from .models.schemas import (
    ChatRequest, ChatResponse, HealthResponse,
    SessionStatsResponse, SessionListResponse, ConversationHistoryResponse
)
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Course Classifier API",
    description="An AI-powered course classifier that routes questions to specialized agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize controller
chat_controller = ChatController()


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return await chat_controller.health_check()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return await chat_controller.health_check()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response with course classification
    
    - **message**: The user's message/question
    - **session_id**: Optional session ID for tracking conversations
    """
    return await chat_controller.process_chat_message(request)


@app.get("/courses")
async def get_available_courses():
    """Get list of available course categories"""
    return {
        "courses": [
            "Structured Programming Language",
            "English", 
            "Physics",
            "None"
        ],
        "description": "Available course categories for message classification"
    }


@app.get("/sessions", response_model=SessionListResponse)
async def get_active_sessions():
    """Get list of active chat sessions"""
    return await chat_controller.get_active_sessions()


@app.get("/sessions/{session_id}", response_model=SessionStatsResponse)
async def get_session_stats(session_id: str):
    """Get statistics for a specific session"""
    return await chat_controller.get_session_stats(session_id)


@app.get("/sessions/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_session_history(
    session_id: str,
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of messages returned")
):
    """
    Get conversation history for a session
    
    - **session_id**: The session ID to get history for
    - **limit**: Optional limit on number of messages (1-100)
    """
    return await chat_controller.get_session_history(session_id, limit)


@app.post("/sessions/{session_id}/clear")
async def clear_session(session_id: str):
    """
    Clear conversation history for a session
    
    - **session_id**: The session ID to clear
    """
    return await chat_controller.clear_session(session_id)


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session completely
    
    - **session_id**: The session ID to delete
    """
    return await chat_controller.delete_session(session_id)
