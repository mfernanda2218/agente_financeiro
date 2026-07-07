import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories - ajustado para funcionar quando executado de dentro da pasta src
BASE_DIR = Path(__file__).resolve().parent.parent  # Agora sobe duas pastas: src/ -> raiz do projeto
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# File paths
TRANSACOES_FILE = DATA_DIR / "transacoes.csv"
PERFIL_FILE = DATA_DIR / "perfil_investidor.json"
PRODUTOS_FILE = DATA_DIR / "produtos_financeiros.json"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model config
LLM_MODEL = "llama-3.1-8b-instant"