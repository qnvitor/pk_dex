"""Configuração centralizada do projeto."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

# Diretórios base
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# PokéAPI
POKEAPI_BASE_URL = os.getenv('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')
POKEAPI_CACHE_TTL = int(os.getenv('POKEAPI_CACHE_TTL', '86400'))

# Database
DB_PATH = os.getenv('DB_PATH', str(DATA_DIR / 'pokemon_db.sqlite'))

# Ollama / RAG
DEFAULT_OLLAMA_MODEL = os.getenv('DEFAULT_OLLAMA_MODEL', 'llama3.2:3b')
AVAILABLE_MODELS = {
    "Llama 3.2 3B (Recomendado)": "llama3.2:3b",
    "Llama 3.2 1B (Mais Rápido)": "llama3.2:1b",
    "Phi-3 Mini": "phi3:mini",
    "Gemma 2B": "gemma:2b",
    "Mistral 7B": "mistral:7b"
}

# Vector Store
CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', str(DATA_DIR / 'chroma_db'))

# Embeddings
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
EMBEDDING_CACHE_DIR = str(MODELS_DIR / 'sentence_transformers')

# RAG
DEFAULT_N_CONTEXT_DOCS = int(os.getenv('DEFAULT_N_CONTEXT_DOCS', '3'))
DEFAULT_RAG_ENABLED = os.getenv('DEFAULT_RAG_ENABLED', 'true').lower() == 'true'

# Criar diretórios se não existirem
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
Path(CHROMA_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
