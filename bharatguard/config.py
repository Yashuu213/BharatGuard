import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:4b")  # qwen3:4b or phi-4-mini
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))

# API URLs
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "chroma")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH", "./output")

# Ensure necessary directories exist
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(GIT_REPO_PATH, exist_ok=True)
