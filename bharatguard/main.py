import asyncio
import logging
import uuid
from bharatguard.core.graph import app_graph
from bharatguard.core.state import create_initial_state

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def run_bharatguard(task: str):
    """
    Executes the BharatGuard Agent workflow for a given task.
    Initializes the state, runs the LangGraph, and returns the final state.
    """
    print(f"\n--- [BHARATGUARD PHASE 2: {task.upper()}] ---")
    
    # Initialize the default state with the user task
    initial_state = create_initial_state(task)
    
    # Config for LangGraph (thread management and checkpointer)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    try:
        # Execute the LangGraph workflow asynchronously
        async for event in app_graph.astream(initial_state, config):
            for node_name, state_update in event.items():
                print(f"[{node_name.upper()}] completed.")
                
                # Print logs from the agent if available
                if "agent_logs" in state_update:
                    latest_log = state_update["agent_logs"][-1]
                    print(f"Log: {latest_log['message']}")

        # Return the final state after the 'reporter' node finishes
        # To get the final state, we can use get_state if needed, 
        # but astream yields the updates.
        return "Task Completed Successfully"

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return f"Execution failed: {str(e)}"

if __name__ == "__main__":
    # Sample task for Phase 2 Demo: A GST-compliant payment integration
    sample_task = "Create a GST-compliant checkout system for a handicraft store in Rajasthan."
    
    print("Starting BharatGuard Phase 2 Prototype...")
    asyncio.run(run_bharatguard(sample_task))
    print("\n--- [PHASE 2 EXECUTION FINISHED] ---")
