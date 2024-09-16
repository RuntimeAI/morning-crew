import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

# MindsDB Configuration
MINDSDB_API_KEY = os.getenv("MINDSDB_API_KEY")
MINDSDB_NAME = os.getenv("MINDSDB_NAME")

# POSTGRES Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


# LLM Model Configuration
MODEL_MAPPING = {
    'S1': 'gpt-4o-mini', # Small model - replaceable with Gemini-Flash
    'G1': 'gpt-4o-mini', # General purpose model - replaceable with Gemini-1.5-Pro
    'P1': 'gpt-4o', # Large powerful model - replaceable with Gemini-1.5-Pro
    'L1': 'gpt-4-mini', # Long context model - replaceable with Claude-3.5-Sonnet
    'E1': 'text-embedding-ada-002' # Embedding model
}

# Default LLM Configuration
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL = 'G1'

# Runtime Configuration
MAX_ROLES_PER_RUNTIME = 10
MAX_TASKS_PER_RUNTIME = 100

# Cache Configuration
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
MAX_CACHE_ITEMS = 1000

# Redis Configuration (for LLMCache)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
if REDIS_PASSWORD == "None":
    REDIS_PASSWORD = None

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Project Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROLES_DIR = os.path.join(PROJECT_ROOT, "roles")
SKILLSETS_DIR = os.path.join(PROJECT_ROOT, "skillsets")

# Ensure necessary directories exist
os.makedirs(CACHE_DIR, exist_ok=True)