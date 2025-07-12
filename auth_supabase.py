import streamlit as st
from supabase_client import supabase

def login(email, senha):
    res = supabase.auth.sign_in_with_password({"email": email, "password": senha})
    if res and res.session:
        st.session_state["usuario"] = res.user
        st.session_state["token"] = res.session.access_token
        return True
    else:
        return False

def registrar(email, senha):
    res = supabase.auth.sign_up({"email": email, "password": senha})
    if res and res.user:
        st.success("Conta criada. Verifique seu email para confirmar.")
        return True
    else:
        st.error("Erro ao registrar.")
        return False

def logout():
    if "usuario" in st.session_state:
        del st.session_state["usuario"]
    if "token" in st.session_state:
        del st.session_state["token"]

