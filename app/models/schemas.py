from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MessageClassifier(BaseModel):
    """Model for message classification"""
    course: Literal["Structured Programming Language", "English", "Physics", "None"] = Field(
        ...,
        description="Classify the message under which course it falls (None if it doesn't match any)."
    )


class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Model for incoming chat requests"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for chat responses"""
    message: str
    course: str
    session_id: Optional[str] = None
    timestamp: datetime


class HealthResponse(BaseModel):
    """Model for health check responses"""
    status: str
    message: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime


class SessionStatsResponse(BaseModel):
    """Model for session statistics responses"""
    session_id: str
    message_count: int
    created_at: datetime
    last_accessed: datetime
    is_expired: bool


class SessionListResponse(BaseModel):
    """Model for session list responses"""
    sessions: List[str]
    total_count: int


class ConversationHistoryResponse(BaseModel):
    """Model for conversation history responses"""
    session_id: str
    messages: List[ChatMessage]
    total_messages: int
