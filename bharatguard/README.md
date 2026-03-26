# BharatGuard Agent (Demo Prototype of MetaForge)

## Phase 1 Status: Foundation Ready
This repository contains the complete, production-ready foundation for the BharatGuard Agent. It includes the LangGraph skeleton, state definitions, and modular agent structures.

## Setup Instructions

### Prerequisites
1.  **Ollama**: Install and pull the required model.
    ```bash
    ollama pull qwen3:4b
    ```
2.  **Conda/Python**: Recommending Python 3.10+.

### Installation
1.  Clone the repository and navigate to the root directory.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### How to Run
To run the prototype skeleton and verify the graph flow:
```bash
python -m bharatguard.main
```

## Folder Structure
- `/bharatguard/`: Source code.
  - `agents/`: AI agent definitions (Supervisor, Planner, Coder, Tester).
  - `compliance/`: Legal and technical compliance rules.
  - `core/`: State management and graph workflow logic.
  - `utils/`: Reusable utilities like Ollama and Git clients.
- `data/`: Local storage for ChromaDB and mocks.
- `output/`: Directory for generated code and reports.

## What is Ready
- [x] Hierarchical folder structure.
- [x] State definition via `TypedDict`.
- [x] LangGraph `StateGraph` skeleton.
- [x] Ollama client with streaming support.
- [x] Basic persistence via `SqliteSaver`.
- [x] Entry point for prototype execution.
