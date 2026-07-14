# NOVO: src/components/transacoes_upload.py
import streamlit as st
import pandas as pd

from datetime import datetime
from src import data_loader

def render_transacoes_upload():
    """Renderiza área de upload de transações"""
    st.subheader("Suas Transações")
    
    # Opção: upload de arquivo
    uploaded_file = st.file_uploader(
        "Faça upload do seu CSV de transações",
        type=["csv"],
        help="CSV deve ter colunas: data,valor,categoria,descricao"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            # Validação básica
            required_cols = ["data", "valor", "categoria", "descricao"]
            if all(col in df.columns for col in required_cols):
                st.session_state.transacoes_df = df
                st.success(f"{len(df)} transações carregadas!")
                st.rerun()
            else:
                st.error(f"CSV deve conter colunas: {', '.join(required_cols)}")
        except Exception as e:
            st.error(f"Erro ao carregar CSV: {str(e)}")
    
    # Opção: cadastro manual
    st.caption("Ou registre manualmente:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        manual_data = st.date_input("Data", value=datetime.now().date())
    with col2:
        manual_valor = st.number_input("Valor (R$)", step=0.01)
    with col3:
        manual_categoria = st.selectbox(
            "Categoria",
            ["alimentacao", "transporte", "moradia", "lazer", 
             "saude", "educacao", "compras", "salario", "investimento", "outros"]
        )
    with col4:
        manual_descricao = st.text_input("Descrição", placeholder="Ex: Supermercado")
    
    if st.button("Adicionar transação manual"):
        if manual_data and manual_valor != 0:
            nova_transacao = {
                "data": manual_data.strftime("%Y-%m-%d"),
                "valor": manual_valor,
                "categoria": manual_categoria,
                "descricao": manual_descricao or manual_categoria
            }
            
            if "transacoes_df" not in st.session_state or st.session_state.transacoes_df.empty:
                st.session_state.transacoes_df = pd.DataFrame(columns=["data", "valor", "categoria", "descricao"])
            
            # Converte dicionário para DataFrame e concatena
            nova_linha = pd.DataFrame([nova_transacao])
            st.session_state.transacoes_df = pd.concat(
                [st.session_state.transacoes_df, nova_linha], 
                ignore_index=True
            )
            st.success("Transação adicionada!")
            st.rerun()
        else:
            st.warning("Preencha data e valor (diferente de zero)")
    
    # Exibe transações atuais
    if "transacoes_df" in st.session_state and not st.session_state.transacoes_df.empty:
        st.dataframe(st.session_state.transacoes_df.head(20), use_container_width=True)
        st.caption(f"Total: {len(st.session_state.transacoes_df)} transações")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Limpar todas as transações"):
                st.session_state.transacoes_df = pd.DataFrame(columns=["data", "valor", "categoria", "descricao"])
                st.rerun()
        with col2:
            # Botão para carregar transações de exemplo
            if st.button("Carregar exemplo"):
                st.session_state.transacoes_df = data_loader.load_transacoes()
                st.rerun()