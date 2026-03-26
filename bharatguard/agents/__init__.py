from bharatguard.agents.supervisor import supervisor_node
from bharatguard.agents.planner import planner_node
from bharatguard.agents.coder import coder_node
from bharatguard.agents.tester import tester_node
from bharatguard.agents.compliance_guardian import compliance_guardian_node
from typing import Dict, Any
from bharatguard.core.state import AgentState

# Export all node functions for clean graph integration
__all__ = ["supervisor_node", "planner_node", "coder_node", "tester_node", "reporter_node", "compliance_guardian_node"]

async def reporter_node(state: AgentState) -> Dict[str, Any]:
    """
    Reporter Agent: Finalizes the output and presents it to the user.
    """
    return {
        "current_node": "reporter",
        "evolution_log": [{"event": "Execution Finished", "details": "The task has been successfully processed."}]
    }
