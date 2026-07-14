# NOVO: src/components/produtos_upload.py
import streamlit as st
import json
import pandas as pd

from src import data_loader

def render_produtos_upload():
    """Renderiza área de gerenciamento de produtos"""
    st.subheader("Produtos Financeiros")
    
    # Upload de produtos via JSON
    uploaded_produtos = st.file_uploader(
        "Importar catálogo de produtos (JSON)",
        type=["json"],
        help="JSON com lista de produtos financeiros"
    )
    
    if uploaded_produtos:
        try:
            produtos = json.load(uploaded_produtos)
            st.session_state.produtos = produtos
            st.success(f"{len(produtos)} produtos carregados!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar produtos: {str(e)}")
    
    # Opção: adicionar produto manualmente
    with st.expander("Adicionar novo produto manualmente"):
        col1, col2 = st.columns(2)
        with col1:
            novo_nome = st.text_input("Nome do produto")
            novo_tipo = st.selectbox(
                "Tipo",
                ["renda_fixa", "renda_variavel", "fundo_investimento", "criptomoeda"]
            )
            novo_risco = st.selectbox("Risco", ["baixo", "medio", "alto"])
        with col2:
            novo_rentabilidade = st.text_input("Rentabilidade (ex: 120% CDI)")
            novo_minimo = st.number_input("Investimento mínimo (R$)", 0.0, 1000000.0, 100.0)
            novo_liquidez = st.text_input("Liquidez (ex: diaria, 30 dias)")
        
        if st.button("Adicionar produto"):
            if novo_nome:
                novo_produto = {
                    "nome": novo_nome,
                    "tipo": novo_tipo,
                    "rentabilidade": novo_rentabilidade or "variavel",
                    "risco": novo_risco,
                    "minimo_investimento": novo_minimo,
                    "liquidez": novo_liquidez or "indisponivel"
                }
                
                if "produtos" not in st.session_state:
                    st.session_state.produtos = {}
                
                # Usa nome como chave ou gera um ID
                produto_id = novo_nome.lower().replace(" ", "_")
                st.session_state.produtos[produto_id] = novo_produto
                st.success(f"Produto '{novo_nome}' adicionado!")
                st.rerun()
            else:
                st.warning("Digite o nome do produto")
    
    # Exibe produtos atuais
    if "produtos" in st.session_state and st.session_state.produtos:
        st.subheader("Catálogo atual")
        produtos_list = []
        for key, prod in st.session_state.produtos.items():
            if isinstance(prod, dict):
                produtos_list.append({
                    "ID": key,
                    "Nome": prod.get("nome", ""),
                    "Tipo": prod.get("tipo", ""),
                    "Risco": prod.get("risco", ""),
                    "Rentabilidade": prod.get("rentabilidade", ""),
                    "Mínimo": f"R$ {prod.get('minimo_investimento', 0):.2f}",
                    "Liquidez": prod.get("liquidez", "")
                })
        
        if produtos_list:
            df_produtos = pd.DataFrame(produtos_list)
            st.dataframe(df_produtos, use_container_width=True)
        
        if st.button("Limpar produtos"):
            st.session_state.produtos = {}
            st.rerun()
    
    # Produtos padrão de fallback
    if "produtos" not in st.session_state or not st.session_state.produtos:
        if st.button("Carregar produtos padrão"):
            st.session_state.produtos = data_loader.load_produtos_financeiros()
            st.success("Produtos padrão carregados!")
            st.rerun()