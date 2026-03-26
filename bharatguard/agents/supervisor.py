import json
import logging
from datetime import datetime
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field
from bharatguard.core.state import AgentState, AgentLog
from bharatguard.utils.ollama_client import OllamaClient
from bharatguard.config import MODEL_NAME

logger = logging.getLogger(__name__)

class RoutingDecision(BaseModel):
    """
    Structured output for the supervisor's routing decision.
    """
    next_agent: Literal["planner", "coder", "tester", "reporter"] = Field(
        ..., description="The next agent to activate."
    )
    reasoning: str = Field(
        ..., description="The logic behind choosing the next agent."
    )

class SupervisorAgent:
    """
    The orchestrator of the BharatGuard system.
    Analyzes the current state and directs the flow to the appropriate worker agent.
    """
    
    def __init__(self, client: OllamaClient):
        self.client = client

    async def decide(self, state: AgentState) -> RoutingDecision:
        """
        Interrogates the LLM to decide the next transition.
        """
        system_prompt = (
            "You are the BharatGuard Supervisor. Your job is to orchestrate a team of agents: "
            "1. Planner: Designs the technical architecture and compliance framework.\n"
            "2. Coder: Generates the FastAPI and React code.\n"
            "3. Tester: Verifies the code and checks for syntax errors.\n"
            "4. Reporter: Finalizes the output for the user.\n\n"
            "Rules:\n"
            "- If no plan exists, go to 'planner'.\n"
            "- If a plan exists but no code is generated, go to 'coder'.\n"
            "- If code is generated but not yet audited for compliance, wait (handled by graph).\n"
            "- If compliance score is low, go back to 'coder'.\n"
            "- If compliance score is high but not tested, go to 'tester'.\n"
            "- If everything is complete and tested, go to 'reporter'.\n"
            "Respond ONLY with a JSON object following the RoutingDecision schema."
        )
        
        user_prompt = f"Current State Summary:\n{json.dumps(self._state_summary(state), indent=2)}"
        
        try:
            response_text = await self.client.generate(
                prompt=f"{system_prompt}\n\n{user_prompt}",
                model=MODEL_NAME
            )
            
            # Extract JSON from response (handling potential markdown)
            clean_json = self._extract_json(response_text)
            decision_dict = json.loads(clean_json)
            return RoutingDecision(**decision_dict)
            
        except Exception as e:
            logger.error(f"Supervisor decision failed: {e}")
            # Fallback logic
            return RoutingDecision(
                next_agent="planner" if not state.get("plan", {}).get("steps") else "reporter",
                reasoning=f"Fallback due to error: {str(e)}"
            )

    def _state_summary(self, state: AgentState) -> Dict[str, Any]:
        """Extracts a lightweight summary for the LLM."""
        return {
            "has_plan": bool(state.get("plan", {}).get("steps")),
            "has_code": bool(state.get("generated_code", {}).get("backend_code")),
            "compliance_score": state.get("compliance_score", 0),
            "compliance_loops": state.get("compliance_loop_count", 0),
            "test_status": state.get("test_results", {}).get("passed", 0) > 0,
            "error_logs": [log for log in state.get("agent_logs", []) if "error" in log["message"].lower() or "failed" in log["message"].lower()]
        }

    def _extract_json(self, text: str) -> str:
        """Helper to find JSON block in LLM output."""
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        return text.strip()

async def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    The node function for LangGraph integration.
    """
    client = OllamaClient()
    supervisor = SupervisorAgent(client)
    
    decision = await supervisor.decide(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "Supervisor",
        "message": f"Directed to {decision.next_agent}. Reasoning: {decision.reasoning}"
    }
    
    return {
        "current_node": "supervisor",
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Routing Decision", "details": decision.next_agent}],
        "next_agent": decision.next_agent  # Internal state for routing
    }
