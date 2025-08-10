from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import threading
from ..models.schemas import ChatMessage


class SessionMemory:
    """Memory management for individual sessions"""
    
    def __init__(self, session_id: str, max_messages: int = 50):
        self.session_id = session_id
        self.messages: List[ChatMessage] = []
        self.max_messages = max_messages
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.metadata = {}
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session memory"""
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now()
        )
        self.messages.append(message)
        self.last_accessed = datetime.now()
        
        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self, limit: Optional[int] = None) -> List[ChatMessage]:
        """Get messages from session memory"""
        self.last_accessed = datetime.now()
        if limit:
            return self.messages[-limit:]
        return self.messages.copy()
    
    def get_conversation_context(self, include_system: bool = False) -> List[Dict[str, str]]:
        """Get conversation context in format suitable for LLM"""
        context = []
        for msg in self.messages:
            if not include_system and msg.role == "system":
                continue
            context.append({
                "role": msg.role,
                "content": msg.content
            })
        return context
    
    def clear(self) -> None:
        """Clear all messages from session"""
        self.messages.clear()
        self.last_accessed = datetime.now()
    
    def is_expired(self, ttl_hours: int = 24) -> bool:
        """Check if session has expired"""
        return datetime.now() - self.last_accessed > timedelta(hours=ttl_hours)


class MemoryService:
    """Service for managing session-based conversation memory"""
    
    def __init__(self, session_ttl_hours: int = 24, max_sessions: int = 1000):
        self.sessions: Dict[str, SessionMemory] = {}
        self.session_ttl_hours = session_ttl_hours
        self.max_sessions = max_sessions
        self._lock = threading.RLock()
    
    def get_session(self, session_id: str) -> SessionMemory:
        """Get or create a session memory"""
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = SessionMemory(session_id)
                self._cleanup_expired_sessions()
            
            return self.sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to session memory"""
        session = self.get_session(session_id)
        session.add_message(role, content)
    
    def get_conversation_context(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation context for a session"""
        session = self.get_session(session_id)
        return session.get_conversation_context()[-limit:] if limit else session.get_conversation_context()
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """Get messages from a session"""
        session = self.get_session(session_id)
        return session.get_messages(limit)
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session"""
        with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id].clear()
                return True
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session completely"""
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        with self._lock:
            return list(self.sessions.keys())
    
    def get_session_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics for a session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        return {
            "session_id": session_id,
            "message_count": len(session.messages),
            "created_at": session.created_at.isoformat(),
            "last_accessed": session.last_accessed.isoformat(),
            "is_expired": session.is_expired(self.session_ttl_hours)
        }
    
    def _cleanup_expired_sessions(self) -> None:
        """Clean up expired sessions"""
        with self._lock:
            expired_sessions = [
                session_id for session_id, session in self.sessions.items()
                if session.is_expired(self.session_ttl_hours)
            ]
            
            for session_id in expired_sessions:
                del self.sessions[session_id]
            
            # If we still have too many sessions, remove oldest ones
            if len(self.sessions) > self.max_sessions:
                sorted_sessions = sorted(
                    self.sessions.items(),
                    key=lambda x: x[1].last_accessed
                )
                sessions_to_remove = len(self.sessions) - self.max_sessions
                for session_id, _ in sorted_sessions[:sessions_to_remove]:
                    del self.sessions[session_id]
