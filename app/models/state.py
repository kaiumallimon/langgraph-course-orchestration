from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    """State model for LangGraph workflow"""
    messages: Annotated[list, add_messages]
    course: str | None
    session_id: Optional[str]
