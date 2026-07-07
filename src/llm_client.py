from groq import Groq
from src import config
import httpx

def get_system_prompt():
    return """Você é um Consultor Financeiro Inteligente altamente capacitado.
Seu objetivo é analisar transações, perfil de risco e sugerir produtos financeiros adequados.

REGRAS:
1. Responda sempre em Markdown bem formatado.
2. Use tabelas ou listas com marcadores para facilitar a leitura de dados ou recomendações.
3. Se recomendar um produto, justifique por que ele se alinha ao perfil de risco do investidor.
4. Não invente produtos que não estejam na lista de produtos disponíveis fornecida.
5. Se não souber responder ou se a pergunta fugir do escopo financeiro, avise educadamente que sua especialidade é finanças pessoais e investimentos."""

def build_context(perfil, transacoes_df, produtos):
    contexto = f"""
--- DADOS DO CLIENTE ---
Perfil do Investidor:
{perfil}

Últimas Transações (amostra):
{transacoes_df.head(20).to_string() if not transacoes_df.empty else "Nenhuma transação encontrada."}

Produtos Financeiros Disponíveis no momento:
{produtos}
------------------------
"""
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
                    # Remove proxies do timeout
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
        # Apenas passamos as mensagens que não são de sistema para não poluir
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