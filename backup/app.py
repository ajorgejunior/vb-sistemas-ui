import streamlit as st
from modules import painel, consultar, enviar_pdf
from utils import verificar_status_api  # Agora importamos a verificação da API do utils.py

# Configuração da interface
st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# Dicionário para renomear os itens do menu
paginas = {
    "📊 Painel de Estatísticas": painel,
    "🔍 Consultar Processos": consultar,
    "📄 Enviar PDF para Processamento": enviar_pdf
}

# Criar menu no sidebar com os nomes personalizados
st.sidebar.title("Menu")
pagina_selecionada = st.sidebar.radio("Escolha uma opção", list(paginas.keys()))

# Carregar a página correspondente
paginas[pagina_selecionada].mostrar()

# Adicionar verificação do status da API no rodapé
st.markdown("---")
api_status = verificar_status_api()
st.markdown(f"<p style='text-align: center; color: gray;'>📡 Status da API: {api_status}</p>", unsafe_allow_html=True)

