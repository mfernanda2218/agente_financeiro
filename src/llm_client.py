from groq import Groq
from src import config

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

def chat_completion(messages, context_str=None):
    """
    Envia o histórico de mensagens para a API do Groq.
    Injeta o contexto na mensagem do sistema caso context_str seja fornecido.
    """
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY não configurada.")
        
    client = Groq(api_key=config.GROQ_API_KEY)
    
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
            
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=api_messages
    )
    
    return response.choices[0].message.content
