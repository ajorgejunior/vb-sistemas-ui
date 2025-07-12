import streamlit as st
from supabase_client import supabase

def login(email, senha):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": senha})
        if res and res.session:
            user = res.user
            st.session_state["usuario"] = user
            st.session_state["token"] = res.session.access_token

            display_name = user.user_metadata.get("display_name")
            if not display_name or str(display_name).strip().lower() in ["", "null"]:
                st.session_state["precisa_definir_nome"] = True
                st.session_state["redirecionar_login"] = True
            else:
                st.session_state["redirecionar_inicio"] = True

            return True
    except Exception as e:
        st.error("Erro ao fazer login: " + str(e))
    return False

def registrar(email, senha):
    try:
        res = supabase.auth.sign_up({"email": email, "password": senha})
        if res and res.user:
            return True
    except Exception as e:
        st.error("Erro ao registrar: " + str(e))
    return False

def recuperar_senha(email):
    try:
        supabase.auth.reset_password_email(email)
        return True
    except Exception:
        return False

def logout():
    for chave in ["usuario", "token", "login_time", "precisa_definir_nome", "redirecionar_inicio", "redirecionar_login"]:
        st.session_state.pop(chave, None)

