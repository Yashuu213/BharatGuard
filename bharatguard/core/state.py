from typing import TypedDict, List, Dict, Any, Annotated, Optional
import operator
from datetime import datetime

class AgentLog(TypedDict):
    """Represents a single log entry from an agent."""
    timestamp: str
    agent_name: str
    message: str

class AgentState(TypedDict):
    """
    Enhanced State definition for BharatGuard Agent (Phase 3).
    Includes fields for the Compliance Guardian Engine.
    """
    user_task: str
    messages: Annotated[List[Dict[str, str]], operator.add]
    current_node: str
    plan: Dict[str, Any]
    compliance_checklist: List[Dict[str, Any]]
    
    # Phase 3 Fields
    compliance_details: List[Dict[str, Any]] # Detailed rule results
    compliance_score: float # Weighted final score
    fix_suggestions: List[str] # Actionable items for the Coder
    compliance_loop_count: int # To prevent infinite loops (max 3)
    
    generated_code: Dict[str, Any]
    test_results: Dict[str, Any]
    agent_logs: Annotated[List[AgentLog], operator.add]
    evolution_log: Annotated[List[Dict[str, Any]], operator.add]
    current_version: int

def create_initial_state(task: str) -> AgentState:
    """Helper to initialize the state with Phase 3 default values."""
    return {
        "user_task": task,
        "messages": [],
        "current_node": "supervisor",
        "plan": {"steps": [], "tools_needed": [], "estimated_complexity": "unknown"},
        "compliance_checklist": [],
        "compliance_details": [],
        "compliance_score": 0.0,
        "fix_suggestions": [],
        "compliance_loop_count": 0,
        "generated_code": {"backend_code": "", "frontend_code": "", "files": []},
        "test_results": {"passed": 0, "total": 0, "details": []},
        "agent_logs": [],
        "evolution_log": [{
            "timestamp": datetime.now().isoformat(),
            "event": "State Initialized",
            "details": f"Task: {task}"
        }],
        "current_version": 1
    }
