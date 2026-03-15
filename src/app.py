import streamlit as st
import pandas as pd
import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

        # Chamada à API do Groq
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um consultor financeiro responsável."
                },
                {
                    "role": "user",
                    "content": f"""Contexto:
            {contexto}

            Pergunta do cliente:
            {pergunta}"""
                }
            ]
        )
        
        st.write(response.choices[0].message.content)