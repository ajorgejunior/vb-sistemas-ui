import streamlit as st
from modules import home, painel, consultar, enviar_pdf, digesto, cadastrar_digesto, conversar, login
from auth_supabase import logout
from utils import verificar_status_api

st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# Todas as páginas disponíveis
paginas = {
    "🔐 Login": login,
    "🏠 Início": home,
#    "📊 Painel de Estatísticas": painel,
    "🔍 Consultar Processos": consultar,
    "📄 Enviar PDF para Processamento": enviar_pdf,
    "📦 Processos da Digesto": digesto,
    "📥 Cadastrar Digesto": cadastrar_digesto,
    "💬 Conversar com Processo": conversar
}

# Se não estiver logado, força o usuário para a tela de login
if "usuario" not in st.session_state:
    st.session_state["pagina_selecionada"] = "🔐 Login"

# Redirecionamento via URL
query = st.query_params
if "page" in query:
    st.session_state.pagina_selecionada = query["page"]
    if "numero" in query:
        st.session_state.numero_digesto = query["numero"]
    st.query_params = {}

# Sidebar
st.sidebar.title("Menu")

# Exibe nome do usuário e botão de logout, se logado
if "usuario" in st.session_state and st.session_state["pagina_selecionada"] != "🔐 Login":
    user_email = st.session_state["usuario"].get("email", "usuário")
    st.sidebar.markdown(f"👤 **{user_email}**")
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.rerun()

pagina_selecionada = st.sidebar.radio(
    "Escolha uma opção", list(paginas.keys()), key="pagina_selecionada"
)

# Protege páginas que não sejam login
if st.session_state["pagina_selecionada"] != "🔐 Login" and "usuario" not in st.session_state:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

# Renderiza a página selecionada
paginas[st.session_state["pagina_selecionada"]].mostrar()

# Rodapé
st.markdown("---")
api_status = verificar_status_api()
st.markdown(f"<p style='text-align: center; color: gray;'>📡 Status da API: {api_status}</p>", unsafe_allow_html=True)

