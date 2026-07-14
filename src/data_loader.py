import pandas as pd
import json
from src.components import config  # Mantém assim, mas ajuste abaixo

def load_transacoes(file_path=None):
    """Carrega as transações do CSV."""
    path_to_load = file_path if file_path else config.TRANSACOES_FILE
    try:
        df = pd.read_csv(path_to_load)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["data", "valor", "categoria", "descricao"])
    except Exception as e:
        raise Exception(f"Erro ao carregar transações: {str(e)}")

def load_perfil_investidor():
    """Carrega o perfil do investidor do JSON."""
    try:
        with open(config.PERFIL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise Exception(f"Erro ao carregar perfil: {str(e)}")

def load_produtos_financeiros():
    """Carrega os produtos financeiros disponíveis do JSON."""
    try:
        with open(config.PRODUTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise Exception(f"Erro ao carregar produtos: {str(e)}")
        