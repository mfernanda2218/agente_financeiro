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
5. Se não souber responder ou se a pergunta fugir do escopo financeiro, avise educadamente que sua especialidade é finanças pessoais e investimentos.
6. ATENÇÃO CRÍTICA AOS VALORES: Ao responder sobre investimentos, não confunda o 'Valor de Investimento' com a 'Rentabilidade' ou 'Retorno'. Garanta que os valores (X e Y) fornecidos pelo usuário ou extraídos dos produtos não sejam invertidos na sua resposta."""

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

# MODIFICAR: src/llm_client.py - build_context

def build_context(perfil, transacoes_df, produtos):
    """Constrói contexto enriquecido com dados do usuário"""
    contexto = []
    
    # 1. Perfil do usuário
    if perfil:
        contexto.append("=== PERFIL DO INVESTIDOR ===")
        contexto.append(f"Nome: {perfil.get('nome', 'N/A')}")
        contexto.append(f"Idade: {perfil.get('idade', 'N/A')}")
        contexto.append(f"Perfil de Risco: {perfil.get('perfil_risco', 'N/A')}")
        contexto.append(f"Renda Mensal: R$ {perfil.get('renda_mensal', 0):,.2f}")
        contexto.append(f"Patrimônio: R$ {perfil.get('patrimonio', 0):,.2f}")
        contexto.append(f"Objetivos: {', '.join(perfil.get('objetivos', []))}")
        contexto.append(f"Experiência: {perfil.get('experiencia_investimento', 'N/A')}")
        contexto.append("")
    
    # 2. Análise de transações
    if transacoes_df is not None and not transacoes_df.empty:
        contexto.append("=== RESUMO FINANCEIRO ===")
        
        total_gastos = transacoes_df[transacoes_df["valor"] < 0]["valor"].sum()
        total_ganhos = transacoes_df[transacoes_df["valor"] > 0]["valor"].sum()
        
        contexto.append(f"Total de Receitas: R$ {abs(total_ganhos):,.2f}")
        contexto.append(f"Total de Despesas: R$ {abs(total_gastos):,.2f}")
        contexto.append(f"Saldo no Período: R$ {total_ganhos + total_gastos:,.2f}")
        contexto.append(f"Nº de Transações: {len(transacoes_df)}")
        
        # Gastos por categoria
        if not transacoes_df[transacoes_df["valor"] < 0].empty:
            gastos_categoria = transacoes_df[transacoes_df["valor"] < 0].groupby("categoria")["valor"].sum().abs()
            contexto.append("\nGastos por Categoria:")
            for cat, val in gastos_categoria.items():
                contexto.append(f"  • {cat}: R$ {val:,.2f}")
        
        # Maiores gastos
        if not transacoes_df[transacoes_df["valor"] < 0].empty:
            top_gastos = transacoes_df[transacoes_df["valor"] < 0].nlargest(3, "valor")
            contexto.append("\nMaiores Gastos:")
            for _, row in top_gastos.iterrows():
                contexto.append(f"  • {row['descricao']}: R$ {abs(row['valor']):,.2f}")
        
        contexto.append("")
    
    # 3. Produtos financeiros
    if produtos:
        contexto.append("=== PRODUTOS FINANCEIROS DISPONÍVEIS ===")
        if isinstance(produtos, dict):
            for key, prod in produtos.items():
                if isinstance(prod, dict):
                    contexto.append(
                        f"• {prod.get('nome', key)}: "
                        f"{prod.get('tipo', 'N/A')} | "
                        f"Risco: {prod.get('risco', 'N/A')} | "
                        f"Rentabilidade: {prod.get('rentabilidade', 'N/A')} | "
                        f"Liquidez: {prod.get('liquidez', 'N/A')} | "
                        f"Mínimo: R$ {prod.get('minimo_investimento', 0):,.2f}"
                    )
        elif isinstance(produtos, list):
            for prod in produtos:
                if isinstance(prod, dict):
                    contexto.append(
                        f"• {prod.get('nome', 'Produto')}: "
                        f"{prod.get('tipo', 'N/A')} | "
                        f"Risco: {prod.get('risco', 'N/A')}"
                    )
        contexto.append("")
    
    # 4. Indicadores econômicos (se disponíveis)
    try:
        from src.db_indicadores import IndicadoresDatabase
        db = IndicadoresDatabase()
        indicadores = db.get_todos_indicadores_recentes()
        
        if indicadores and any([indicadores.get('selic'), indicadores.get('ipca')]):
            contexto.append("=== INDICADORES ECONÔMICOS ===")
            if indicadores.get('selic') is not None:
                contexto.append(f"Selic: {indicadores['selic']:.2f}% ao ano")
            if indicadores.get('ipca') is not None:
                contexto.append(f"IPCA: {indicadores['ipca']:.2f}% mensal")
            contexto.append(f"Data: {indicadores.get('data_consulta', 'N/A')}")
            contexto.append("")
    except Exception:
        pass
    
    return "\n".join(contexto)
    
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