from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


# Load credentials from environment
load_dotenv()

# Initialize the model with provider
def get_llm():
    """Get the initialized language model"""
    return init_chat_model(
        "gemini-2.5-flash",
        model_provider="google_genai"
    )
