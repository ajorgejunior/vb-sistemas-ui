import streamlit as st
import requests
from utils import API_URL, exibir_detalhes_processo

def mostrar():
    st.title("🔍 Consulta de Processos Jurídicos")
    termo_busca = st.text_input("Digite um número de processo, advogado, tribunal...")
    tipo_busca = st.selectbox("Escolha o tipo de dado para pesquisa:", ["numero_processo", "advogado", "executado", "exequente", "tribunal"])

    if st.button("Buscar") and termo_busca:
        response = requests.get(f"{API_URL}/buscar-processos/?{tipo_busca}={termo_busca}")
        if response.status_code == 200:
            processos = response.json().get("processos", [])
            if processos:
                for processo in processos:
                    exibir_detalhes_processo(processo)
            else:
                st.warning("Nenhum processo encontrado.")
        else:
            st.error("Erro ao buscar processos.")

