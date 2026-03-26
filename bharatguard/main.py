import asyncio
import logging
import uuid
import os
from bharatguard.core.graph import app_graph
from bharatguard.core.state import create_initial_state

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def run_bharatguard(task: str):
    """
    Executes the BharatGuard Agent workflow for a given task.
    In Phase 4, it generates a professional PDF audit certificate.
    """
    print(f"\n--- [BHARATGUARD PHASE 4: AUDIT IN PROGRESS] ---")
    print(f"Task: {task}")
    
    initial_state = create_initial_state(task)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    final_output_state = None
    
    try:
        async for event in app_graph.astream(initial_state, config):
            for node_name, state_update in event.items():
                print(f"[{node_name.upper()}] completed execution.")
                
                if "agent_logs" in state_update:
                    latest_log = state_update["agent_logs"][-1]
                    print(f"  > {latest_log['message']}")

                # Track the updates to return the final version
                final_output_state = state_update

        # Final Summary Feedback
        print("\n" + "="*50)
        print("          BHARATGUARD AUDIT COMPLETE")
        print("="*50)
        
        # Note: final_output_state from astream is only the partial update of the last node
        # To get the full final state, we'd need to accumulate or query the checkpointer
        # But since reporter node finishes the task, it should contain the path.
        if final_output_state and "pdf_path" in final_output_state:
            print(f"REPORT SAVED AT: {final_output_state['pdf_path']}")
            print(f"Audit Status: {'SUCCESS' if 'SUCCESS' in final_output_state.get('final_summary', '') else 'CONDITIONALLY APPROVED'}")
        
        print("="*50)
        
        return final_output_state

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return None

if __name__ == "__main__":
    sample_task = "Implement an Aadhaar-linked E-KYC flow for a digital locker in Uttar Pradesh."
    
    print("BharatGuard Phase 4 Prototype Initializing...")
    asyncio.run(run_bharatguard(sample_task))
