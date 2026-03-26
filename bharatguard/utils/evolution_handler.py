import os
import json
import chromadb
from datetime import datetime
from bharatguard.config import RESULTS_DB_PATH, PROMPT_EVOLUTION_PATH

class EvolutionHandler:
    """
    Handles memory and self-improvement for BharatGuard.
    Saves run results to ChromaDB and manages prompt evolution.
    """
    
    def __init__(self):
        self.client = chromadb.PersistentClient(path=RESULTS_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="audit_history")
        self._ensure_prompt_exists()

    def _ensure_prompt_exists(self):
        if not os.path.exists(PROMPT_EVOLUTION_PATH):
            default_prompt = (
                "You are the BharatGuard Planner. Your role is to design technical architectures "
                "that are compliant with Indian regulations."
            )
            with open(PROMPT_EVOLUTION_PATH, "w") as f:
                f.write(default_prompt)

    def save_run(self, task: str, score: float, details: list):
        """Saves a single execution run to the vector database."""
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.collection.add(
            documents=[task],
            metadatas=[{"score": score, "timestamp": datetime.now().isoformat(), "details_count": len(details)}],
            ids=[run_id]
        )
        self._check_and_evolve()

    def get_history(self):
        """Retrieves recent run history."""
        results = self.collection.get()
        history = []
        for i in range(len(results['ids'])):
            history.append({
                "task": results['documents'][i],
                "score": results['metadatas'][i]['score'],
                "timestamp": results['metadatas'][i]['timestamp']
            })
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)

    def _check_and_evolve(self):
        """
        Simple evolution logic: every 3 runs, it 'refines' the prompt.
        In a real scenario, this would involve LLM self-critique.
        """
        results = self.collection.get()
        if len(results['ids']) > 0 and len(results['ids']) % 3 == 0:
            avg_score = sum(m['score'] for m in results['metadatas']) / len(results['ids'])
            with open(PROMPT_EVOLUTION_PATH, "a") as f:
                f.write(f"\n# Self-Improvement Note: Average Compliance at {avg_score}%. Focus on stricter UPI/RBI validation.")

    def get_current_planner_prompt(self) -> str:
        with open(PROMPT_EVOLUTION_PATH, "r") as f:
            return f.read()
