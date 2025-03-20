import streamlit as st
import requests

# Definir URL da API backend
API_URL = "https://vb-sistemas.onrender.com"

# Configuração do layout
st.set_page_config(page_title="Consulta de Processos", layout="centered")
st.title("🔍 Consulta de Processos Jurídicos")
st.write("Selecione o tipo de dado e digite um termo para buscar informações.")

# Opções para tipo de pesquisa
opcoes_pesquisa = {
    "Número do Processo": "numero_processo",
    "Nome do Advogado": "advogado",
    "Tribunal": "tribunal",
    "Exequente": "exequente",
    "Executado": "executado"
}

# Seleção do tipo de pesquisa
tipo_pesquisa = st.selectbox("Escolha o tipo de dado para pesquisa:", list(opcoes_pesquisa.keys()))

# Campo de entrada para busca
search_query = st.text_input("Digite o termo para buscar...")

# Botão de busca
if st.button("Buscar"):
    if search_query:
        # Obter o parâmetro correto do dicionário
        parametro = opcoes_pesquisa[tipo_pesquisa]

        # Fazer requisição ao backend
        response = requests.get(f"{API_URL}/buscar-processos/", params={parametro: search_query})

        if response.status_code == 200:
            try:
                processos = response.json()
                if processos:
                    st.write(f"**{len(processos)} resultados encontrados:**")
                    st.json(processos)  # Exibe os dados formatados
                else:
                    st.warning("Nenhum processo encontrado.")
            except Exception as e:
                st.error(f"Erro ao processar resposta do servidor: {e}")
        else:
            st.error(f"Erro na requisição: {response.status_code}")
    else:
        st.warning("Digite um termo para buscar.")

