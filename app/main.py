from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .controllers.chat_controller import ChatController
from .models.schemas import ChatRequest, ChatResponse, HealthResponse

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
