import logging
from datetime import datetime
from typing import Dict, Any
from bharatguard.core.state import AgentState, AgentLog
from bharatguard.output.pdf_generator import CompliancePDFGenerator

logger = logging.getLogger(__name__)

class ReporterAgent:
    """
    The final agent in the workflow.
    Generates the audit certificate and summarizes the project status.
    """
    
    def __init__(self):
        self.pdf_gen = CompliancePDFGenerator()

    async def finalize_report(self, state: AgentState) -> Dict[str, Any]:
        """
        Triggers the PDF generation and creates a final summary.
        """
        try:
            # Generate the professional PDF audit certificate
            pdf_path = self.pdf_gen.generate_report(state)
            
            # Create a user-friendly summary
            status = "APPROVED" if state.get("compliance_score", 0) >= 75 else "CONDITIONALLY APPROVED"
            summary = (
                f"BharatGuard Phase 4 Audit Complete.\n"
                f"Status: {status}\n"
                f"Compliance Score: {state.get('compliance_score', 0)}%\n"
                f"Generated Audit Certificate: {pdf_path}"
            )
            
            return {
                "pdf_path": pdf_path,
                "final_summary": summary,
                "current_node": "reporter"
            }
            
        except Exception as e:
            logger.error(f"Reporter failed to generate audit certificate: {e}")
            return {
                "final_summary": f"Audit complete, but PDF generation failed: {str(e)}",
                "current_node": "reporter"
            }

async def reporter_node(state: AgentState) -> Dict[str, Any]:
    """
    The node functional wrapper for the Reporter agent.
    """
    reporter = ReporterAgent()
    result = await reporter.finalize_report(state)
    
    log_entry: AgentLog = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": "Reporter",
        "message": "Compliance Audit Certificate generated successfully."
    }
    
    return {
        "pdf_path": result.get("pdf_path", ""),
        "final_summary": result.get("final_summary", ""),
        "agent_logs": [log_entry],
        "evolution_log": [{"event": "Report Generated", "details": result.get("pdf_path")}]
    }
