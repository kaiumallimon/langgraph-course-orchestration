from ..models.state import State
from ..models.schemas import MessageClassifier
from .llm_service import get_llm
from .memory_service import MemoryService


class AgentService:
    """Service class for handling different agent types"""
    
    def __init__(self):
        self.llm = get_llm()
        self.memory_service = MemoryService()

    def classify_message(self, state: State) -> dict:
        """Classify the message into appropriate course category"""
        last_message = state["messages"][-1]

        messages = [
            {
                "role": "system",
                "content": """
You are a comprehensive course classifier. 
Carefully read and analyze the user query in detail. 
Then classify the message into exactly one of the following categories:

- 'Structured Programming Language': If the query is about any structured programming language concepts, 
  syntax, examples, problem-solving, manual tracing, code rewriting or topics specifically related to C programming or other structured languages.

- 'Physics': If the query is about any physics-related topics, including mechanics, thermodynamics, electromagnetism, 
  optics, modern physics, equations, laws, experiments, or problem-solving in physics.

- 'English': If the query is about English language topics, including grammar, vocabulary, writing, reading comprehension, 
  literature analysis, pronunciation, or communication skills.

- 'None': If the query does not fit into any of the above categories or is unrelated to Structured Programming Language, 
  Physics, or English.
"""
            },
            {
                "role": "user",
                "content": last_message.content
            }
        ]

        reply = self.llm.with_structured_output(MessageClassifier).invoke(messages)
        
        print("[CLASSIFICATION]: " + reply.course)
        return {
            "messages": state["messages"],
            "course": reply.course
        }

    def router(self, state: State) -> str:
        """Route to appropriate agent based on classification"""
        course = state.get("course", "None")
        if course == "Structured Programming Language":
            return "spl_agent"
        elif course == "English":
            return "english_agent"
        elif course == "Physics":
            return "physics_agent"
        else:
            return "fallback_agent"

    def spl_agent(self, state: State) -> dict:
        """Handle Structured Programming Language queries"""
        last_message = state["messages"][-1]
        session_id = state.get("session_id")
        
        # Get conversation context if session exists
        context_messages = []
        if session_id:
            context_messages = self.memory_service.get_conversation_context(session_id, limit=10)
        
        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": "You are an expert in Structured Programming Languages, especially C. Answer the user's programming questions clearly. Use the conversation history to provide contextual responses."
            }
        ]
        
        # Add conversation context
        messages.extend(context_messages)
        
        # Add current message if not already in context
        if not context_messages or context_messages[-1]["content"] != last_message.content:
            messages.append({
                "role": "user",
                "content": last_message.content
            })

        reply = self.llm.invoke(messages)
        
        # Store conversation in memory
        if session_id:
            self.memory_service.add_message(session_id, "user", last_message.content)
            self.memory_service.add_message(session_id, "assistant", reply.content)
        
        return {
            "messages": state["messages"] + [reply]
        }

    def english_agent(self, state: State) -> dict:
        """Handle English language queries"""
        last_message = state["messages"][-1]
        session_id = state.get("session_id")
        
        # Get conversation context if session exists
        context_messages = []
        if session_id:
            context_messages = self.memory_service.get_conversation_context(session_id, limit=10)
        
        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": "You are an expert in English language and literature. Provide helpful answers to grammar, vocabulary, and literature questions. Use the conversation history to provide contextual responses."
            }
        ]
        
        # Add conversation context
        messages.extend(context_messages)
        
        # Add current message if not already in context
        if not context_messages or context_messages[-1]["content"] != last_message.content:
            messages.append({
                "role": "user",
                "content": last_message.content
            })

        reply = self.llm.invoke(messages)
        
        # Store conversation in memory
        if session_id:
            self.memory_service.add_message(session_id, "user", last_message.content)
            self.memory_service.add_message(session_id, "assistant", reply.content)
        
        return {
            "messages": state["messages"] + [reply]
        }

    def physics_agent(self, state: State) -> dict:
        """Handle Physics queries"""
        last_message = state["messages"][-1]
        session_id = state.get("session_id")
        
        # Get conversation context if session exists
        context_messages = []
        if session_id:
            context_messages = self.memory_service.get_conversation_context(session_id, limit=10)
        
        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": "You are an expert physicist. Provide clear and concise answers to physics questions. Use the conversation history to provide contextual responses and build upon previous explanations."
            }
        ]
        
        # Add conversation context
        messages.extend(context_messages)
        
        # Add current message if not already in context
        if not context_messages or context_messages[-1]["content"] != last_message.content:
            messages.append({
                "role": "user",
                "content": last_message.content
            })

        reply = self.llm.invoke(messages)
        
        # Store conversation in memory
        if session_id:
            self.memory_service.add_message(session_id, "user", last_message.content)
            self.memory_service.add_message(session_id, "assistant", reply.content)
        
        return {
            "messages": state["messages"] + [reply]
        }

    def fallback_agent(self, state: State) -> dict:
        """Handle general queries that don't fit other categories"""
        last_message = state["messages"][-1]
        session_id = state.get("session_id")
        
        # Get conversation context if session exists
        context_messages = []
        if session_id:
            context_messages = self.memory_service.get_conversation_context(session_id, limit=10)
        
        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful and concise general-purpose assistant. Use the conversation history to provide contextual and relevant responses."
            }
        ]
        
        # Add conversation context
        messages.extend(context_messages)
        
        # Add current message if not already in context
        if not context_messages or context_messages[-1]["content"] != last_message.content:
            messages.append({
                "role": "user",
                "content": last_message.content
            })

        reply = self.llm.invoke(messages)
        
        # Store conversation in memory
        if session_id:
            self.memory_service.add_message(session_id, "user", last_message.content)
            self.memory_service.add_message(session_id, "assistant", reply.content)
        
        return {
            "messages": state["messages"] + [reply]
        }
