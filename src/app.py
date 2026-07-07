import sys
import os
# Adiciona o diretório pai ao path para importações funcionarem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from src import config, data_loader, llm_client  # ← IMPORTANTE: usar from src import

st.set_page_config(page_title="Agente Financeiro", page_icon="💰", layout="wide")

st.title("💰 Agente Financeiro Inteligente")

# Verifica se a API KEY está configurada
if not config.GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY não encontrada. Por favor, adicione sua chave ao arquivo .env e reinicie a aplicação.")
    st.stop()

# --- CARREGAMENTO DE DADOS E SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configurações e Dados")
    
    # Upload de arquivo pelo usuário
    st.subheader("Upload de Transações")
    uploaded_file = st.file_uploader("Substitua o histórico padrão enviando seu próprio CSV", type=["csv"])
    
    try:
        # Se usuário fez upload, carrega o arquivo dele. Senão, carrega o padrão.
        if uploaded_file is not None:
            transacoes_df = pd.read_csv(uploaded_file)
            st.success("Arquivo carregado com sucesso!")
        else:
            transacoes_df = data_loader.load_transacoes()
    except Exception as e:
        st.error(f"Erro ao carregar transações: {str(e)}")
        transacoes_df = pd.DataFrame()

    # Carrega dados do sistema (perfil e produtos)
    perfil = data_loader.load_perfil_investidor()
    produtos = data_loader.load_produtos_financeiros()

    # Exibe resumo do perfil
    if perfil:
        st.subheader("👤 Seu Perfil")
        st.write(f"**Nome:** {perfil.get('nome', 'N/A')}")
        st.write(f"**Perfil de Risco:** {perfil.get('perfil_risco', 'N/A').capitalize()}")
        st.write(f"**Renda Mensal:** R$ {perfil.get('renda_mensal', 0)}")
        st.write(f"**Patrimônio:** R$ {perfil.get('patrimonio', 0)}")

    # --- INDICADORES ECONÔMICOS ---
    st.subheader("📊 Indicadores Econômicos")
    try:
        from src.db_indicadores import IndicadoresDatabase
        db = IndicadoresDatabase()
        if db.engine:
            indicadores = db.get_todos_indicadores_recentes()
            if indicadores and any([indicadores.get('selic'), indicadores.get('ipca')]):
                col1, col2 = st.columns(2)
                with col1:
                    if indicadores.get('selic'):
                        st.metric("Selic", f"{indicadores['selic']:.2f}%")
                with col2:
                    if indicadores.get('ipca'):
                        st.metric("IPCA", f"{indicadores['ipca']:.2f}%")
                st.caption(f"Atualizado: {indicadores.get('data_consulta', 'N/A')}")
            else:
                st.info("Indicadores não disponíveis")
        else:
            st.info("🔄 Banco de dados não disponível. Indicadores não carregados.")
    except Exception as e:
        st.info("📊 Indicadores econômicos serão carregados quando disponíveis")
    
    if st.button("🗑️ Limpar Histórico da Conversa"):
        st.session_state.messages = []
        st.rerun()

# Construir o contexto para o LLM
context_str = llm_client.build_context(perfil, transacoes_df, produtos)

# --- GERENCIAMENTO DE ESTADO DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu Agente Financeiro Inteligente. Como posso te ajudar com seus investimentos e finanças hoje?"}
    ]

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT DO USUÁRIO ---
if prompt := st.chat_input("Faça uma pergunta sobre suas finanças ou investimentos"):
    # Exibe mensagem do usuário na tela e salva no estado
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chama o LLM
    with st.chat_message("assistant"):
        with st.spinner("Analisando seus dados..."):
            try:
                resposta = llm_client.chat_completion(
                    messages=st.session_state.messages,
                    context_str=context_str
                )
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro na comunicação com a API: {str(e)}")