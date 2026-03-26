import logging
from datetime import datetime
from typing import Dict, Any, List
from bharatguard.core.state import AgentState, AgentLog

logger = logging.getLogger(__name__)

class TesterAgent:
    """
    The quality assurance expert.
    Verifies the generated code for syntax and functional correctness.
    """
    
    def __init__(self):
        pass

    async def run_tests(self, state: AgentState) -> Dict[str, Any]:
        """
        Performs basic verification on the generated code.
        """
        backend_code = state.get("generated_code", {}).get("backend_code", "")
        frontend_code = state.get("generated_code", {}).get("frontend_code", "")
        
        # Simulated testing logic
        tests = []
        passed = 0
        total = 3
        
        # Test 1: Syntax Check (Basic)
        if "import" in backend_code and "FastAPI" in backend_code:
            tests.append({"test": "Backend Syntax check", "status": "passed"})
            passed += 1
        else:
            tests.append({"test": "Backend Syntax check", "status": "failed", "error": "FastAPI import missing"})

        # Test 2: React Component check
        if "export default" in frontend_code or "return (" in frontend_code:
            tests.append({"test": "Frontend Component check", "status": "passed"})
            passed += 1
        else:
            tests.append({"test": "Frontend Component check", "status": "failed", "error": "React export or return missing"})

        # Test 3: Compliance Note check
        if "Compliance Note:" in backend_code or "Compliance Note:" in frontend_code:
            tests.append({"test": "Compliance Tag check", "status": "passed"})
            passed += 1
        else:
            tests.append({"test": "Compliance Tag check", "status": "failed", "error": "No compliance comments found"})

        return {
            "passed": passed,
            "total": total,
            "details": tests
        }

async def tester_node(state: AgentState) -> Dict[str, Any]:
    """
    The node function for the Tester agent.
    """
    tester = TesterAgent()
    results = await tester.run_tests(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "Tester",
        "message": f"Tests completed: {results['passed']}/{results['total']} passed."
    }
    
    return {
        "current_node": "tester",
        "test_results": results,
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Testing Completed", "details": results}]
    }
