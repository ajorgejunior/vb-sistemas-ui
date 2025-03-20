import streamlit as st
import requests

# Definir URL da API backend
API_URL = "https://vb-sistemas.onrender.com"

# Configuração do layout
st.set_page_config(page_title="Consulta de Processos", layout="centered")
st.title("🔍 Consulta de Processos Jurídicos")
st.write("Digite um número de processo, advogado, tribunal, exequente ou executado para buscar informações.")

# Campo de entrada do usuário
search_query = st.text_input("Digite um termo para buscar...")

# Botão de busca
if st.button("Buscar"):
    if search_query:
        resultados_combinados = []
        parametros = ["numero_processo", "advogado", "tribunal", "exequente", "executado"]

        # Fazer requisição para cada parâmetro e combinar os resultados
        for param in parametros:
            response = requests.get(f"{API_URL}/buscar-processos/", params={param: search_query})

            if response.status_code == 200:
                try:
                    processos = response.json()
                    if isinstance(processos, list):  # Garante que a resposta seja uma lista
                        for p in processos:
                            if isinstance(p, dict) and "numero_processo" in p:
                                resultados_combinados.append(p)
                except Exception as e:
                    st.error(f"Erro ao processar resposta do servidor para {param}: {e}")

        # Remover duplicatas (caso um processo seja encontrado em mais de um campo)
        resultados_unicos = {p["numero_processo"]: p for p in resultados_combinados}.values()

        # Exibir resultados
        if resultados_unicos:
            st.write(f"**{len(resultados_unicos)} resultados encontrados:**")
            st.json(list(resultados_unicos))  # Exibe os dados formatados
        else:
            st.warning("Nenhum processo encontrado.")

    else:
        st.warning("Digite um termo para buscar.")
