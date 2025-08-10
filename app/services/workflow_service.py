from langgraph.graph import StateGraph, START, END
from ..models.state import State
from .agent_service import AgentService


class WorkflowService:
    """Service for managing the LangGraph workflow"""
    
    def __init__(self):
        self.agent_service = AgentService()
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()

    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(State)
        
        # Add nodes
        workflow.add_node("classify_message", self.agent_service.classify_message)
        workflow.add_node("spl_agent", self.agent_service.spl_agent)
        workflow.add_node("english_agent", self.agent_service.english_agent)
        workflow.add_node("physics_agent", self.agent_service.physics_agent)
        workflow.add_node("fallback_agent", self.agent_service.fallback_agent)

        # Add edges
        workflow.add_edge(START, "classify_message")
        workflow.add_conditional_edges("classify_message", self.agent_service.router)
        workflow.add_edge("spl_agent", END)
        workflow.add_edge("english_agent", END)
        workflow.add_edge("physics_agent", END)
        workflow.add_edge("fallback_agent", END)

        return workflow

    def process_message(self, message: str, session_id: str = None) -> dict:
        """Process a message through the workflow"""
        result = self.app.invoke({
            "messages": [{"role": "user", "content": message}],
            "session_id": session_id
        })
        return result
