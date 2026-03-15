import streamlit as st
import pandas as pd
import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Agente Financeiro Inteligente")

# carregar dados
transacoes = pd.read_csv("data/transacoes.csv")

with open("data/perfil_investidor.json") as f:
    perfil = json.load(f)

with open("data/produtos_financeiros.json") as f:
    produtos = json.load(f)

pergunta = st.text_input("Faça uma pergunta sobre suas finanças")

if pergunta:
    with st.spinner("Pensando..."):
        contexto = f"""
        Perfil do cliente:
        {perfil}

        Transações recentes:
        {transacoes.head(20).to_string()}

        Produtos disponíveis:
        {produtos}
        """

        prompt = f"""
        Contexto:
        {contexto}

        Pergunta do cliente:
        {pergunta}
        """

        # Chamada à API do Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""Você é um consultor financeiro responsável.
            
            Contexto:
            {contexto}

            Pergunta do cliente:
            {pergunta}"""
        )
        
        st.write(response.text)