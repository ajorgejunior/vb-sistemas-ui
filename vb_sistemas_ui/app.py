import streamlit as st
import requests

API_URL = "https://vb-sistemas.onrender.com"  # URL do backend FastAPI

st.set_page_config(page_title="VB Sistemas - Gestão de Processos", layout="wide")

st.title("🔍 Consulta de Processos Jurídicos")

# Campo de busca
search_query = st.text_input("Digite um número de processo, advogado, tribunal...")

if st.button("Buscar"):
    if search_query:
        response = requests.get(f"{API_URL}/buscar-processos/", params={"termo": search_query})
        if response.status_code == 200:
            processos = response.json()
            st.write(f"**{len(processos)} resultados encontrados:**")
            st.json(processos)
        else:
            st.error("Erro ao buscar processos.")
    else:
        st.warning("Digite um termo para buscar.")
