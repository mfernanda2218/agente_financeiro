import streamlit as st
import pandas as pd
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

st.title("Agente Financeiro Inteligente")

# carregar dados
transacoes = pd.read_csv("data/transacoes.csv")

with open("data/perfil_investidor.json") as f:
    perfil = json.load(f)

with open("data/produtos_financeiros.json") as f:
    produtos = json.load(f)

pergunta = st.text_input("Faça uma pergunta sobre suas finanças")

with st.spinner("Pensando..."):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

if pergunta:

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

    # Chamada à API do Ollama
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": f"""Você é um consultor financeiro responsável.
            
            Contexto:
            {contexto}

            Pergunta do cliente:
            {pergunta}""",
            "stream": False
        }
    )
    
    if response.status_code == 200:
        resultado = response.json()
        st.write(resultado.get("response", "Desculpe, não consegui processar sua pergunta."))
    else:
        st.write(f"Erro ao conectar com o Ollama: {response.status_code}")