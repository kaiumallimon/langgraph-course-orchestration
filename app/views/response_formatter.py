from datetime import datetime
from ..models.schemas import ChatResponse, HealthResponse, ErrorResponse
from langchain.schema import AIMessage


class ResponseFormatter:
    """Service for formatting API responses"""
    
    @staticmethod
    def format_chat_response(result: dict, session_id: str = None) -> ChatResponse:
        """Format chat workflow result into ChatResponse"""
        # Extract AI message content
        ai_message = None
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                ai_message = message.content
                break
        
        if not ai_message:
            ai_message = "I couldn't process your request. Please try again."
        
        course = result.get("course", "None")
        
        return ChatResponse(
            message=ai_message,
            course=course,
            session_id=session_id,
            timestamp=datetime.now()
        )
    
    @staticmethod
    def format_health_response() -> HealthResponse:
        """Format health check response"""
        return HealthResponse(
            status="healthy",
            message="Course Classifier API is running",
            timestamp=datetime.now()
        )
    
    @staticmethod
    def format_error_response(error: str, detail: str = None) -> ErrorResponse:
        """Format error response"""
        return ErrorResponse(
            error=error,
            detail=detail,
            timestamp=datetime.now()
        )
