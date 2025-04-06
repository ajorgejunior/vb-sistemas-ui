import streamlit as st
from utils import processar_pdf

def mostrar():
    st.title("📄 Enviar PDF para Processamento")
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"], help="Limite 200MB por arquivo")
    
    if uploaded_file and st.button("Enviar"):
        processar_pdf(uploaded_file)

