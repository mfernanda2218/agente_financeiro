import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import config, data_loader, llm_client

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