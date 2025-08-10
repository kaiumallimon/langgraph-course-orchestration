from fastapi import HTTPException
from ..models.schemas import (
    ChatRequest, ChatResponse, HealthResponse, ErrorResponse,
    SessionStatsResponse, SessionListResponse, ConversationHistoryResponse
)
from ..services.workflow_service import WorkflowService
from ..views.response_formatter import ResponseFormatter
import uuid


class ChatController:
    """Controller for handling chat-related requests"""
    
    def __init__(self):
        self.workflow_service = WorkflowService()
        self.response_formatter = ResponseFormatter()

    async def process_chat_message(self, request: ChatRequest) -> ChatResponse:
        """Process a chat message through the workflow"""
        try:
            # Generate session ID if not provided
            session_id = request.session_id or str(uuid.uuid4())
            
            # Process message through workflow with session ID
            result = self.workflow_service.process_message(request.message, session_id)
            
            # Format and return response
            return self.response_formatter.format_chat_response(result, session_id)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing message: {str(e)}"
            )

    async def health_check(self) -> HealthResponse:
        """Perform health check"""
        try:
            return self.response_formatter.format_health_response()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Health check failed: {str(e)}"
            )

    async def get_session_history(self, session_id: str, limit: int = None) -> ConversationHistoryResponse:
        """Get conversation history for a session"""
        try:
            memory_service = self.workflow_service.agent_service.memory_service
            messages = memory_service.get_messages(session_id, limit)
            
            return ConversationHistoryResponse(
                session_id=session_id,
                messages=messages,
                total_messages=len(memory_service.get_messages(session_id))
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving session history: {str(e)}"
            )

    async def clear_session(self, session_id: str) -> dict:
        """Clear conversation history for a session"""
        try:
            memory_service = self.workflow_service.agent_service.memory_service
            success = memory_service.clear_session(session_id)
            
            return {
                "session_id": session_id,
                "cleared": success,
                "message": "Session cleared successfully" if success else "Session not found"
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error clearing session: {str(e)}"
            )

    async def delete_session(self, session_id: str) -> dict:
        """Delete a session completely"""
        try:
            memory_service = self.workflow_service.agent_service.memory_service
            success = memory_service.delete_session(session_id)
            
            return {
                "session_id": session_id,
                "deleted": success,
                "message": "Session deleted successfully" if success else "Session not found"
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting session: {str(e)}"
            )

    async def get_active_sessions(self) -> SessionListResponse:
        """Get list of active sessions"""
        try:
            memory_service = self.workflow_service.agent_service.memory_service
            sessions = memory_service.get_active_sessions()
            
            return SessionListResponse(
                sessions=sessions,
                total_count=len(sessions)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving active sessions: {str(e)}"
            )

    async def get_session_stats(self, session_id: str) -> SessionStatsResponse:
        """Get statistics for a specific session"""
        try:
            memory_service = self.workflow_service.agent_service.memory_service
            stats = memory_service.get_session_stats(session_id)
            
            if not stats:
                raise HTTPException(
                    status_code=404,
                    detail=f"Session {session_id} not found"
                )
            
            return SessionStatsResponse(**stats)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving session stats: {str(e)}"
            )
