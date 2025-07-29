import streamlit as st
from modules import login, home, painel, consultar, enviar_pdf, digesto, cadastrar_digesto, conversar
from auth_supabase import logout
from utils import verificar_status_api

st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# Base de páginas sem login
paginas_base = {
    "🏠 Início": home,
#    "📊 Painel de Estatísticas": painel,
#    "🔍 Consultar Processos": consultar,
#    "📄 Enviar PDF para Processamento": enviar_pdf,
    "📦 Consultar Processos (API)": digesto,
    "📥 Cadastrar Processo (API)": cadastrar_digesto,
    "💬 Conversar com Processo (GPT)": conversar
}

# Adiciona "🔐 Login" se usuário não estiver logado ou ainda não preencheu nome
if "usuario" not in st.session_state or st.session_state.get("precisa_definir_nome"):
    paginas = {"🔐 Login": login, **paginas_base}
else:
    paginas = paginas_base

# Redirecionamento seguro (antes de widgets)
if st.session_state.get("redirecionar_inicio"):
    st.session_state["pagina_selecionada"] = "🏠 Início"
    del st.session_state["redirecionar_inicio"]

if st.session_state.get("redirecionar_login"):
    st.session_state["pagina_selecionada"] = "🔐 Login"
    del st.session_state["redirecionar_login"]

# Redirecionamento via URL
query = st.query_params
if "page" in query:
    st.session_state["pagina_selecionada"] = query["page"]
    if "numero" in query:
        st.session_state["numero_digesto"] = query["numero"]
    st.query_params = {}

# Inicializa página padrão
if "pagina_selecionada" not in st.session_state:
    st.session_state["pagina_selecionada"] = "🔐 Login" if "usuario" not in st.session_state else "🏠 Início"

# Sidebar
st.sidebar.title("Menu")

# Exibe nome do usuário e botão de logout
if "usuario" in st.session_state and st.session_state["pagina_selecionada"] != "🔐 Login":
    user = st.session_state["usuario"]
    nome = user.user_metadata.get("display_name") or user.email
    st.sidebar.markdown(f"👤 **{nome}**")
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.rerun()

# Navegação segura
pagina_selecionada = st.sidebar.radio("Escolha uma opção", list(paginas.keys()), key="pagina_selecionada")

# Proteção de rotas
if pagina_selecionada != "🔐 Login" and "usuario" not in st.session_state:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

# Renderiza a página
paginas[pagina_selecionada].mostrar()

# Rodapé
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: gray;'>📡 Status da API: {verificar_status_api()}</p>", unsafe_allow_html=True)

