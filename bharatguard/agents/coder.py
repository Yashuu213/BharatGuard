import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from bharatguard.core.state import AgentState, AgentLog
from bharatguard.utils.ollama_client import OllamaClient
from bharatguard.config import MODEL_NAME

logger = logging.getLogger(__name__)

class CoderAgent:
    """
    The developer of the system.
    Generates high-quality code based on the technical plan.
    """
    
    def __init__(self, client: OllamaClient):
        self.client = client

    async def generate_code(self, state: AgentState) -> Dict[str, Any]:
        """
        Generates backend and frontend code using Ollama.
        """
        system_prompt = (
            "You are the BharatGuard Coder. Your task is to generate clean, production-ready code.\n\n"
            "Requirements:\n"
            "- Backend: FastAPI (Python)\n"
            "- Frontend: React (JSX)\n"
            "- Integration: Full setup for the provided plan.\n"
            "- Compliance: Add comments like '# Compliance Note: [Area]' where relevant.\n\n"
            "Output must be a JSON object with these keys:\n"
            "- backend_code: Complete main.py content\n"
            "- frontend_code: Complete App.jsx content\n"
            "- files: List of filenames created"
        )
        
        plan_str = json.dumps(state['plan'], indent=2)
        user_prompt = f"Technical Plan:\n{plan_str}\n\nGenerate the complete codebase."
        
        try:
            response_text = await self.client.generate(
                prompt=f"{system_prompt}\n\n{user_prompt}",
                model=MODEL_NAME
            )
            
            clean_json = self._extract_json(response_text)
            code_data = json.loads(clean_json)
            return code_data
            
        except Exception as e:
            logger.error(f"Coder failed: {e}")
            return {
                "backend_code": "# Error generating backend",
                "frontend_code": "// Error generating frontend",
                "files": ["main.py", "App.jsx"]
            }

    def _extract_json(self, text: str) -> str:
        """Helper to find JSON block in LLM output."""
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        return text.strip()

async def coder_node(state: AgentState) -> Dict[str, Any]:
    """
    The node function for the Coder agent.
    """
    client = OllamaClient()
    coder = CoderAgent(client)
    
    code_data = await coder.generate_code(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "Coder",
        "message": f"Generated code for {len(code_data.get('files', []))} files."
    }
    
    return {
        "current_node": "coder",
        "generated_code": code_data,
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Code Generated", "details": code_data.get("files")}]
    }
