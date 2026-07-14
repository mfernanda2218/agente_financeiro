import sys
import os
import json
from datetime import datetime

# Adiciona o diretório pai ao path para importações funcionarem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from src import config, data_loader, llm_client
from src.components import (
    render_perfil_form,
    render_transacoes_upload,
    render_produtos_upload,
    render_analise_gastos
)

st.set_page_config(page_title="Agente Financeiro", layout="wide")

# Aplica o CSS customizado
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_indicadores_painel():
    """Renderiza painel de indicadores econômicos"""
    st.subheader("Indicadores Econômicos")
    
    # Tenta carregar do banco
    try:
        from src.db_indicadores import IndicadoresDatabase
        db = IndicadoresDatabase()
        if db.engine:
            indicadores = db.get_todos_indicadores_recentes()
            if indicadores and any([indicadores.get('selic'), indicadores.get('ipca')]):
                _render_indicadores(indicadores, fonte="Banco Central (API)")
                return
    except Exception as e:
        pass
    
    # Fallback: dados mockados
    try:
        from src.db_indicadores import get_indicadores_fallback
        indicadores = get_indicadores_fallback()
        _render_indicadores(indicadores, fonte="Dados simulados")
    except:
        st.info("Indicadores econômicos não disponíveis no momento")
    
    st.caption("Os indicadores são atualizados automaticamente.")

def _render_indicadores(indicadores, fonte):
    """Renderiza métricas de indicadores"""
    col1, col2 = st.columns(2)
    with col1:
        if indicadores.get('selic') is not None:
            st.metric("Selic", f"{indicadores['selic']:.2f}%")
    with col2:
        if indicadores.get('ipca') is not None:
            st.metric("IPCA", f"{indicadores['ipca']:.2f}%")
    
    st.caption(f"Data da Consulta: {indicadores.get('data_consulta', 'N/A')}")
    st.caption(fonte)

# ============================================
# INÍCIO DA APLICAÇÃO PRINCIPAL
# ============================================

# Verifica se a API KEY está configurada
if not config.GROQ_API_KEY:
    st.error("GROQ_API_KEY não encontrada. Por favor, adicione sua chave ao arquivo .env e reinicie a aplicação.")
    st.stop()

# Inicializa estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou seu Agente Financeiro Inteligente. Como posso te ajudar com seus investimentos e finanças hoje?"}
    ]
if "perfil" not in st.session_state:
    st.session_state.perfil = {}
if "transacoes_df" not in st.session_state:
    st.session_state.transacoes_df = pd.DataFrame()
if "produtos" not in st.session_state:
    st.session_state.produtos = {}

# ============================================
# SIDEBAR - GERENCIAMENTO DE DADOS
# ============================================

with st.sidebar:
    st.header("Configurações")
    
    # Tabs para diferentes tipos de dados
    tab1, tab2, tab3, tab4 = st.tabs(["Perfil", "Transações", "Produtos", "Indicadores"])
    
    with tab1:
        perfil = render_perfil_form()
        if perfil:
            st.session_state.perfil = perfil
    
    with tab2:
        render_transacoes_upload()
    
    with tab3:
        render_produtos_upload()
    
    with tab4:
        render_indicadores_painel()
    
    st.divider()
    
    # Painel de análise rápida
    if not st.session_state.transacoes_df.empty:
        render_analise_gastos(st.session_state.transacoes_df)
    
    # Botão para limpar conversa
    if st.button("Limpar Histórico da Conversa"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Sou seu Agente Financeiro Inteligente. Como posso te ajudar com seus investimentos e finanças hoje?"}
        ]
        st.rerun()

# ============================================
# ÁREA PRINCIPAL - CHAT
# ============================================

st.title("Agente Financeiro Inteligente")

# Exibe status dos dados
status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
    status_perfil = "Ativo" if st.session_state.perfil else "Pendente"
    st.caption(f"Perfil: {status_perfil}")
with status_col2:
    status_trans = "Carregadas" if not st.session_state.transacoes_df.empty else "Vazio"
    st.caption(f"Transações: {status_trans} ({len(st.session_state.transacoes_df)})")
with status_col3:
    status_prod = "Carregados" if st.session_state.produtos else "Vazio"
    st.caption(f"Produtos: {status_prod} ({len(st.session_state.produtos)})")

# Exibe mensagens do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# INPUT DO USUÁRIO
# ============================================

if prompt := st.chat_input("Faça uma pergunta sobre suas finanças ou investimentos"):
    # Exibe mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera resposta do LLM
    with st.chat_message("assistant"):
        with st.spinner("Analisando seus dados..."):
            try:
                # Usa dados da sessão para construir o contexto
                context_str = llm_client.build_context(
                    st.session_state.perfil,
                    st.session_state.transacoes_df,
                    st.session_state.produtos
                )
                
                resposta = llm_client.chat_completion(
                    messages=st.session_state.messages,
                    context_str=context_str
                )
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro na comunicação com a API: {str(e)}")