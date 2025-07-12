import streamlit as st
from auth_supabase import login, registrar

def mostrar():
    st.title("🔐 Login no Sistema")

    tipo = st.radio("Acesso", ["Login", "Registrar nova conta"])
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if tipo == "Login":
        if st.button("Entrar"):
            if login(email, senha):
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Falha ao logar.")
    else:
        if st.button("Registrar"):
            registrar(email, senha)

