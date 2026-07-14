# NOVO: src/components/perfil_upload.py
import streamlit as st
import json

def render_perfil_form():
    """Renderiza formulário para cadastro do perfil do investidor"""
    st.subheader("Seu Perfil")
    
    # Se já existe perfil na sessão, preenche os campos
    perfil_existente = st.session_state.get("perfil", {})
    
    with st.form("perfil_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo", value=perfil_existente.get("nome", ""))
            idade = st.number_input("Idade", 18, 100, value=perfil_existente.get("idade", 30))
            renda_mensal = st.number_input("Renda mensal (R$)", 0, 1000000, value=perfil_existente.get("renda_mensal", 5000))
        with col2:
            perfil_risco = st.selectbox(
                "Perfil de risco",
                ["conservador", "moderado", "agressivo"],
                index=["conservador", "moderado", "agressivo"].index(perfil_existente.get("perfil_risco", "moderado")) if perfil_existente.get("perfil_risco") in ["conservador", "moderado", "agressivo"] else 1
            )
            patrimonio = st.number_input("Patrimônio total (R$)", 0, 100000000, value=perfil_existente.get("patrimonio", 50000))
            objetivos_opcoes = ["aposentadoria", "compra de imóvel", "viagem", "educação", "reserva de emergência", "empreender"]
            
            # Filtra os objetivos existentes para garantir que só existam opções válidas
            objetivos_default = [obj for obj in perfil_existente.get("objetivos", []) if obj in objetivos_opcoes]
            
            objetivos = st.multiselect(
                "Objetivos financeiros",
                objetivos_opcoes,
                default=objetivos_default
            )
        
        col3, col4 = st.columns(2)
        with col3:
            experiencia = st.selectbox(
                "Experiência com investimentos",
                ["iniciante", "intermediario", "avancado"],
                index=["iniciante", "intermediario", "avancado"].index(perfil_existente.get("experiencia_investimento", "intermediario")) if perfil_existente.get("experiencia_investimento") in ["iniciante", "intermediario", "avancado"] else 1
            )
        with col4:
            # Campo opcional para upload de arquivo JSON
            uploaded_json = st.file_uploader(
                "Ou importe JSON", 
                type=["json"],
                help="Importe um arquivo JSON com os dados do perfil"
            )
        
        submitted = st.form_submit_button("Salvar Perfil")
        
        if submitted:
            if uploaded_json:
                try:
                    perfil = json.load(uploaded_json)
                    st.session_state.perfil = perfil
                    st.success("Perfil importado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao carregar JSON: {str(e)}")
            else:
                # Salva do formulário
                perfil = {
                    "nome": nome or "Usuário",
                    "idade": idade,
                    "perfil_risco": perfil_risco,
                    "renda_mensal": renda_mensal,
                    "patrimonio": patrimonio,
                    "objetivos": objetivos,
                    "experiencia_investimento": experiencia
                }
                st.session_state.perfil = perfil
                st.success("Perfil salvo com sucesso!")
                st.rerun()
    
    # Exibe perfil atual se existir
    if "perfil" in st.session_state and st.session_state.perfil:
        perfil = st.session_state.perfil
        st.success(f"Perfil de {perfil.get('nome', 'Usuário')} carregado")
        st.caption(f"Risco: {perfil.get('perfil_risco', 'N/A').capitalize()} | Renda: R$ {perfil.get('renda_mensal', 0):,.2f}")
        return perfil
    return None