import streamlit as st
from auth_supabase import login, registrar, recuperar_senha
from supabase_client import supabase
from datetime import datetime

def mostrar():
    if st.session_state.get("precisa_definir_nome"):
        st.title("👤 Defina seu nome de exibição")
        nome = st.text_input("Nome completo")

        if st.button("Salvar nome"):
            try:
                supabase.auth.update_user({"data": {"display_name": nome}})
                novo_usuario = supabase.auth.get_user().user
                st.session_state["usuario"] = novo_usuario
                del st.session_state["precisa_definir_nome"]
                st.session_state["redirecionar_inicio"] = True
                st.rerun()
            except Exception as e:
                st.error("Erro ao salvar nome: " + str(e))
        return

    st.title("🔐 Login no Sistema")

    tipo = st.radio("Acesso", ["Login", "Registrar nova conta"])
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if tipo == "Login":
        if st.button("Entrar"):
            if login(email, senha):
                st.success("Login realizado com sucesso!")
                st.session_state["login_time"] = datetime.utcnow()
                st.rerun()
            else:
                st.error("Falha ao logar.")
    else:
        if st.button("Registrar"):
            if registrar(email, senha):
                st.success("Conta criada com sucesso! Verifique seu email e faça login.")
            else:
                st.error("Erro ao registrar conta.")

    with st.expander("🔁 Esqueci minha senha"):
        email_recup = st.text_input("Email para recuperação", key="recuperacao_email")
        if st.button("Enviar link de recuperação"):
            if recuperar_senha(email_recup):
                st.success("Link enviado para seu email.")
            else:
                st.error("Não foi possível enviar o link.")

