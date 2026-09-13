import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Providers: openai / gemini / ollama
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434/v1"
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")

TOP_K = int(os.getenv("TOP_K", "5"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "12"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

KNOWLEDGE_DIR = ROOT / "knowledge"
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "chatbot.sqlite3"
INDEX_PATH = DATA_DIR / "tfidf_index.pkl"

DATA_DIR.mkdir(exist_ok=True)
