import logging
from datetime import datetime
from typing import Dict, Any, List
from bharatguard.core.state import AgentState, AgentLog
from bharatguard.compliance.rules import ALL_RULES
from bharatguard.compliance.scorer import ComplianceScorer

logger = logging.getLogger(__name__)

class ComplianceGuardianAgent:
    """
    The regulatory expert.
    Audits the generated code against 25+ Indian compliance rules.
    """
    
    def __init__(self):
        pass

    async def audit_code(self, state: AgentState) -> Dict[str, Any]:
        """
        Runs the rule engine against the generated code.
        """
        backend_code = state.get("generated_code", {}).get("backend_code", "")
        frontend_code = state.get("generated_code", {}).get("frontend_code", "")
        full_code = f"{backend_code}\n\n{frontend_code}"
        
        results = []
        fix_suggestions = []
        
        # Determine scope based on plan
        scope = [req.upper() for req in state.get("plan", {}).get("compliance_requirements", [])]
        
        for rule in ALL_RULES:
            # Only check rules in scope, or all rules if scope is not defined
            if not scope or any(s in rule.category.upper() for s in scope) or rule.category == "RBI":
                passed = rule.check_fn(full_code)
                results.append({
                    "rule_id": rule.rule_id,
                    "category": rule.category,
                    "description": rule.description,
                    "status": "passed" if passed else "failed",
                    "severity": rule.severity
                })
                
                if not passed:
                    fix_suggestions.append(f"[{rule.category}] {rule.fix_suggestion}")

        # Calculate weighted score
        score, category_scores = ComplianceScorer.calculate_score(results)
        
        return {
            "score": score,
            "details": results,
            "fix_suggestions": fix_suggestions,
            "category_scores": category_scores
        }

async def compliance_guardian_node(state: AgentState) -> Dict[str, Any]:
    """
    The node function for the Compliance Guardian.
    """
    guardian = ComplianceGuardianAgent()
    audit_results = await guardian.audit_code(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "ComplianceGuardian",
        "message": f"Audit complete. Score: {audit_results['score']}%."
    }
    
    # Update loop count for routing
    new_loop_count = state.get("compliance_loop_count", 0) + 1
    
    return {
        "current_node": "compliance_guardian",
        "compliance_score": audit_results["score"],
        "compliance_details": audit_results["details"],
        "fix_suggestions": audit_results["fix_suggestions"],
        "compliance_loop_count": new_loop_count,
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Compliance Audit", "details": audit_results["score"]}]
    }
