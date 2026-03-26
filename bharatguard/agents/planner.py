import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from bharatguard.core.state import AgentState, AgentLog
from bharatguard.utils.ollama_client import OllamaClient
from bharatguard.config import MODEL_NAME

logger = logging.getLogger(__name__)

from bharatguard.config import MODEL_NAME, PROMPT_EVOLUTION_PATH
import os

class PlannerAgent:
    """
    The architect of the system.
    Takes a user task and defines the design, tech stack, and compliance requirements.
    """
    
    def __init__(self, client: OllamaClient):
        self.client = client
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Loads the refined prompt if version 2 exists, else uses default."""
        if os.path.exists(PROMPT_EVOLUTION_PATH):
            with open(PROMPT_EVOLUTION_PATH, "r") as f:
                return f.read()
        
        return (
            "You are the BharatGuard Planner. Your role is to design technical architectures "
            "that are compliant with Indian regulations.\n\n"
            "Identify which categories apply to the task (GST, UPI, Aadhaar, DPDP, RBI).\n\n"
            "Requirement details for your plan:\n"
            "- GST: For commerce or taxation.\n"
            "- UPI: For payments or money transfers.\n"
            "- Aadhaar: For identity, KYC, or logins.\n"
            "- DPDP: For any personal data collection.\n"
            "- RBI: For financial security and logging.\n\n"
            "Output must be a JSON object with these keys:\n"
            "- steps: List[str]\n"
            "- compliance_requirements: List[str] (be specific about rule categories like 'UPI' or 'GST')\n"
            "- tech_stack: str\n"
            "- estimated_complexity: str"
        )

    async def create_plan(self, state: AgentState) -> Dict[str, Any]:
        """
        Generates a structured plan with Indian compliance focus.
        """
        user_prompt = f"User Task: {state['user_task']}"
        
        try:
            response_text = await self.client.generate(
                prompt=f"{self.system_prompt}\n\n{user_prompt}",
                model=MODEL_NAME
            )
            
            clean_json = self._extract_json(response_text)
            plan_data = json.loads(clean_json)
            return plan_data
            
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            return {
                "steps": ["Step 1: Research", "Step 2: Basic Setup"],
                "compliance_requirements": ["General Data Protection"],
                "tech_stack": "FastAPI + Python",
                "estimated_complexity": "medium"
            }

    def _extract_json(self, text: str) -> str:
        """Helper to find JSON block in LLM output."""
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        return text.strip()

async def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    The node function for the Planner agent.
    """
    client = OllamaClient()
    planner = PlannerAgent(client)
    
    plan = await planner.create_plan(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "Planner",
        "message": f"Generated plan with {len(plan.get('steps', []))} steps. Complexity: {plan.get('estimated_complexity')}"
    }
    
    # Map compliance requirements to the checklist structure
    checklist = [{"area": req, "status": "pending"} for req in plan.get("compliance_requirements", [])]
    
    return {
        "current_node": "planner",
        "plan": plan,
        "compliance_checklist": checklist,
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Plan Generated", "details": plan}]
    }
