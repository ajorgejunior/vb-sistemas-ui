import streamlit as st
from modules import home, painel, consultar, enviar_pdf, digesto, cadastrar_digesto, conversar
from utils import verificar_status_api

st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

paginas = {
    "🏠 Início": home,
#    "📊 Painel de Estatísticas": painel,
    "🔍 Consultar Processos": consultar,
    "📄 Enviar PDF para Processamento": enviar_pdf,
    "📦 Processos da Digesto": digesto,
    "📥 Cadastrar Digesto": cadastrar_digesto,
    "💬 Conversar com Processo": conversar
}

# Redirecionamento via query string
query = st.query_params
if "page" in query:
    st.session_state.pagina_selecionada = query["page"]
    if "numero" in query:
        st.session_state.numero_digesto = query["numero"]
    st.query_params = {}  # limpa

# Sidebar com radio sincronizado ao estado
st.sidebar.title("Menu")
pagina_selecionada = st.sidebar.radio(
    "Escolha uma opção", list(paginas.keys()), key="pagina_selecionada"
)

# Renderizar a página
paginas[pagina_selecionada].mostrar()

# Rodapé com status
st.markdown("---")
api_status = verificar_status_api()
st.markdown(f"<p style='text-align: center; color: gray;'>📡 Status da API: {api_status}</p>", unsafe_allow_html=True)
