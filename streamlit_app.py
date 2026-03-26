import streamlit as st
import asyncio
import os
import json
import uuid
from datetime import datetime
from bharatguard.main import run_bharatguard
from bharatguard.demo_tasks import DEMO_TASKS
from bharatguard.utils.evolution_handler import EvolutionHandler
from bharatguard.core.graph import app_graph
from bharatguard.core.state import create_initial_state

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="BharatGuard Agent", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #1a237e; color: white; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .agent-log { font-family: 'Courier New', Courier, monospace; font-size: 0.85rem; color: #2c3e50; }
    .sidebar .sidebar-content { background-color: #1a237e; color: white; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'evolution_handler' not in st.session_state:
    st.session_state.evolution_handler = EvolutionHandler()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'last_run' not in st.session_state:
    st.session_state.last_run = None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/officel/80/000000/security-shield.png", width=80)
    st.title("BharatGuard Agent")
    st.write("Demo Prototype of **MetaForge**")
    st.divider()
    
    st.subheader("About")
    st.info("BharatGuard is a self-evolving AI agent designed to build compliant IndiaStack applications. It integrates GST, UPI, Aadhaar, and DPDP regulations autonomously.")
    
    st.subheader("Demo Showcase")
    task_selected = st.selectbox("Select a Demo Task", [t['title'] for t in DEMO_TASKS])
    selected_task_desc = next(t['description'] for t in DEMO_TASKS if t['title'] == task_selected)
    
    st.write(f"**Description:** {selected_task_desc}")
    if st.button("Load Task"):
        st.session_state.task_input = selected_task_desc
    
    st.divider()
    st.caption("March 2026 | Fully Local | Not for Prod Legal Use")

# --- MAIN UI ---
st.title("🛡️ BharatGuard Agent — IndiaStack Compliance AI")
st.markdown("##### *Build regulatory-ready apps in seconds*")

# --- INPUT SECTION ---
col1, col2 = st.columns([4, 1])
with col1:
    task_input = st.text_area("Enter your application requirements", 
                              value=st.session_state.get('task_input', ""),
                              placeholder="e.g., Create a secure UPI payment system...",
                              height=100)
with col2:
    st.write("Voice Input")
    if st.button("🎙️ Whisper Input"):
        st.warning("Voice (Whisper-tiny) simulation: Listening...")
        st.success("Detected: 'Generate a GST compliant store login'")
        task_input = "Generate a GST compliant store login"

if st.button("🚀 Generate Compliant App", type="primary"):
    if not task_input:
        st.error("Please enter a task description.")
    else:
        # Reset logs for new run
        st.session_state.logs = []
        
        with st.status("BharatGuard Orchestrating Agents...", expanded=True) as status:
            # Graph execution loop
            initial_state = create_initial_state(task_input)
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}
            
            # Simple async wrapper for Streamlit
            async def run_and_log():
                async for event in app_graph.astream(initial_state, config):
                    for node_name, state_update in event.items():
                        msg = f"**{node_name.upper()}** completed."
                        if "agent_logs" in state_update:
                            msg = state_update["agent_logs"][-1]["message"]
                        
                        st.write(f"Agent: `{node_name}` | {msg}")
                        st.session_state.logs.append({"node": node_name, "message": msg})
                        
                        # Store last final state update
                        st.session_state.last_run = state_update

            asyncio.run(run_and_log())
            status.update(label="Audit Certificate Generated!", state="complete", expanded=False)
        
        # Save to Evolution History
        if st.session_state.last_run:
            score = st.session_state.last_run.get("compliance_score", 0)
            details = st.session_state.last_run.get("compliance_details", [])
            st.session_state.evolution_handler.save_run(task_input, score, details)

# --- RESULTS SECTION ---
if st.session_state.last_run:
    st.divider()
    res_col1, res_col2, res_col3 = st.columns(3)
    
    score = st.session_state.last_run.get("compliance_score", 0)
    with res_col1:
        st.metric("Compliance Score", f"{score}%", delta="Phase 3 Engine")
        
    with res_col2:
        files_count = len(st.session_state.last_run.get("generated_code", {}).get("files", []))
        st.metric("Files Generated", files_count, delta="Clean Architecture")
        
    with res_col3:
        loops = st.session_state.last_run.get("compliance_loop_count", 0)
        st.metric("Audit Loops", loops, delta="Self-Correction")

    tab1, tab2, tab3 = st.tabs(["📝 Audit Summary", "💻 Code Preview", "📜 Agent Evolution"])
    
    with tab1:
        st.subheader("Compliance Guardian Findings")
        for detail in st.session_state.last_run.get("compliance_details", []):
            status = "✅" if detail['status'] == 'passed' else "❌"
            st.write(f"{status} **[{detail['category']}]** {detail['description']}")
            
        if st.session_state.last_run.get("pdf_path"):
            pdf_path = st.session_state.last_run.get("pdf_path")
            st.success(f"Audit Certificate Ready: `{pdf_path}`")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download Compliance Certificate (PDF)", f, file_name=os.path.basename(pdf_path))

    with tab2:
        st.subheader("Generated Source Code")
        backend = st.session_state.last_run.get("generated_code", {}).get("backend_code", "# N/A")
        st.code(backend, language="python", line_numbers=True)

    with tab3:
        st.subheader("System Multi-Run Evolution")
        history = st.session_state.evolution_handler.get_history()
        if history:
            st.line_chart([h['score'] for h in reversed(history)])
            st.write("**Evolution Log:**")
            for h in history[:5]:
                st.write(f"- {h['timestamp'][:16]} | Score: {h['score']}% | Task: {h['task'][:50]}")
        else:
            st.write("No history available yet. Run more tasks to trigger evolution.")
