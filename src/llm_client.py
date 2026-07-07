from groq import Groq
from src import config
import httpx
from src.db_indicadores import IndicadoresDatabase
import logging

logger = logging.getLogger(__name__)

def get_system_prompt():
    """Retorna o prompt do sistema sem conexão com banco."""
    return """Você é um Consultor Financeiro Inteligente altamente capacitado.
Seu objetivo é analisar transações, perfil de risco e sugerir produtos financeiros adequados.

REGRAS:
1. Responda sempre em Markdown bem formatado.
2. Use tabelas ou listas com marcadores para facilitar a leitura de dados ou recomendações.
3. Se recomendar um produto, justifique por que ele se alinha ao perfil de risco do investidor.
4. Não invente produtos que não estejam na lista de produtos disponíveis fornecida.
5. Se não souber responder ou se a pergunta fugir do escopo financeiro, avise educadamente que sua especialidade é finanças pessoais e investimentos."""

def analisar_impacto_indicadores(indicadores, perfil):
    """Analisa o impacto dos indicadores nas recomendações."""
    analise = []
    
    if indicadores and indicadores.get('selic') is not None:
        selic = indicadores['selic']
        if selic > 12:
            analise.append(f"• SELIC em {selic:.2f}%: Momento favorável para renda fixa. Considere CDB, Tesouro Selic e LCI/LCA.")
        elif selic < 8:
            analise.append(f"• SELIC em {selic:.2f}%: Renda fixa menos atrativa. Avalie maior exposição a ações e FIIs.")
        else:
            analise.append(f"• SELIC em {selic:.2f}%: Cenário neutro para investimentos.")
    
    if indicadores and indicadores.get('ipca') is not None:
        ipca = indicadores['ipca']
        if ipca > 0.5:  # IPCA mensal
            analise.append(f"• IPCA em {ipca:.2f}%: Inflação elevada. Busque ativos com proteção contra perda de poder de compra.")
    
    return "\n".join(analise)

def build_context(perfil, transacoes_df, produtos):
    """Constrói o contexto incluindo indicadores econômicos do banco."""
    
    # Contexto básico
    contexto = f"""
--- DADOS DO CLIENTE ---
Perfil do Investidor:
{perfil}

Últimas Transações (amostra):
{transacoes_df.head(20).to_string() if not transacoes_df.empty else "Nenhuma transação encontrada."}

Produtos Financeiros Disponíveis no momento:
{produtos}
"""
    
    # Adiciona indicadores econômicos do banco
    try:
        db = IndicadoresDatabase()
        indicadores = db.get_todos_indicadores_recentes()
        
        if indicadores and any([indicadores.get('selic'), indicadores.get('ipca')]):
            contexto += "\n--- INDICADORES ECONÔMICOS ATUAIS (Banco de Dados) ---\n"
            if indicadores.get('selic') is not None:
                contexto += f"Taxa Selic: {indicadores['selic']:.2f}% ao ano\n"
                contexto += f"Data Selic: {indicadores.get('selic_data', 'N/A')}\n"
            if indicadores.get('ipca') is not None:
                contexto += f"IPCA Mensal: {indicadores['ipca']:.2f}%\n"
                contexto += f"Data IPCA: {indicadores.get('ipca_data', 'N/A')}\n"
            contexto += f"Data da consulta: {indicadores.get('data_consulta', 'N/A')}\n"
            contexto += "---------------------------------------\n"
            
            # Adicionar análise de impacto
            analise = analisar_impacto_indicadores(indicadores, perfil)
            if analise:
                contexto += "\n--- ANÁLISE DE IMPACTO DOS INDICADORES ---\n"
                contexto += analise
        else:
            contexto += "\n(Indicadores econômicos: dados não disponíveis no momento)\n"
                
    except Exception as e:
        logger.warning(f"Não foi possível carregar indicadores econômicos: {e}")
        contexto += "\n(Indicadores econômicos não disponíveis no momento)\n"
    
    return contexto

def create_groq_client():
    """Cria um cliente Groq com compatibilidade entre versões."""
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY não configurada.")
    
    try:
        # Tentativa 1: Cliente padrão
        client = Groq(api_key=config.GROQ_API_KEY)
        return client
    except TypeError as e:
        if "proxies" in str(e):
            try:
                # Tentativa 2: Criar cliente com timeout personalizado
                client = Groq(
                    api_key=config.GROQ_API_KEY,
                    timeout=60.0,
                    max_retries=2
                )
                return client
            except:
                try:
                    # Tentativa 3: Usar httpx client personalizado
                    http_client = httpx.Client(
                        timeout=httpx.Timeout(60.0),
                        follow_redirects=True
                    )
                    client = Groq(
                        api_key=config.GROQ_API_KEY,
                        http_client=http_client
                    )
                    return client
                except Exception as e2:
                    raise Exception(f"Falha ao criar cliente Groq: {str(e2)}")
        else:
            raise e

def chat_completion(messages, context_str=None):
    """
    Envia o histórico de mensagens para a API do Groq.
    Injeta o contexto na mensagem do sistema caso context_str seja fornecido.
    """
    try:
        client = create_groq_client()
    except Exception as e:
        raise Exception(f"Erro ao inicializar cliente Groq: {str(e)}")
    
    # Preparar a mensagem do sistema com ou sem contexto
    system_content = get_system_prompt()
    if context_str:
        system_content += f"\n\nBaseie-se nestes dados para suas respostas:\n{context_str}"
        
    api_messages = [{"role": "system", "content": system_content}]
    
    # Adicionar as mensagens do usuário e do assistente (histórico)
    for msg in messages:
        if msg["role"] in ["user", "assistant"]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=api_messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Erro na comunicação com a API Groq: {str(e)}")