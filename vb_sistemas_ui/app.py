import streamlit as st
import requests
import json
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# Sidebar para seleção de funcionalidade
st.sidebar.title("Menu")
pagina = st.sidebar.radio("Selecione uma opção", ["Consulta de Processos", "Enviar PDF"])

# Definição da URL da API
API_URL = "https://vb-sistemas.onrender.com"

if pagina == "Consulta de Processos":
    st.title("🔍 Consulta de Processos Jurídicos")
    st.write("Selecione o tipo de dado e digite um termo para buscar informações.")

    # Opções para busca
    opcoes_busca = {
        "Número do Processo": "numero_processo",
        "Advogado": "advogado",
        "Executado": "executado",
        "Exequente": "exequente",
        "Tribunal/Órgão Julgador": "tribunal"
    }

    tipo_busca = st.selectbox("Escolha o tipo de dado para pesquisa:", list(opcoes_busca.keys()))
    termo_busca = st.text_input("Digite o termo para buscar...")

    if st.button("Buscar"):
        if not termo_busca.strip():
            st.warning("Por favor, digite um termo para buscar.")
        else:
            # Faz a requisição para a API
            parametro_api = opcoes_busca[tipo_busca]
            response = requests.get(f"{API_URL}/buscar-processos/", params={parametro_api: termo_busca})

            if response.status_code == 200:
                dados = response.json().get("processos", [])
                
                if dados:
                    st.success(f"{len(dados)} resultados encontrados:")
                    for processo in dados:
                        with st.expander(f"📂 Processo: {processo['numero_processo']}"):
                            st.markdown(f"**📍 Tribunal:** {processo.get('jurisdicao', 'N/A')}")
                            st.markdown(f"**🏛 Órgão Julgador:** {processo.get('orgao_julgador', 'N/A')}")
                            st.markdown(f"**⚖️ Classe:** {processo.get('classe', 'N/A')}")
                            st.markdown(f"**📌 Assunto:** {processo.get('assunto', 'N/A')}")
                            st.markdown(f"**💰 Valor da Causa:** R$ {processo.get('valor_causa', 0):,.2f}")
                            st.markdown(f"**👥 Exequente:** {processo.get('exequente', 'N/A')}")
                            st.markdown(f"**👨‍⚖️ Executado:** {processo.get('executado', 'N/A')}")
                            st.markdown(f"**⚖️ Advogados:** {', '.join(json.loads(processo['advogados'])) if 'advogados' in processo else 'N/A'}")
                            st.markdown(f"**📆 Data de Criação:** {processo.get('data_criacao', 'N/A')}")

                            movimentacoes = json.loads(processo["movimentacoes"]) if "movimentacoes" in processo else []
                            if movimentacoes:
                                st.markdown("**📜 Movimentações:**")
                                for mov in movimentacoes:
                                    st.markdown(f"- {mov}")
                else:
                    st.warning("Nenhum processo encontrado.")
            else:
                st.error("Erro ao buscar processos.")

elif pagina == "Enviar PDF":
    st.title("📤 Enviar PDF para Processamento")
    st.write("Envie um arquivo PDF contendo informações sobre processos jurídicos para extração e cadastro no sistema.")

    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Enviar"):
            files = {"pdf": uploaded_file.getvalue()}
            response = requests.post(f"{API_URL}/processar-pdf/", files=files)

            if response.status_code == 200:
                st.success("Arquivo processado e salvo no banco de dados com sucesso!")
            else:
                st.error(f"Erro ao enviar o arquivo. Código {response.status_code}")
