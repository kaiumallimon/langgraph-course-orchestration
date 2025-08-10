from fastapi import HTTPException
from ..models.schemas import ChatRequest, ChatResponse, HealthResponse, ErrorResponse
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
            
            # Process message through workflow
            result = self.workflow_service.process_message(request.message)
            
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
