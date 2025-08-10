# Course Classifier API

An intelligent AI-powered FastAPI application that automatically classifies user messages into academic course categories and routes them to specialized AI agents for expert responses.

## 🚀 Features

- **Intelligent Classification**: Automatically categorizes messages into Structured Programming Language, English, Physics, or General topics
- **Specialized AI Agents**: Each course category has a dedicated AI agent with domain expertise
- **MVC Architecture**: Clean, maintainable codebase following Model-View-Controller pattern
- **RESTful API**: Easy-to-use HTTP endpoints with automatic documentation
- **Session Management**: Optional session tracking for conversation continuity
- **LangGraph Workflow**: Sophisticated message routing using LangGraph state machines

## 🏗️ Architecture

This application follows the MVC (Model-View-Controller) pattern:

```
├── app/
│   ├── controllers/          # Request handling and business logic coordination
│   │   └── chat_controller.py
│   ├── models/              # Data models and schemas
│   │   ├── schemas.py       # Pydantic models for API
│   │   └── state.py         # LangGraph state definitions
│   ├── services/            # Business logic and external integrations
│   │   ├── agent_service.py # AI agent implementations
│   │   ├── llm_service.py   # Language model initialization
│   │   └── workflow_service.py # LangGraph workflow management
│   ├── views/               # Response formatting
│   │   └── response_formatter.py
│   └── main.py              # FastAPI application setup
├── main.py                  # Application entry point
└── requirements.txt         # Dependencies
```

## 📚 Supported Course Categories

1. **Structured Programming Language**: C programming, algorithms, data structures, coding concepts
2. **English**: Grammar, vocabulary, literature, writing, reading comprehension
3. **Physics**: Mechanics, thermodynamics, electromagnetism, optics, modern physics
4. **General**: Fallback category for questions outside the main subjects

## 🛠️ Prerequisites

- Python 3.8+
- Google AI API key (for Gemini model)
- Virtual environment (recommended)

## ⚡ Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd langgraph-tutorial

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
.\venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### 4. Run the Application

```bash
# Start the FastAPI server
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### Health Check
```http
GET /health
```
Returns the API health status.

#### Send Message
```http
POST /chat
Content-Type: application/json

{
  "message": "What is a for loop in C?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "message": "A for loop in C is a control structure...",
  "course": "Structured Programming Language",
  "session_id": "generated-or-provided-session-id",
  "timestamp": "2025-08-11T10:30:00Z"
}
```

#### Get Available Courses
```http
GET /courses
```
Returns list of supported course categories.

## 🔧 Development

### Project Structure Details

- **Controllers**: Handle HTTP requests and coordinate between services and views
- **Models**: Define data structures using Pydantic for validation and serialization
- **Services**: Contain business logic, AI agent implementations, and LangGraph workflows
- **Views**: Format responses and handle data presentation

### Adding New Course Categories

1. Update the `MessageClassifier` model in `app/models/schemas.py`
2. Add classification logic in `AgentService.classify_message()`
3. Implement the new agent method in `AgentService`
4. Update the router logic in `AgentService.router()`
5. Add the new agent node to the workflow in `WorkflowService`

### Custom AI Agents

Each agent is a method in `AgentService` that:
1. Takes a `State` object containing messages
2. Formats messages for the LLM
3. Invokes the language model
4. Returns updated state with AI response

## 🧪 Testing

### Manual Testing

You can test the API using:

1. **Browser**: Visit `http://localhost:8000/docs` for interactive testing
2. **curl**: 
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Explain Newton'\''s first law"}'
   ```
3. **Python requests**:
   ```python
   import requests
   response = requests.post(
       "http://localhost:8000/chat",
       json={"message": "How do you declare a variable in C?"}
   )
   print(response.json())
   ```

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini model | Yes |

## 📦 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for developing language model applications
- **LangGraph**: Library for building stateful, multi-actor applications
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **python-dotenv**: Environment variable management

## 🚧 Production Considerations

1. **Security**: 
   - Update CORS origins to specific domains
   - Add authentication/authorization
   - Validate and sanitize inputs

2. **Performance**:
   - Implement connection pooling
   - Add caching for common queries
   - Use async database connections

3. **Monitoring**:
   - Add logging and metrics
   - Implement health checks
   - Monitor API response times

4. **Deployment**:
   - Use production ASGI server (e.g., Gunicorn + Uvicorn)
   - Set up proper environment configuration
   - Configure reverse proxy (Nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Technologies

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google AI Documentation](https://ai.google.dev/)

## 📞 Support

For questions and support, please open an issue in the repository.
