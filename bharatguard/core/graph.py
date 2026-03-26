from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from bharatguard.core.state import AgentState
from bharatguard.agents import (
    supervisor_node, 
    planner_node, 
    coder_node, 
    tester_node, 
    reporter_node,
    compliance_guardian_node
)

def create_graph():
    """
    Constructs the Phase 3 LangGraph for BharatGuard.
    Includes the Compliance Guardian loop.
    """
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("compliance_guardian", compliance_guardian_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("reporter", reporter_node)

    # 2. Supervisor Routing
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state.get("next_agent", "reporter"),
        {
            "planner": "planner",
            "coder": "coder",
            "tester": "tester",
            "reporter": "reporter"
        }
    )

    # 3. Compliance Loop Logic
    # After coder, always go to compliance guardian
    workflow.add_edge("coder", "compliance_guardian")

    # After compliance guardian, decide: tester or back to coder
    def route_after_compliance(state: AgentState):
        score = state.get("compliance_score", 0)
        loop_count = state.get("compliance_loop_count", 0)
        
        if score >= 75 or loop_count >= 3:
            return "tester"
        return "coder"

    workflow.add_conditional_edges(
        "compliance_guardian",
        route_after_compliance,
        {
            "tester": "tester",
            "coder": "coder"
        }
    )

    # 4. Standard Edges back to Supervisor
    workflow.add_edge("planner", "supervisor")
    workflow.add_edge("tester", "supervisor")
    workflow.add_edge("reporter", END)

    # 5. Set Entry Point
    workflow.set_entry_point("supervisor")

    # 6. Setup Persistence
    memory = SqliteSaver.from_conn_string(":memory:")
    
    return workflow.compile(checkpointer=memory)

app_graph = create_graph()
