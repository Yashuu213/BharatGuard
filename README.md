# 🛡️ BharatGuard Agent — IndiaStack Compliance AI
**Demo Prototype of MetaForge | Fully Local Deployment | March 2026**

BharatGuard is a specialized agentic framework designed to build secure, regulatory-compliant applications for the Indian market. It autonomously integrates GST, UPI, Aadhaar, DPDP, and RBI guidelines into generated source code.

---

## 🚀 Key Features

- **Hierarchical Multi-Agent System**: Supervisor-led orchestration of Planner, Coder, Compliance Guardian, Tester, and Reporter agents.
- **Compliance Guardian Engine**: Real-time audit against 25+ Indian regulatory rules with weighted scoring.
- **Self-Improving Intelligence**: Every 3 runs, BharatGuard analyzes success metrics and evolves its internal planning strategies via ChromaDB.
- **Auditor-Ready Reports**: Generates professional PDF Compliance Certificates with full evidence logs.
- **Voice Intelligence**: Support for multilingual task input (English/Hindi) using Whisper.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- **Ollama**: Install and pull the required model.
  ```bash
  ollama pull qwen3:4b
  ```
- **Python**: Recommending Python 3.10 or higher.

### 2. Configuration
- Clone this repository.
- Install dependencies:
  ```bash
  pip install -r bharatguard/requirements.txt
  ```

### 3. Running the Prototype
#### **CLI Mode** (Core System)
```bash
python -m bharatguard.main
```

#### **Visual Dashboard** (Recommended for Showcases)
```bash
streamlit run streamlit_app.py
```

---

## 📊 Phase Summary
- **Phase 1**: Folder structure, State definitions, LangGraph skeleton.
- **Phase 2**: Hierarchical agent logic and routing.
- **Phase 3**: Compliance Guardian Engine (25+ rules, weighted scoring).
- **Phase 4**: Professional PDF Compliance Certificate generation.
- **Phase 5**: Streamlit Dashboard & Self-Improvement via ChromaDB.

---

## 📜 60-Second Demo Script (MetaForge Showcase)

1.  **[0-10s]**: "This is BharatGuard, a demo prototype of MetaForge. It builds software that is compliant by design for the Indian market."
2.  **[10-30s]**: "I'll select a Jaipur Handicraft Store task. Watch as the agents—Supervisor, Planner, and Coder—collaborate locally. The Compliance Guardian is auditing every line of code against RBI and GST guidelines."
3.  **[30-50s]**: "The audit is complete. We have an 88% compliance score. You can see the specific GST and UPI rules it validated. Now, I'm downloading the professional Compliance Certificate generate by the Reporter Agent."
4.  **[50-60s]**: "BharatGuard is self-evolving. It has recorded this run in its local memory, improving its performance for future financial audits. Fully local, fully private, and regulatory-ready."

---

## ⚠️ Disclaimer
This project is a **demo prototype** created by the MetaForge team. It is not intended for production-grade legal work. All regulatory rules are simulations based on 2026 guidelines.
